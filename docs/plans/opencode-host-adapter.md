# OpenCode host adapter — spec

Date: 2026-10-10. Branch: `feat/opencode-host`.

## Outcome

agent-memory works with OpenCode end to end: memory injection at prompt
time, conversation capture without agent discipline, scheduled
distillation through the host's own CLI, and sleep-time Manage — installed
by one setup command, verified by one doctor command. No OpenCode fork,
no changes to the core write path.

## Why a plugin, not host hooks

OpenCode V2 (verified against `@opencode/plugin` 2.0.26 and the V2 docs)
fires no session-boundary events. The supported interception points are
prompt admission, per-request assembly, tool execution, compaction, and a
server event stream. So the Claude-style boundary model (SessionStart /
Stop / SessionEnd) cannot be ported one to one. The adapter instead maps
the three universal moments onto what OpenCode does offer:

- inject → `prompt` hook appends the MEMORY.md payload on admission;
- pause → periodic capture plus an explicit `/mem-distill` command
  (no exact end-of-turn signal exists);
- evict → `compaction` hook.

Capture and distillation stay separated: capture appends to the archive,
distillation consumes the backlog. A missed run delays knowledge, never
loses it.

## Components

1. **OpenCode plugin (TypeScript).** Lives beside the Python packages and
   ships its own manifest. On setup it registers the prompt hook, the
   compaction hook, the distill command, capture on tool completion, and a
   capture timer as the last resort. Capture layers overlap: tool results
   are archived as they land, admission of a new prompt flushes the
   previous turn's remainder, the timer catches long tool-less stretches,
   and startup backfill covers a close before any flush. On unload the
   plugin disposes all registrations and timers. The plugin shells out to the
   installed `mem` / `mem-hook` binaries by absolute path and never embeds
   reasoning: no LLM client inside, same as the library core.
2. **Python host dialect.** `moments` gains an `opencode` entry mapping the
   plugin's triggers onto inject / pause / evict; `setup` and `doctor` gain
   the host with probe, settings merge, skill install, and optional MCP
   wiring. Executor gains an `opencode` reasoner dialect over headless
   `opencode run`, with the existing endpoint reasoner as fallback.
3. **MCP wiring.** The existing `mem-mcp` stdio server is registered as a
   local MCP server with the store path in its environment. No new tools.

## Behavior contracts

- Startup backfill: on load the plugin compares archived pointers against
  reachable session history and captures the gap, so a closed-before-flush
  session is recovered on next start, not lost.
- Capture is idempotent: re-reading the same session history must not
  duplicate archive entries (pointer per session).
- Capture period is a store config knob, not a hardcoded value.
- The plugin never breaks the host: every hook path catches failures into
  the store log and yields control. A failed distill leaves the backlog
  eligible for retry; the watermark advances only on success.
- One store, all hosts: an OpenCode-written memory is recallable from
  Claude Code / Codex and vice versa (same core calls, same validation).
- Russian queries retrieve Russian records (covered by the `fix/ru-tokenizer`
  change this work builds on).

## Non-goals

- Exact end-of-turn / end-of-session triggers (the host does not emit them).
- New recall ranking, new memory tools, or core write-path changes.
- Vector index (stays optional, unchanged).

## Acceptance

- `mem setup --host opencode` ends READY in a probe project; `mem doctor`
  distinguishes host / store / hook / reasoner failures.
- Prompt hook injects the MEMORY.md line; timer capture archives new
  transcript material; `/mem-distill` produces memories visible to recall.
- Kill-the-app-mid-session drill: close OpenCode before a flush, reopen,
  backfill archives the gap, recall finds it.
- Full Python suite green plus plugin smoke test against a probe store.
