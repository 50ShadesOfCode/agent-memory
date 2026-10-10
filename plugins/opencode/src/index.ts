import { spawn, spawnSync } from "node:child_process";
import { appendFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { pathToFileURL } from "node:url";
import { Plugin } from "@opencode/plugin";
import { buildHookEvent, firstToken, toHistoryItems, unseenItems } from "./memory.ts";

const EXECUTOR_ENV = "AGENT_MEMORY_EXECUTOR";
const DEFAULT_PERIOD_MS = 600_000;
const THROTTLE_MS = 5_000;

interface Options {
  hook?: string;
  store?: string;
  periodMs?: number;
  throttleMs?: number;
}

interface Context {
  options?: unknown;
  session: {
    context(input: { sessionID: string }): Promise<unknown>;
    get(input: { sessionID: string }): Promise<unknown>;
    hook(name: string, callback: (event: any) => void | Promise<void>): Promise<unknown>;
  };
  tool: {
    hook(name: string, callback: (event: any) => void | Promise<void>): Promise<unknown>;
  };
  command: {
    transform(callback: (editor: any) => void): Promise<unknown>;
  };
  event: {
    subscribe(options?: { signal?: AbortSignal }): AsyncIterable<unknown>;
  };
  storage: {
    get(key: string): Promise<unknown>;
    set(key: string, value: unknown): Promise<void>;
  };
}

const lastRun = new Map<string, number>();

function hookBinary(hook: string): string {
  return join(dirname(firstToken(hook)), "mem");
}

function storeLog(store: string, message: string): void {
  try {
    mkdirSync(join(store, ".state"), { recursive: true });
    appendFileSync(join(store, ".state", "hooks.log"), `${message}\n`);
  } catch {
    /* logging must never break the host */
  }
}

function pipeHook(hook: string, payload: unknown): boolean {
  const result = spawnSync("/bin/sh", ["-c", hook], {
    input: JSON.stringify(payload),
    timeout: 60_000,
    stdio: ["pipe", "ignore", "ignore"],
  });
  return !result.error && result.status === 0;
}

async function pointerOf(ctx: Context, sessionID: string): Promise<string | null> {
  const pointer = await ctx.storage.get(`pointer:${sessionID}`);
  return typeof pointer === "string" ? pointer : null;
}

async function remember(ctx: Context, sessionID: string): Promise<void> {
  const known = await ctx.storage.get("sessions");
  const sessions: string[] = Array.isArray(known) ? known.filter((id) => typeof id === "string") : [];
  if (!sessions.includes(sessionID)) {
    sessions.push(sessionID);
    await ctx.storage.set("sessions", sessions);
  }
}

async function forget(ctx: Context, sessionID: string): Promise<void> {
  const known = await ctx.storage.get("sessions");
  const sessions: string[] = Array.isArray(known) ? known.filter((id) => typeof id === "string") : [];
  if (sessions.includes(sessionID)) {
    await ctx.storage.set(
      "sessions",
      sessions.filter((id) => id !== sessionID),
    );
  }
}

const DISTILL_TITLE = "agent-memory-distill";

async function executorOwned(ctx: Context, sessionID: string): Promise<boolean> {
  if (process.env[EXECUTOR_ENV]) return true;
  try {
    const info = (await ctx.session.get({ sessionID })) as { title?: unknown } | null;
    return typeof info?.title === "string" && info.title === DISTILL_TITLE;
  } catch {
    return false;
  }
}

async function capture(
  ctx: Context,
  opts: Required<Pick<Options, "hook" | "store">> & { throttleMs: number },
  sessionID: string,
  trigger: string,
): Promise<void> {
  try {
    const now = Date.now();
    if (now - (lastRun.get(sessionID) ?? 0) < opts.throttleMs) return;
    lastRun.set(sessionID, now);
    if (await executorOwned(ctx, sessionID)) return;
    const messages = await ctx.session.context({ sessionID });
    const history = toHistoryItems(Array.isArray(messages) ? messages : []);
    const { items, pointer } = unseenItems(history, await pointerOf(ctx, sessionID));
    if (items.length === 0 || pointer === null) return;
    // Full history, not the delta: the watermark slices what it already saw.
    if (!pipeHook(opts.hook, buildHookEvent(sessionID, trigger, history))) return;
    await ctx.storage.set(`pointer:${sessionID}`, pointer);
    await remember(ctx, sessionID);
  } catch (error) {
    storeLog(opts.store, `capture failed: ${String(error)}`);
  }
}

function inject(event: any, store: string): void {
  try {
    const index = join(store, "MEMORY.md");
    if (!existsSync(index) || readFileSync(index, "utf-8").trim() === "") return;
    event.prompt.files ??= [];
    event.prompt.files.push({ uri: pathToFileURL(index).href });
  } catch (error) {
    storeLog(store, `inject failed: ${String(error)}`);
  }
}

function launchDistill(opts: Required<Pick<Options, "hook" | "store">>, sessionID: string): void {
  try {
    const child = spawn(
      hookBinary(opts.hook),
      ["distill", "--session", sessionID, "--reason", "host", "--reason-host", "opencode"],
      {
        detached: true,
        stdio: "ignore",
        env: { ...process.env, AGENT_MEMORY_STORE: opts.store, [EXECUTOR_ENV]: "1" },
      },
    );
    child.on("error", (error) => storeLog(opts.store, `distill launch failed: ${String(error)}`));
    child.unref();
  } catch (error) {
    storeLog(opts.store, `distill launch failed: ${String(error)}`);
  }
}

export default Plugin.define({
  id: "agent-memory",
  async setup(ctx: unknown) {
    if (process.env[EXECUTOR_ENV]) return;
    const outer = ctx as Context;
    const opts = (outer.options ?? {}) as Options;
    if (!opts.hook || !opts.store) return;
    const run = { hook: opts.hook, store: opts.store, throttleMs: opts.throttleMs ?? THROTTLE_MS };

    const known = await outer.storage.get("sessions").catch(() => []);
    const sessions: string[] = Array.isArray(known) ? known.filter((id) => typeof id === "string") : [];
    for (const sessionID of sessions) {
      await capture(outer, run, sessionID, "backfill");
    }

    await outer.session.hook("prompt", async (event: any) => {
      if (typeof event?.sessionID === "string") await capture(outer, run, event.sessionID, "prompt");
      inject(event, run.store);
    });
    await outer.tool.hook("execute.after", async (event: any) => {
      if (typeof event?.sessionID === "string") await capture(outer, run, event.sessionID, "tool");
    });
    await outer.session.hook("compaction", async (event: any) => {
      if (typeof event?.sessionID === "string") await capture(outer, run, event.sessionID, "compaction");
    });
    await outer.command.transform((editor: any) => {
      editor.add({
        name: "mem-distill",
        description: "Distill archived conversation into memories",
        execute: async ({ sessionID }: any) => {
          if (typeof sessionID === "string") {
            await capture(outer, run, sessionID, "command");
            launchDistill(run, sessionID);
          }
        },
      });
    });

    const timer = setInterval(() => {
      void (async () => {
        const current = await outer.storage.get("sessions").catch(() => []);
        const ids: string[] = Array.isArray(current) ? current.filter((id) => typeof id === "string") : [];
        for (const sessionID of ids) {
          await capture(outer, run, sessionID, "timer");
        }
      })();
    }, opts.periodMs ?? DEFAULT_PERIOD_MS);
    const events = new AbortController();
    void (async () => {
      try {
        for await (const raw of outer.event.subscribe({ signal: events.signal })) {
          const type = (raw as { type?: unknown } | null)?.type;
          const data = (raw as { data?: unknown } | null)?.data;
          const sessionID = (data as { sessionID?: unknown } | null)?.sessionID;
          if (typeof sessionID !== "string") continue;
          if (type === "session.created") {
            await remember(outer, sessionID);
          } else if (
            type === "session.idle" ||
            type === "session.execution.succeeded" ||
            type === "session.execution.failed"
          ) {
            await capture(outer, run, sessionID, "idle");
          } else if (type === "session.deleted") {
            await forget(outer, sessionID);
          }
        }
      } catch {
        /* the stream ends with unload */
      }
    })();
    return () => {
      events.abort();
      clearInterval(timer);
    };
  },
});
