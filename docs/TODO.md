# Follow-ups

## Read policy follow-up

- Evaluate the memory-first reading policy with observed exposure before attributing
  answer changes to bounded Trace or optional Vector candidates.

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

Deferred minor findings from the `feat/opencode-host` review pass; the
fixable ones landed, one residual stays documented.

- Positional watermark versus shape-shifting history: if a message's
  extracted text changes shape between reads, positions shift and items are
  missed or duplicated with no content check. No cheap fix — a content-aware
  watermark is a core change. Revisit if observed in traces.

## Muse Code follow-ups

- Run the isolated Muse shell, lifecycle hook, and stdio MCP sandbox preflight on an installed,
  authenticated Muse build, then record the observed compatibility result.
- Run Muse-to-Muse, Muse-to-Codex, and Codex-to-Muse portability smoke before the full four-host
  matrix.
- Map `MUSE_SESSION_ID` into shared MCP source context only if provenance can accept it without a
  Muse-specific Store field.
- Validate the isolated root-session fixture against an exported log from the supported Muse
  version before treating raw-log fallback as release-ready.
