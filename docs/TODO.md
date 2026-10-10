# Follow-ups

## Read policy follow-up

- Evaluate the memory-first reading policy with observed exposure before attributing
  answer changes to bounded Trace or optional Vector candidates.

## Management follow-ups

- Preserve identity and provenance when regrouping menu-based add-only schemas;
  the current move re-enters add-only naming and can replace the source file with
  a renamed record that does not inherit its evidence.
- Revalidate the duplicate keeper under the same writer lock as T0 invalidation; current
  stale-write detection protects only the record being invalidated.
- Decide explicit confirmation and host-level authorization for permanent GC, import and
  cross-store changes; CLI labels alone do not identify a human.
- Decide preimage retention and recovery guarantees for split and in-place correction,
  including stores outside Git and multi-file Manage failures.
- Decide whether direct link/unlink delta commands, relation audit history and per-operation
  bounds are needed; current correct replaces the complete list.
- Review recovery of interrupted multi-file operations outside Git-backed stores.

## Executor follow-ups

- Replace the host-CLI reasoner with an executor-owned agent loop: native tool use, a
  persisted per-run trace (messages, tool calls, operations, usage), explicit prompt caching,
  a context provider per job, and a durable job queue in place of the fire-and-forget launch.
  The host CLI stays the zero-key fallback.
- Boundary distillation through the host CLI takes 80–100 s per boundary on Haiku (three
  negotiation rounds, one cold process each); measure again once the executor loop lands.
- Verify the Codex dialect end to end, including the one-time hook trust review; it is
  covered by unit tests only.

## OpenCode host follow-ups

Deferred minor findings from the `feat/opencode-host` review pass; none blocks
the adapter, each is a small test-plus-fix when taken.

- Empty-answer exit-0 returns `ok=True` for the opencode dialect and skips
  Host-level retries, unlike codex/muse; safe end to end only because
  `HostReasoner` raises on empty. Add `HOST_OPENCODE` to the empty-answer
  failure tuple in `hosts.py` with a test.
- `disables_native_memory` for opencode is a substring check for `--format`;
  OpenCode ships no native layer, so return `True` unconditionally instead.
- `OpencodeDialect.command` silently ignores `tools_enabled`, `max_turns`
  and `workdir`; harmless while distill runs tool-less, but document the
  limitation — there is no tool-scoping equivalent in `opencode run`.
- Throttle stamps the session before the history read, so a no-op capture
  suppresses a follow-up capture with genuinely new items for up to 5 s;
  move the stamp to after the spawn decision.
- `pipeHook` blocks the awaited prompt path up to the hook self-timeout
  (~20 s worst case); consider async spawn for prompt-admission capture.
- `HOOK_COMMAND` substring matching in setup/doctor can false-positive on
  an unrelated plugin entry mentioning `mem-hook`; match against
  `options.hook` instead.
- Positional watermark versus shape-shifting history: if a message's
  extracted text changes shape between reads, positions shift and items are
  missed or duplicated with no content check; acceptable residual, revisit
  if observed.

## Muse Code follow-ups

- Run the isolated Muse shell, lifecycle hook, and stdio MCP sandbox preflight on an installed,
  authenticated Muse build, then record the observed compatibility result.
- Run Muse-to-Muse, Muse-to-Codex, and Codex-to-Muse portability smoke before the full four-host
  matrix.
- Map `MUSE_SESSION_ID` into shared MCP source context only if provenance can accept it without a
  Muse-specific Store field.
- Validate the isolated root-session fixture against an exported log from the supported Muse
  version before treating raw-log fallback as release-ready.
