# Vault phase 2 (inbox + adopt) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A human drops Obsidian notes into `inbox/`; `mem adopt` validates, places and moves them into the tree, and `mem inspect` reports projection dropouts with reasons.

**Architecture:** Adopt reuses the single write path literally — parse inbox file to a spec, call `Store.record(**spec)`, unlink the inbox file only on success. Invalid files never move; reasons surface per file. Reserved dirnames (`inbox/`, attachments, `.obsidian/`) live in config and are excluded from truth.

**Tech Stack:** Python 3.12, stdlib only (pathlib), existing core/CLI patterns.

**Spec:** `/Users/kakty/.opencode/plan/vault-as-store.md` (phase 2), repo rules in `AGENTS.md` (docs-first, TDD, single write path, config holds every knob).

## Global Constraints

- Python floor 3.12, ruff line-length 100, mypy clean.
- No new third-party dependencies.
- English in code identifiers, commits, and CLI copy.
- Full suite + ruff + mypy green at every task; commit at every green point.

## Review Focus

- Name collision: inbox note whose name matches an existing active memory — must reject with reason, never overwrite.
- No-frontmatter file in inbox — stays put, reason names the missing block.
- Adopt while another writer holds the store lock — must serialize, never corrupt.
- Dropout repair round-trip: file listed as dropout, human fixes, re-adopt succeeds.
- `.obsidian/` workspace files and attachments — never indexed, never listed as dropouts.

---

### Task 1: Design-doc boundary for inbox/adopt

**Files:**
- Modify: `docs/design/identity-and-placement.md` (adopt/placement boundary)
- Modify: `docs/design/config-surface.md` (new `inbox_dirname`, `attachments_dirname` knobs)
- Modify: `docs/design/index.md` (only if a new doc is added — prefer not to)

**Interfaces:**
- Consumes: vault plan phase 2 (validate → place → move; invalid stays; dropout report).
- Produces: the normative sentences Tasks 2–5 argue from (quote them in code-review).

- [ ] **Step 1: Write the doc additions**

Add to `identity-and-placement.md`: inbox is outside truth; adopt derives placement from schema key via `placement.resolve` exactly as `record` does; the inbox file is unlinked only after the record persists; rename-equals-new-memory (name is identity). Add to `config-surface.md`: `storage.inbox_dirname` (default `"inbox"`), `storage.attachments_dirname` (default `"attachments"`), both reserved and excluded from truth.

- [ ] **Step 2: Self-check against AGENTS.md doc rules**

No how (no code, no paths to functions, no literals beyond the two dirname defaults which are config values); shorter than before unless a new idea was added.

- [ ] **Step 3: Commit**

```bash
git add docs/design/identity-and-placement.md docs/design/config-surface.md
git commit -m "docs: inbox/adopt boundary for vault phase 2"
```

### Task 2: Reserved inbox/attachments dirnames in config and layout

**Files:**
- Modify: `packages/core/src/agent_memory/core/config.py` (storage section near `pending_dirname`, line ~127)
- Modify: `packages/core/src/agent_memory/core/paths.py` (`reserved_dirnames()`, line ~76)
- Test: `tests/unit/test_config.py` (extend), `tests/unit/test_store_layout.py` (or wherever `truth_files` exclusion is pinned — grep first)

**Interfaces:**
- Consumes: Task 1 normative sentences.
- Produces: `config.storage.inbox_dirname`, `config.storage.attachments_dirname`; `StoreLayout.reserved_dirnames()` includes both; `truth_files()` skips them.

- [ ] **Step 1: Write the failing tests**

```python
def test_inbox_and_attachments_are_reserved(tmp_path):
    layout = StoreLayout(tmp_path)  # use the repo's existing layout fixture style
    assert "inbox" in layout.reserved_dirnames()
    assert "attachments" in layout.reserved_dirnames()

def test_truth_files_skips_reserved(store):
    (store.root / "inbox" / "note.md").parent.mkdir(parents=True, exist_ok=True)
    (store.root / "inbox" / "note.md").write_text("x", encoding="utf-8")
    assert all("inbox" not in p.parts for p in store.layout.truth_files())
```

