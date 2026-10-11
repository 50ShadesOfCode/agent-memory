# Testing conventions

Tests assert relationships and invariants, never hardcoded values. A feature
shipped without a test is incomplete. Fixtures replace live external services;
hosts that may be absent (Muse binary, model endpoints) skip with a clear
message instead of failing.

## Layers

- `tests/unit/` — per-module invariants, fast, gate every change. CI enforces
  coverage with `--cov-fail-under=85`.
- `tests/system/` — end-to-end behavior: CLI, MCP, concurrency, entry
  equivalence, host integrations, offline benchmarks.
- `tests/redteam/` — adversarial cases (poisoning, malformed input, races)
  proving fail-safe behavior. Release gate.

## Markers

`stress` marks performance budgets, run on release. `redteam` marks
adversarial cases, gate before release. Both run in CI's default suite.

## Shared fixtures

`tests/conftest.py` provides a frozen clock, default config and a temporary
initialized store, so time-dependent assertions compare relationships rather
than clock values.

## Per-file test map

Unit files mirror core modules one to one (store, recall, manage, schema,
placement, locking, triggers, config, frontmatter, watermark, distill replay,
host dialects, regression pins). System files cover CLI, concurrency,
entry-equivalence, fixed-exam, harness, interop, locomo, recall-benchmark,
growth stress, sleep stores, read observability, and each host integration
(OpenCode plugin, Muse integration and preflight, judge hosts, management
entries).
