# Changelog

All notable changes to this project are recorded here, newest first.
Entries are added under `Unreleased` with each change and moved under a
version heading on release.

## Unreleased

## 0.3.0 — 2026-10-12

Concurrency and crash-safety hardening from a full-repo audit: WAL with busy
timeout, write-intent replay, lock-free telemetry, duplicate reporting, and
a hardened flat-write gate.

### Fixed

- SQLite runs in WAL mode with a 5 s busy timeout, so parallel readers no
  longer hit `database is locked`; `rebuild` drops WAL siblings with the index.
- Crash safety: a write-intent file replays unprojected files on the next
  projection, provenance writes are atomic (temp + fsync + link), session
  appends heal torn tails and fsync, and crashed merges retry into the base
  name instead of stamping orphans.
- Telemetry (recall/read/feedback access log) no longer takes the writer lock;
  contention is covered by a dedicated test.
- Same-name files across directories are reported as `duplicates` in sync
  reports and `mem inspect` instead of persisting invisibly; hook transcripts
  load only as real `.jsonl` files and hook session/host values pass as
  `--flag=value` so hostile input cannot inject flags.
- Secret scrubbing covers `sk-ant-`, `ghp_`/`ghs_`/`gho_`, `AKIA`, `xoxb-`,
  and PEM private-key headers; CLI input-file failures report as validation
  errors instead of tracebacks.
- Overwrites that change content emit a `record_overwrite` tripwire observation
  (no enforcement yet — evidence first).
- Flaky flat-write gate now measures minimum-of-samples instead of median.

## 0.2.0 — 2026-10-12

## 0.2.0 — 2026-10-12

Benchmark tracks 1–3 and 5 done (track 4 deferred: free-tier quota blocks
the full 120-episode matrix), plus project-review cleanup.

### Added

- Offline recall benchmark: 140 seeded records (English and Russian plus
  confusable families), 140 queries, pinned floors Recall@1 >= 0.90,
  Recall@5 >= 0.95, recall p99 <= 500 ms (`tests/system/test_recall_benchmark.py`).
- Benchmark and experiment design covering five tracks
  (`docs/plans/benchmarks-design.md`).

### Fixed

- Write scaling: a single write no longer rehashes and reparses the whole
  store. Projection after a write covers only touched files (`Indexer.sync_paths`),
  and the injected index renders from indexed rows. Full passes stay on explicit
  sync, rebuild and crash recovery.
- Stress and soak coverage: 10k-record soak (single-write p99, recall p99 vs
  size, full rebuild budget) plus concurrent writers at volume with zero loss
  (`tests/system/test_soak.py`, `tests/system/test_concurrency_soak.py`).
- Project review cleanup: dropped a redundant re-sort in the injected index
  render, typed index-row conversion, and read each truth file once for
  parse plus hash instead of twice.

## 0.1.0 — 2026-10-11

First release under our own roof: OpenCode host support, Unicode recall,
twenty review findings fixed, and eight upstream hardening fixes merged.

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

- Russian and other non-Latin queries retrieve matching records.
- Archive, watermark and pending writes are serialized through a
  re-entrant store lock; watermark marks are written atomically, and a
  corrupt mark file fails loudly naming the file.
- Malformed frontmatter (colon-less lines, duplicate or empty keys),
  non-numeric weights and list-valued custom fields are rejected instead
  of silently coerced; bulk reads skip bad files with a report.
- Truth files are validated on every read path, not just at index time.
- Distill replays skip already-applied specs instead of duplicating memories;
  skipped operations and executor parse faults are reported in the batch.
- Legacy migration backfills missing timestamps instead of emitting null.
- Access-log writes are serialized under the store lock on a short connection.
- Recalled entries and the injected index are marked as data, not instructions.
- Scope spelling is normalized once for the SQL prefilter and the postfilter.
- Feedback is recorded as a usage signal and settled by Manage in batch.
- Host errors are redacted at construction; hook signals degrade safely.
- Hook failure log redacts credential-shaped values via one shared scrubber.
- Supersede revalidates the successor under the same writer lock.
- Capture re-forwards full history on human-rate triggers so a failed pipe
  cannot strand material.
- `gc`, `import` and `decide` refuse executor-owned sessions; `gc` and
  `import` need `--force` without a terminal.
- Moves preserve identity, provenance and links instead of re-recording.
- Interrupted merges resume by adopting their own target; staged temp files
  are reaped on startup.
- Multiline config values round-trip through TOML blocks.
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
