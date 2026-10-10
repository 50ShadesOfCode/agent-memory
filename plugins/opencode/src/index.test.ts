import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
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

test("failing hook still admits the prompt and advances no pointer", async () => {
  const dir = store();
  const s = stub(
    { hook: "/nonexistent-mem-hook --host opencode", store: dir, throttleMs: 0 },
    messages(),
  );
  const done = await start(s);
  try {
    await s.handlers["prompt"]({ sessionID: "s1", prompt: { text: "hi", files: [] } });
    assert.equal(s.storage.get("pointer:s1"), undefined);
  } finally {
    done();
  }
});

test("working hook advances the pointer", async () => {
  const dir = store();
  const s = stub({ hook: "true", store: dir, throttleMs: 0 }, messages());
  const done = await start(s);
  try {
    await s.handlers["prompt"]({ sessionID: "s1", prompt: { text: "hi", files: [] } });
    assert.equal(s.storage.get("pointer:s1"), "m1");
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
    await s.handlers["prompt"]({ sessionID: "s1", prompt: { text: "hi", files: [] } });
    assert.equal(s.storage.get("pointer:s1"), undefined);
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
    const event = { sessionID: "s1", prompt: { text: "hi", files: [] as Array<{ uri: string }> } };
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
    const known = s.storage.get("sessions") as string[];
    assert.ok(known.includes("s9"));
  } finally {
    done();
  }
});

test("session.idle captures the finished turn", async () => {
  const dir = store();
  const s = stub({ hook: "true", store: dir, throttleMs: 0 }, messages(), [
    { type: "session.idle", data: { sessionID: "s1" } },
  ]);
  const done = await start(s);
  try {
    await new Promise((resolve) => setTimeout(resolve, 100));
    assert.equal(s.storage.get("pointer:s1"), "m1");
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
    const known = s.storage.get("sessions") as string[];
    assert.ok(!known.includes("s9"));
  } finally {
    done();
  }
});
