# Design

- [Batch write boundaries](batch-write-boundaries.md) defines per-item rejection and
  recovery after a batch write or projection failure.
- [Configuration surface](config-surface.md) defines config as the only home for
  every tunable and its fail-loud validation.
- [Entry adapters](entry-adapters.md) defines the zero-algorithm boundary: CLI, MCP
  and hooks collapse into the same core calls.
- [Executor and reasoning](executor-reasoning.md) defines where model reasoning
  lives, why the core holds no client, and how verdicts fail closed.
- [Experiment and evidence](experiment-evidence.md) defines what licenses an
  experiment result: fixed recall, identical judging, attached exposure.
- [Host adapters](host-adapters.md) defines lifecycle, executor, native-memory, and sandbox
  boundaries for supported agent hosts.
- [Explicit raw evidence reads](raw-evidence-reads.md) defines the boundary between
  an explicit provenance read and the default retrieval policy.
- [Identity and placement](identity-and-placement.md) defines location-free
  identity, schema-derived tree, and the active-or-invalid file atom.
- [Management operation boundaries](management-operation-boundaries.md) defines the
  correction, relationship mutation, automatic duplicate supersession, and automatic
  directory grouping contracts.
- [Projection and cache](projection-and-cache.md) defines indexes as rebuildable
  caches and the rule that write cost must not grow with store size.
- [Read paths](read-paths.md) defines the three read tracks and the rule that reads
  never mutate truth files.
- [Security boundaries](security-boundaries.md) defines fail-safe handling of
  hostile input, secret scrubbing, and memory-as-data.
- [Sleep consolidation](sleep-consolidation.md) defines unattended value-based
  forgetting with per-kind caps and one commit per sleep.
- [Write path](write-path.md) defines the single write pipeline and the boundary
  between append-only raw and distillation as projection.
