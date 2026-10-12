# UI notes (brainstorm, 2026-10-12)

Working notes for the future agent-memory UI (`~/Projects/agent-memory-ui`).
Competitive research: AEndrix03/Graft, trailhq/Graft, tickernelz/opencode-mem.

## Why a UI

The system works without one; a UI is justified only for human workflows:
review sleep proposals, inspect what agents remembered, debug retrieval.
Positioning for other agent-memory users: open store + human-in-the-loop
governance is the differentiator no competitor shows.

## Screens worth building (priority order undecided)

- **Timeline: raw message → memory → recall** — our trace pointers
  (`sessions/<id>#<start>-<end>`) + provenance beat opencode-mem's
  memory↔prompt timeline; competitors' data models cannot show this.
- **Proposals console** — sleep T1 review with diff, evidence, accept/refuse;
  candidates keep deterministic ids across passes. The one place a person is
  mandatory; graft has no equivalent (agent self-audits).
- **Retrieval debugger** — needs `recall --explain` first (see TODO.md);
  per-signal score breakdown, gates, anchors.
- **Store explorer** — tree by type/group, levels (abstract → outline →
  full), links graph, supersede chains.
- **Status dashboard** — needs `mem status` first (see TODO.md): store
  health, pending proposals, distillation backlog.

## Borrow from competitors

- REST API layer over `mem --json`; UI is just a client (opencode-mem does
  this: `POST /api/memories`, `/api/stats`).
- Auto-start on a fixed port, loopback by default, HTTP basic auth when
  bound beyond loopback (opencode-mem).
- Scope switcher: this project vs all projects (opencode-mem `defaultScope`;
  same need as named profiles in TODO.md).
- `graft viz` as the reference for a graph viewer over markdown nodes:
  local server + `--export` to a self-contained HTML.

## Do not copy

- DB as only source of truth (opencode-mem): no grep, no git, shard-by-path
  orphans on repo move. Our UI must be able to show "what is really on disk".
- Injecting all relevant memory into every prompt (opencode-mem): context
  cost; L0 path list stays better.
- Single-shot capture without archived evidence (opencode-mem): "missed"
  must never mean "lost".
- Graft's silent agent self-audit, title-only gate, stale not affecting
  reads: we keep T1 human confirmation and `invalid_at` semantics.
