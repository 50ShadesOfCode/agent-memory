import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, unlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import plugin from "./index.ts";

const DISTILL_TITLE = "agent-memory-distill";

interface Stub {
  ctx: any;
  handlers: Record<string, (event: any) => unknown>;
  commandDef: any;
  storage: Map<string, unknown>;
}

function stub(
  options: Record<string, unknown>,
  messages: unknown[] = [],
  scriptedEvents: unknown[] = [],
): Stub {
  const handlers: Record<string, (event: any) => unknown> = {};
  const storage = new Map<string, unknown>();
  let commandDef: any = null;
  const ctx = {
    options,
    session: {
      context: async () => messages,
      get: async () => ({ id: "s1", title: "work" }),
      hook: async (name: string, cb: (event: any) => unknown) => {
        handlers[name] = cb;
      },
    },
    event: {
      subscribe: async function* () {
        yield* scriptedEvents;
      },
    },
    tool: {
      hook: async (name: string, cb: (event: any) => unknown) => {
        handlers[`tool:${name}`] = cb;
      },
    },
    command: {
      transform: async (cb: (editor: any) => void) => {
        cb({ add: (def: any) => (commandDef = def) });
      },
    },
    storage: {
      get: async (key: string) => storage.get(key),
      set: async (key: string, value: unknown) => {
        storage.set(key, value);
      },
    },
  };
  return {
    ctx,
    handlers,
    get commandDef() {
      return commandDef;
    },
    storage,
  };
}

async function start(s: Stub): Promise<() => void> {
  const cleanup = await (plugin as any).setup(s.ctx);
  return typeof cleanup === "function" ? cleanup : () => {};
}

function store(): string {
  return mkdtempSync(join(tmpdir(), "mem-plugin-"));
}

function messages(): unknown[] {
  return [{ messageID: "m1", role: "user", parts: [{ type: "text", text: "hi" }] }];
}

async function waitFor(fn: () => unknown | Promise<unknown>, timeoutMs = 5000): Promise<void> {
  const start = Date.now();
  while ((await fn()) === undefined) {
    if (Date.now() - start > timeoutMs) throw new Error("timed out waiting for condition");
    await new Promise((resolve) => setTimeout(resolve, 25));
  }
}

test("failing hook still admits the prompt and advances no pointer", async () => {
  const dir = store();
  const s = stub(
    { hook: "/nonexistent-mem-hook --host opencode", store: dir, throttleMs: 0 },
    messages(),
  );
  const done = await start(s);
  try {
    await s.handlers["prompt"]({ sessionID: "s-fail", prompt: { text: "hi", files: [] } });
    await new Promise((resolve) => setTimeout(resolve, 200));
    assert.equal(await s.storage.get("pointer:s-fail"), undefined);
  } finally {
    done();
  }
});

test("working hook advances the pointer", async () => {
  const dir = store();
  const s = stub({ hook: "true", store: dir, throttleMs: 0 }, messages());
  const done = await start(s);
  try {
    await s.handlers["prompt"]({ sessionID: "s-work", prompt: { text: "hi", files: [] } });
    await waitFor(async () => await s.storage.get("pointer:s-work"));
    assert.equal(await s.storage.get("pointer:s-work"), "m1");
  } finally {
    done();
  }
});

test("polled triggers respect the throttle", async () => {
  const dir = store();
  const seen: unknown[] = messages();
  const s = stub({ hook: "true", store: dir }, seen);
  const done = await start(s);
  try {
    await s.handlers["tool:execute.after"]({ sessionID: "s-throttle" });
    await waitFor(async () => await s.storage.get("pointer:s-throttle"));
    seen.push({ messageID: "m2", role: "user", parts: [{ type: "text", text: "more" }] });
    await s.handlers["tool:execute.after"]({ sessionID: "s-throttle" });
    await new Promise((resolve) => setTimeout(resolve, 200));
    assert.equal(await s.storage.get("pointer:s-throttle"), "m1");
  } finally {
    done();
  }
});

test("a failed forward never suppresses the retry", async () => {
  const dir = store();
  const marker = join(dir, "broken");
  writeFileSync(marker, "", "utf-8");
  const s = stub({ hook: `test ! -f ${marker}`, store: dir, throttleMs: 60000 }, messages());
  const done = await start(s);
  try {
    await s.handlers["tool:execute.after"]({ sessionID: "s-retry" });
    unlinkSync(marker);
    await s.handlers["tool:execute.after"]({ sessionID: "s-retry" });
    await waitFor(async () => await s.storage.get("pointer:s-retry"));
    assert.equal(await s.storage.get("pointer:s-retry"), "m1");
  } finally {
    done();
  }
});
test("a no-op capture never suppresses the next productive one", async () => {
  const dir = store();
  const seen: unknown[] = messages();
  const s = stub({ hook: "true", store: dir }, seen);
  const done = await start(s);
  try {
    await s.handlers["prompt"]({ sessionID: "s-noop", prompt: { text: "hi", files: [] } });
    await waitFor(async () => await s.storage.get("pointer:s-noop"));
    await s.handlers["prompt"]({ sessionID: "s-noop", prompt: { text: "hi", files: [] } });
    seen.push({ messageID: "m2", role: "user", parts: [{ type: "text", text: "more" }] });
    await s.handlers["prompt"]({ sessionID: "s-noop", prompt: { text: "hi", files: [] } });
    await waitFor(async () => (await s.storage.get("pointer:s-noop") === "m2" ? true : undefined));
    assert.equal(await s.storage.get("pointer:s-noop"), "m2");
  } finally {
    done();
  }
});

