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

Unit files mirror core modules one to one; system files cover one behavior each
(CLI, MCP, concurrency, entry-equivalence, exams, harness, interop, benchmarks,
host integrations). When a module is added, renamed or split, its test file
follows in the same change — the map lives in the tree layout, not in this doc.
