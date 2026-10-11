# Changelog

All notable changes to this project are recorded here, newest first.
Entries are added under `Unreleased` with each change and moved under a
version heading on release.

## Unreleased

### Added

- OpenCode host support: memory plugin (prompt injection, layered capture
  on finished turns, tool results, timer and compaction, `/mem-distill`
  command, startup backfill), `mem setup --host opencode` and `mem doctor`
  integration, and a headless `opencode run` executor dialect.
- Store configuration knob `write.capture_period_seconds` (default 600),
  projected into the OpenCode plugin options at setup time.
- Regression tests for invalid-truth cache eviction, provenance
  append-only, blank session messages, Unicode JSONL framing, incomplete
  distillation, MCP framing and argument types, and capture serialization.

### Fixed

- Russian queries retrieve Russian records (Cyrillic letters kept in the
  FTS query tokenizer).
- Archive, watermark and pending writes are serialized through a
  re-entrant store lock; watermark marks are written atomically, and a
  corrupt mark file fails loudly naming the file.
- Empty executor answers fail at dialect level with retries instead of
  passing silently.
- The OpenCode capture plugin advances its pointer only on successful
  hook delivery, stands down for executor sessions, and never blocks
  prompt admission.
- MCP stdio server survives malformed request frames with JSON-RPC errors.
- MCP dispatch validates declared argument types (recall limits must be
  positive integers) before core calls.
- Archive files keep a numeric suffix on filename collision instead of
  overwriting provenance.
- Blank session messages are retained so provenance ranges stay bound.
- JSONL readers split on the encoded newline only, preserving Unicode
  separators inside values.
- Exhausted executor negotiation reports validation failure and keeps the
  archived backlog eligible for retry.
- Capture holds the store writer lock across increment selection, append
  and watermark advancement.
- CI installs the OpenCode plugin node dependencies; node tests run by
  explicit file list for older runners.

### Docs

- README: OpenCode setup and behavior, plugin node prerequisites.
- Agent skill: OpenCode setup command and `/mem-distill` guidance.
- Design docs: OpenCode moment mapping, full-history capture contract,
  per-fix boundary notes.
- Deferred follow-ups are tracked in `docs/TODO.md`.