Match the existing fixture names in those test files (grep `def store` / layout fixtures first).

- [ ] **Step 2: Run to verify they fail**

Run: `uv run pytest tests/unit/test_config.py tests/unit/test_store_layout.py -q`
Expected: FAIL (unknown knobs / files not skipped)

- [ ] **Step 3: Implement**

Add `inbox_dirname: str = "inbox"` and `attachments_dirname: str = "attachments"` to the storage config dataclass; include both in `reserved_dirnames()` (also keep `.obsidian` out of truth: add `".obsidian"` to the reserved set — hardcoded service name, not a knob).

- [ ] **Step 4: Run tests to verify they pass**

Run: same as Step 2
Expected: PASS, plus `uv run ruff check .` and `uv run mypy` clean

- [ ] **Step 5: Commit**

```bash
git add packages/core/src/agent_memory/core/config.py packages/core/src/agent_memory/core/paths.py tests/unit/test_config.py tests/unit/test_store_layout.py
git commit -m "feat(core): reserve inbox and attachments dirnames"
```

### Task 3: Core adopt — parse, record, unlink

**Files:**
- Create: `packages/core/src/agent_memory/core/adopt.py`
- Test: `tests/system/test_adopt.py` (new; CLI-level JSON tests live in `tests/system/test_cli.py` style — grep first, put core tests here)

**Interfaces:**
- Consumes: `Store.record(**spec)` (`store.py:122`), `MemoryRecord.from_text` (`record.py:87`), `record.validate` (`record.py:128`).
- Produces: `adopt_files(store: Store) -> AdoptReport`; `AdoptReport.adopted: list[str]` (memory names), `AdoptReport.rejected: list[AdoptRejection]` with `AdoptRejection(path: str, errors: list[str])`.

- [ ] **Step 1: Write the failing tests**

```python
def test_adopt_valid_note_is_recorded_and_unlinked(store):
    (store.layout.root / "inbox").mkdir(exist_ok=True)
    (store.layout.root / "inbox" / "freeze.md").write_text(
        "---\nname: freeze-note\ntype: fact\nabstract: freeze Fridays\n---\n\nNo deploys.\n",
        encoding="utf-8",
    )
    report = adopt_files(store)
    assert report.adopted == ["freeze-note"]
    assert not (store.layout.root / "inbox" / "freeze.md").exists()
    assert store.read("freeze-note").text == "No deploys.\n"

def test_adopt_invalid_note_stays_put_with_errors(store):
    (store.layout.root / "inbox").mkdir(exist_ok=True)
    (store.layout.root / "inbox" / "bad.md").write_text("no frontmatter here\n", encoding="utf-8")
    report = adopt_files(store)
    assert report.adopted == []
    assert len(report.rejected) == 1 and report.rejected[0].errors
    assert (store.layout.root / "inbox" / "bad.md").exists()

def test_adopt_name_collision_rejects(store):
    store.record(type="fact", name="taken", abstract="taken", body="x")
    ...same inbox file with name: taken...
    report = adopt_files(store)
    assert report.adopted == [] and report.rejected
    assert (store.layout.root / "inbox" / "taken.md").exists()
```

Check the `store` fixture name in `tests/conftest.py` / `tests/system/` before writing (adapt if different).

- [ ] **Step 2: Run to verify they fail**

Run: `uv run pytest tests/system/test_adopt.py -q`
Expected: FAIL with "adopt not defined" (import error)

- [ ] **Step 3: Implement `adopt_files(store: Store) -> AdoptReport` in `adopt.py`**

