# Identity and placement

A schema defines what a memory type is: its slots, its identity key, its placement
group and its write mode. The tree and the identity derive from the type, so the same
thing written by different writers lands in the same file.

Identity is location-free: a kebab-case slug survives a move, so links and provenance
citations keep working. Placement derives deterministically from type, group and key;
system-sourced groups preserve their boundaries while menu-sourced groups may be
clustered and merged.

One file holds knowledge that expires as a whole. A memory is active or invalid,
nothing in between, and invalidation comes only from replacement or deletion —
partial staleness inside a file would poison the whole file.
