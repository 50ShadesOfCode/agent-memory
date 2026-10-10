# OpenCode host adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `mem setup --host opencode` ends READY: memory injects on prompts, conversation capture survives app kills, distillation reasons through headless `opencode run`.

**Architecture:** Python side adds an `opencode` dialect to the existing `moments` / `setup` / `doctor` / executor tables (a dialect, never a branch — Invariant 8). TypeScript side adds one plugin under `plugins/opencode/` that maps prompt/compaction/tool hooks plus a timer onto those moments and shells out to the installed `mem` binaries by absolute path.

**Tech Stack:** Python 3.12+, TypeScript (OpenCode plugin API, `@opencode/plugin` 2.x), SQLite FTS5 (unchanged), headless `opencode run`.

**Spec:** `docs/plans/opencode-host-adapter.md`

## Global Constraints

- English identifiers, commits, and PR text.
- No LLM client anywhere new: the plugin shells to `mem`/`mem-hook` only; reasoning stays in the executor package through the host CLI.
- Hooks never break the host: every hook path catches failures into the store log and yields control (exit 0 semantics, per `hook_entry.py`).
- Single write path: plugin capture appends to the archive only; memories are written by `mem distill` through validate → hash-diff → reindex.
- Capture is idempotent per session pointer; the distill watermark advances only on success, backlog stays eligible for retry.
- Capture period is a store config knob, not a hardcoded value.
- Nothing lands on `main` except via feature branch + PR; work happens in this branch's worktree.

## Review Focus

- Plugin throws inside a hook and blocks the user's prompt → expect: prompt still admitted, failure in store log (test: hook with failing `mem` binary still admits).
- Same session history read twice archives duplicates → expect: pointer per session, second read appends nothing.
- Distillation launched from the executor's own reasoning session recurses → expect: executor-marked sessions stand down (same `EXECUTOR_ENV_VAR` rule as `hook_entry.main`).
- `AGENT_MEMORY_STORE` unset and no `--store` passed → expect: explicit failure naming the missing store, never a silent default write somewhere surprising.
- `opencode run` fails (no auth, no model) → expect: executor failure reported, archive backlog retained for retry, never treated as completed projection.

---

## File structure

- `docs/design/host-adapters.md` — extend the two-boundaries statement with the OpenCode moment mapping (modify).
- `packages/adapters/src/agent_memory/adapters/moments.py` — add `HOST_OPENCODE` + dialect entry (modify).
- `packages/adapters/src/agent_memory/adapters/setup.py` — settings path, plugin install, MCP wiring for opencode (modify).
- `packages/adapters/src/agent_memory/adapters/doctor.py` — opencode checks: probe, settings, plugin, live reasoner (modify).
- `packages/executor/src/agent_memory/executor/hosts.py` — `HOST_OPENCODE`, `BINARIES` entry, `OpencodeDialect` (modify).
- `plugins/opencode/package.json`, `plugins/opencode/src/index.ts` — the plugin (create).
- `tests/unit/test_opencode_host.py` — dialect/setup/doctor tests (create).
- `tests/system/test_opencode_plugin.py` — setup READY + drill tests against a probe store (create).

---

### Task 1: Design doc + moments dialect

**Files:**
- Modify: `docs/design/host-adapters.md`
- Modify: `packages/adapters/src/agent_memory/adapters/moments.py`
- Test: `tests/unit/test_opencode_host.py`

**Interfaces:**
- Consumes: `moments.DIALECTS`, `MOMENT_INJECT/PAUSE/EVICT` (existing).
- Produces: `HOST_OPENCODE = "opencode"`; `DIALECTS["opencode"]` mapping plugin triggers (`prompt`, `tool`, `timer`, `compaction`) onto moments; `moment_for("opencode", event)` used by Task 3.

- [ ] **Step 1: Write the failing test** — in `tests/unit/test_opencode_host.py`, assert `moment_for("opencode", "prompt") == MOMENT_INJECT`, `moment_for("opencode", "compaction") == MOMENT_EVICT`, and tool/timer events map to `MOMENT_PAUSE`.
- [ ] **Step 2: Run it** — `uv run pytest tests/unit/test_opencode_host.py -q`, expect FAIL (`opencode` unknown → None).
- [ ] **Step 3: Extend `docs/design/host-adapters.md`** — two-boundaries statement plus the OpenCode moment mapping, what/why only.
- [ ] **Step 4: Implement** `HOST_OPENCODE` + `DIALECTS` entry in `moments.py` (data only, no branches).
- [ ] **Step 5: Run tests** — `uv run pytest tests/unit/test_opencode_host.py -q`, expect PASS; then `uv run pytest tests/unit -q`.
- [ ] **Step 6: Commit** — `git add -f docs/design/host-adapters.md docs/plans/opencode-host-adapter.md docs/plans/opencode-host-adapter-plan.md packages/adapters/src/agent_memory/adapters/moments.py tests/unit/test_opencode_host.py` + message `feat(opencode): moments dialect`.

### Task 2: Setup + doctor for opencode

**Files:**
- Modify: `packages/adapters/src/agent_memory/adapters/setup.py`
- Modify: `packages/adapters/src/agent_memory/adapters/doctor.py`
- Test: `tests/unit/test_opencode_host.py` (extend)