For each `*.md` directly in `<root>/<inbox_dirname>/` (sorted, non-recursive): parse with `MemoryRecord.from_text`; on `ValidationError` record rejection and continue (file stays). Build a spec from the parsed record's fields (`type`, `name`, `abstract`, `body`, plus `links`, `project`, `subject`, `user`, `source`, `topic`, `category` when present) and call `store.record(**spec)`; on `ValidationError` (collision, schema) record rejection and continue. Unlink the inbox file only after `record` returns. Never catch broad `Exception` — unexpected errors propagate.

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/system/test_adopt.py -q`
Expected: PASS, plus ruff + mypy clean

- [ ] **Step 5: Commit**

```bash
git add packages/core/src/agent_memory/core/adopt.py tests/system/test_adopt.py
git commit -m "feat(core): adopt inbox notes through the single write path"
```

### Task 4: CLI `mem adopt`

**Files:**
- Modify: `packages/cli/src/agent_memory/cli/main.py` (subparser near `import`, line ~199; handler near `_import`, line ~493)
- Test: extend `tests/system/test_adopt.py` with a CLI JSON test

**Interfaces:**
- Consumes: `adopt_files` from Task 3.
- Produces: `mem adopt [--json]` printing `{"adopted": [...], "rejected": [{"path": ..., "errors": [...]}]}`; exit code 0 even with rejections (rejections are data, not failure).

- [ ] **Step 1: Write the failing test**

```python
def test_cli_adopt_json(store, capsys):
    ...write valid + invalid inbox files...
    assert main(["--store", str(store.root), "adopt", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["adopted"] == ["freeze-note"]
    assert payload["rejected"][0]["path"].endswith("bad.md")
```

Follow the existing `main([...])` + `capsys` pattern from `test_cli.py` (check exact store-arg spelling first).

- [ ] **Step 2: Run to verify it fails**

Run: `uv run pytest tests/system/test_adopt.py::test_cli_adopt_json -q`
Expected: FAIL (argparse errors on unknown `adopt`)

- [ ] **Step 3: Implement**

Add `adopt` subparser and `_adopt(store, args)` returning the report dict; wire into the dispatch exactly like `_import`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/system/test_adopt.py tests/system/test_cli.py -q`
Expected: PASS, plus ruff + mypy clean

- [ ] **Step 5: Commit**

```bash
git add packages/cli/src/agent_memory/cli/main.py tests/system/test_adopt.py
git commit -m "feat(cli): mem adopt inbox notes"
```

### Task 5: Dropout report in `mem inspect`

**Files:**
- Modify: `packages/core/src/agent_memory/core/store.py` (add `Store.projection_dropouts()`)
- Modify: `packages/cli/src/agent_memory/cli/main.py` (`_inspect`, line ~466)
- Test: extend `tests/system/test_adopt.py` (dropout-and-return test)

**Interfaces:**
- Consumes: `StoreLayout.truth_files()`, `SearchIndex.rows()`, `Indexer._load`-equivalent validation (`MemoryRecord.from_text` + `record.validate`).
- Produces: `Store.projection_dropouts() -> list[dict]` with `{"path": ..., "reason": ...}`; `mem inspect --json` includes a `dropouts` key.

- [ ] **Step 1: Write the failing test**

```python
def test_dropout_reported_then_repaired(store):
    ...place a truth file with malformed frontmatter directly in the tree...
    dropouts = store.projection_dropouts()
    assert len(dropouts) == 1 and dropouts[0]["reason"]
    ...fix the file, re-sync...
    assert store.projection_dropouts() == []
```

Reasons must name the cause: `"frontmatter: <first error>"`, `"unknown type: <t>"`, `"duplicate name: <n>"` — grep `record.validate` error shapes first and mirror them.

- [ ] **Step 2: Run to verify it fails**

Run: `uv run pytest tests/system/test_adopt.py::test_dropout_reported_then_repaired -q`
Expected: FAIL (no such method)

- [ ] **Step 3: Implement `Store.projection_dropouts()`**

For each file in `truth_files()`: parse + validate; on failure record `{path, reason}`. Then compare indexed names (`SearchIndex.rows()`) against successfully parsed names; any truth file whose name is absent from the index is a dropout with reason `"not indexed"`. Return sorted by path.

- [ ] **Step 4: Surface in `_inspect` and run tests**

Add `"dropouts": store.projection_dropouts()` to the inspect payload. Run: `uv run pytest tests/system/test_adopt.py tests/system/test_cli.py -q`
Expected: PASS, plus ruff + mypy clean

- [ ] **Step 5: Commit**

```bash
git add packages/core/src/agent_memory/core/store.py packages/cli/src/agent_memory/cli/main.py tests/system/test_adopt.py
git commit -m "feat(inspect): report projection dropouts with reasons"
```
