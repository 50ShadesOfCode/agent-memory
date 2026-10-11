# Projection and cache

Markdown files are the single source of truth; every index is a rebuildable cache.
Deleting the index loses no knowledge: a rebuild re-derives it from truth files by
content hash, and an external edit becomes visible on the next sync or rebuild.

A write projects only the files it touched; full passes belong to explicit sync,
rebuild and crash recovery, which remain the discovery path for changes made outside
the store. Cost must not grow with store size, or the store stops being writable.

The injected index is a projection too. It carries stable high-weight residents under
a hard byte budget, never query-sensitive picks; relevance-ranked entries stay
reachable through recall and context instead of competing for the same slots.