**Interfaces:**
- Consumes: `HOST_OPENCODE` from Task 1; existing `install()` / check helpers.
- Produces: `mem setup --host opencode [--mcp]` writes OpenCode project/global config (settings path, plugin entry, optional MCP server with store env); `mem doctor --host opencode` reports host/store/plugin/reasoner layers.

- [ ] **Step 1: Write the failing test** — `install("opencode", settings_path=tmp, store_root=tmp)` writes a config containing the plugin entry and hook command with `--host opencode`; unknown pre-existing plugin entries are preserved; missing store root fails with an error naming the store, never a silent default.
- [ ] **Step 2: Run it** — expect FAIL (unsupported host).
- [ ] **Step 3: Implement** settings path resolution, preserving merge, plugin entry install, MCP server entry (stdio `mem-mcp` + `AGENT_MEMORY_STORE` env) behind `--mcp`.
- [ ] **Step 4: Write the failing doctor test** — missing `opencode` binary reports host-layer failure naming the binary; present binary + valid settings reports READY layers.
- [ ] **Step 5: Run it** — expect FAIL, then implement doctor checks, re-run to PASS.
- [ ] **Step 6: Run** `uv run pytest tests/unit -q && uv run ruff check . && uv run mypy`, expect clean.
- [ ] **Step 7: Commit** — message `feat(opencode): setup and doctor`.

### Task 3: Executor dialect over headless `opencode run`

**Files:**
- Modify: `packages/executor/src/agent_memory/executor/hosts.py`
- Test: `tests/unit/test_host_dialects.py` (auto-covers via parametrize) + opencode-specific assertions in `tests/unit/test_opencode_host.py`

**Interfaces:**
- Consumes: `Dialect.command(...)`, `.stdin(...)`, `.answer(...)`, `.disables_native_memory(...)` contracts.
- Produces: `DIALECTS["opencode"]` whose command starts with the `opencode` binary and delivers the system prompt one way or the other; used by `mem distill --reason-host opencode`.

- [ ] **Step 1: Write the failing test** — `DIALECTS["opencode"].command(...)` starts with `opencode`, routes through `run`, requests JSON output, and disables any native memory layer.
- [ ] **Step 2: Run it** — expect FAIL (no dialect).
- [ ] **Step 3: Implement** `OpencodeDialect` + `BINARIES` entry (pure methods, testable offline like the others).
- [ ] **Step 4: Run** `uv run pytest tests/unit/test_host_dialects.py tests/unit/test_opencode_host.py -q`, expect PASS (parametrized invariants hold for the new dialect too).
- [ ] **Step 5: Commit** — message `feat(opencode): executor dialect`.

### Task 4: TypeScript plugin (capture + inject + distill command)

**Files:**
- Create: `plugins/opencode/package.json`, `plugins/opencode/src/index.ts`
- Test: `tests/system/test_opencode_plugin.py` (probe-store smoke: plugin loads, prompt hook injects, tool hook archives, backfill covers a gap)

**Interfaces:**
- Consumes: `moment_for("opencode", ...)` (Task 1), absolute `mem`/`mem-hook` paths from setup (Task 2), store config knob for the capture period.
- Produces: registered prompt hook (inject + flush previous turn), tool hook (archive new items), timer (catch-all capture), compaction hook (evict), `/mem-distill` command, startup backfill; all failures to store log, host never blocked.

- [ ] **Step 1: Write the failing system test** — with a probe store and a fake session history, run the plugin's capture routine: new items archived once, re-run archives nothing; backfill archives a pre-kill gap.
- [ ] **Step 2: Run it** — expect FAIL (no plugin).
- [ ] **Step 3: Implement** `plugins/opencode/src/index.ts` (hooks + timer + command + backfill + dispose on unload). Distill launch marks the child environment as executor-owned so its session stands down like `hook_entry.main` requires.
- [ ] **Step 4: Host-never-blocked test** — point the plugin at a failing `mem` binary, fire the prompt hook, assert the prompt is still admitted and the failure lands in the store log.
- [ ] **Step 5: Typecheck + test** — plugin typecheck plus `uv run pytest tests/system/test_opencode_plugin.py -q`, expect PASS.
- [ ] **Step 6: Commit** — message `feat(opencode): capture plugin`.

### Task 5: End-to-end drills + green suite

**Files:**
- Test: `tests/system/test_opencode_plugin.py` (extend)
- Modify: `docs/design/host-adapters.md` if drills reveal a boundary change

**Interfaces:**
- Consumes: Tasks 1–4.
- Produces: green CI on the branch; kill-mid-session drill evidence; interop proof (opencode-written memory recalled via core recall).

- [ ] **Step 1: Kill drill** — seed probe store, simulate close-before-flush, reopen/backfill, assert recall finds the material.
- [ ] **Step 2: Interop check** — record via opencode path, recall via plain core `Recall`; assert the hit.
- [ ] **Step 3: Full verify** — `uv run pytest -q && uv run ruff check . && uv run mypy`, expect 748+ PASS, clean.
- [ ] **Step 4: Live CLI verify** — `mem setup --host opencode` in a probe project ends READY; `mem doctor --host opencode` passes layers.
- [ ] **Step 5: Commit** — message `test(opencode): end-to-end drills`; open PR (owner merges, agent never merges to main).