test("executor-owned process registers nothing", async () => {
  process.env.AGENT_MEMORY_EXECUTOR = "1";
  try {
    const s = stub({ hook: "true", store: store() });
    const done = await start(s);
    try {
      assert.deepEqual(Object.keys(s.handlers), []);
    } finally {
      done();
    }
  } finally {
    delete process.env.AGENT_MEMORY_EXECUTOR;
  }
});

test("distill-titled sessions are skipped", async () => {
  const dir = store();
  const s = stub({ hook: "true", store: dir, throttleMs: 0 }, messages());
  s.ctx.session.get = async () => ({ id: "s1", title: DISTILL_TITLE });
  const done = await start(s);
  try {
    await s.handlers["prompt"]({ sessionID: "s-title", prompt: { text: "hi", files: [] } });
    await new Promise((resolve) => setTimeout(resolve, 200));
    assert.equal(await s.storage.get("pointer:s-title"), undefined);
  } finally {
    done();
  }
});

test("an unverifiable session is skipped, not captured", async () => {
  const dir = store();
  const s = stub({ hook: "true", store: dir, throttleMs: 0 }, messages());
  s.ctx.session.get = async () => {
    throw new Error("transient outage");
  };
  const done = await start(s);
  try {
    await s.handlers["prompt"]({ sessionID: "s-dark", prompt: { text: "hi", files: [] } });
    await new Promise((resolve) => setTimeout(resolve, 200));
    assert.equal(await s.storage.get("pointer:s-dark"), undefined);
  } finally {
    done();
  }
});

test("a custom distill title is honored", async () => {
  const dir = store();
  const s = stub(
    { hook: "true", store: dir, throttleMs: 0, distillTitle: "custom-mark" },
    messages(),
  );
  s.ctx.session.get = async () => ({ id: "s1", title: "custom-mark" });
  const done = await start(s);
  try {
    await s.handlers["prompt"]({ sessionID: "s-custom", prompt: { text: "hi", files: [] } });
    await new Promise((resolve) => setTimeout(resolve, 200));
    assert.equal(await s.storage.get("pointer:s-custom"), undefined);
  } finally {
    done();
  }
});

test("inject attaches MEMORY.md to the prompt", async () => {
  const dir = store();
  writeFileSync(join(dir, "MEMORY.md"), "# memory\n", "utf-8");
  const s = stub({ hook: "true", store: dir, throttleMs: 0 }, []);
  const done = await start(s);
  try {
    const event = { sessionID: "s-inject", prompt: { text: "hi", files: [] as Array<{ uri: string }> } };
    await s.handlers["prompt"](event);
    assert.equal(event.prompt.files.length, 1);
    assert.match(event.prompt.files[0].uri, /MEMORY\.md$/);
  } finally {
    done();
  }
});

test("distill launch failure is logged, never thrown", async () => {
  const dir = store();
  const s = stub(
    { hook: "/nonexistent-dir/mem-hook --host opencode", store: dir, throttleMs: 0 },
    [],
  );
  const done = await start(s);
  try {
    await s.commandDef.execute({ sessionID: "s1" });
    await new Promise((resolve) => setTimeout(resolve, 500));
    const log = readFileSync(join(dir, ".state", "hooks.log"), "utf-8");
    assert.match(log, /distill launch failed/);
  } finally {
    done();
  }
});

test("session.created teaches the plugin new sessions", async () => {
  const dir = store();
  const s = stub({ hook: "true", store: dir, throttleMs: 0 }, [], [
    { type: "session.created", data: { sessionID: "s9" } },
  ]);
  const done = await start(s);
  try {
    await new Promise((resolve) => setTimeout(resolve, 100));
    const known = await s.storage.get("sessions") as string[];
    assert.ok(known.includes("s9"));
  } finally {
    done();
  }
});

test("session.idle captures the finished turn", async () => {
  const dir = store();
  const s = stub({ hook: "true", store: dir, throttleMs: 0 }, messages(), [
    { type: "session.idle", data: { sessionID: "s-idle" } },
  ]);
  const done = await start(s);
  try {
    await new Promise((resolve) => setTimeout(resolve, 100));
    assert.equal(await s.storage.get("pointer:s-idle"), "m1");
  } finally {
    done();
  }
});

test("session.deleted forgets the session", async () => {
  const dir = store();
  const s = stub({ hook: "true", store: dir, throttleMs: 0 }, [], [
    { type: "session.created", data: { sessionID: "s9" } },
    { type: "session.deleted", data: { sessionID: "s9" } },
  ]);
  const done = await start(s);
  try {
    await new Promise((resolve) => setTimeout(resolve, 100));
    const known = await s.storage.get("sessions") as string[];
    assert.ok(!known.includes("s9"));
  } finally {
    done();
  }
});
