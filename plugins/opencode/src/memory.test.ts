import test from "node:test";
import assert from "node:assert/strict";
import { buildHookEvent, firstShellWord, toHistoryItems, unseenItems, type HistoryItem } from "./memory.ts";

const history: HistoryItem[] = [
  { id: "m1", text: "user: hello" },
  { id: "m2", text: "assistant: hi" },
  { id: "m3", text: "user: again" },
];

test("first run archives everything, re-run archives nothing", () => {
  const first = unseenItems(history, null);
  assert.deepEqual(
    first.items.map((item) => item.id),
    ["m1", "m2", "m3"],
  );
  const second = unseenItems(history, first.pointer);
  assert.deepEqual(second.items, []);
  assert.equal(second.pointer, first.pointer);
});

test("unknown pointer treats the whole history as the gap", () => {
  const { items, pointer } = unseenItems(history, "gone-before-the-kill");
  assert.deepEqual(
    items.map((item) => item.id),
    ["m1", "m2", "m3"],
  );
  assert.equal(pointer, "m3");
});

test("empty history keeps the pointer", () => {
  const { items, pointer } = unseenItems([], "m1");
  assert.deepEqual(items, []);
  assert.equal(pointer, "m1");
});

test("hook event carries session, trigger, and texts", () => {
  const event = buildHookEvent("ses_1", "tool", history.slice(0, 2));
  assert.deepEqual(event, {
    session_id: "ses_1",
    event: "tool",
    items: ["user: hello", "assistant: hi"],
  });
});

test("history extraction reads text parts and skips the silent", () => {
  const items = toHistoryItems([
    { messageID: "m1", role: "user", parts: [{ type: "text", text: "hello" }] },
    { messageID: "m2", role: "assistant", content: "hi" },
    { messageID: "m3", role: "assistant", parts: [{ type: "tool", name: "read" }] },
  ]);
  assert.deepEqual(items, [
    { id: "m1", text: "user: hello" },
    { id: "m2", text: "assistant: hi" },
  ]);
});

test("first shell word respects quotes", () => {
  assert.equal(firstShellWord("/bin/mem-hook --host opencode"), "/bin/mem-hook");
  assert.equal(firstShellWord("'/sp ace/mem-hook' --host opencode"), "/sp ace/mem-hook");
});
