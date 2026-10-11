# Write scaling fix

## Problem

Single `record()` cost grows linearly with store size (11 ms at n=100,
194 ms at n=1600): every write runs two full-store passes — `indexer.sync()`
rehashes all truth files, and `memory_md.write(records())` reparses them.
The 10k stress slice cannot run at this cost (~100 min extrapolated).

## Contract change

- After a Store write, projection covers only files the write touched
  (written target, moved source, invalidated predecessor), resolved through
  the manifest by path. `sync_index`/`rebuild_index` keep the full pass for
  out-of-band changes and explicit repair.
- MEMORY.md after a write reflects the touched records against the injected
  projection (search-index rows), not a reparse of all truth files. Byte
  budget and weight-floor rules unchanged; full render stays on rebuild/sync.
- Crash recovery unchanged: snapshot touched files, restore, reproject touched.

## Units

1. Design doc update (batch-write-boundaries: touched-file projection).
2. Failing tests: single-write cost flat across sizes; MEMORY.md fresh after
   write/move/supersede/merge without full scan; out-of-band file still
   discovered only by sync/rebuild.
3. Implementation: manifest keyed by path; `Indexer.sync_paths`; memory_md
   render from touched records + indexed rows.
4. Verify: stress slice green, full suite + ruff + mypy, push.

## Status

Implemented: `Indexer.sync_paths`, `memory_md` entries,
`Store._project_paths` on all write paths. Scaling tests green.

## Risks

- MEMORY.md staleness for untouched weight changes (feedback only touches
  the access log, not truth — safe).
- External file edits invisible until sync (already the documented semantic).
