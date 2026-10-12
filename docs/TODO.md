# Follow-ups

## Read-path hardening follow-up

- `Store.records()` skips undecodable truth files while diagnostics report them;
  pick one rule (surface, skip, or fail loud) for both paths.

## Sleep-commit scope follow-up

- Sleep versions the whole store root (`git add -A`), including raw archived
  transcripts that may hold secrets or PII. Decide: scope the commit to truth
  files, reports and ledger, or scrub credential-shaped content at archive time.
  Until then, docs state that any store repository is sensitive.


## Executor follow-ups

- Replace the host-CLI reasoner with an executor-owned agent loop: native tool use, a
  persisted per-run trace (messages, tool calls, operations, usage), explicit prompt caching,
  a context provider per job, and a durable job queue in place of the fire-and-forget launch.
  The host CLI stays the zero-key fallback.
- Boundary distillation through the host CLI takes 80–100 s per boundary on Haiku (three
  negotiation rounds, one cold process each); measure again once the executor loop lands.
- Verify the Codex dialect end to end, including the one-time hook trust review; it is
  covered by unit tests only.

## OpenCode host follow-ups

Deferred minor findings from the `feat/opencode-host` review pass; the
fixable ones landed, one residual stays documented.

- Positional watermark versus shape-shifting history: if a message's
  extracted text changes shape between reads, positions shift and items are
  missed or duplicated with no content check. No cheap fix — a content-aware
  watermark is a core change. Revisit if observed in traces.
- Store-side backfill sweep: startup backfill only recovers sessions OpenCode
  can still reach through the plugin; a session born, killed, and never
  reopened stays unarchived until then. Narrow the residual gap with a sweep
  that runs on any `mem` start (or distill): walk `archive/sessions/` for
  open watermark pointers whose session history is reachable and archive the
  remainder, host events not required.

## Retrieval follow-ups

Ideas borrowed from a comparison with AEndrix03/Graft (2026-10); keep the
governance invariants that Graft lacks.

- `recall --explain`: expose the per-signal breakdown behind the combined
  score (`relevance * weight * recency` in `core/recall.py`), plus BM25 vs
  vector contribution when fusion is on. Today `--json` carries one opaque
  number; the breakdown is also the data an external debugger needs.
- Confidence gate on recall: label the answer "weak — reformulate the
  query" when the top candidate is far from the request. Build the gate over
  abstract + body, not title only — the failure mode that makes Graft's gate
  miss answers living in the body.

## Manage follow-ups

- Maintenance candidate taxonomy in sleep reports: enumerate the kinds of
  problems the pass looks for (near-duplicate, possible supersession,
  contradiction, isolated low-value, link fragmentation, …) with
  deterministic candidate ids, so a candidate stays stable across passes and
  a decision binds to the same entity.
- Link proposals: when sleep finds memories that look related, file a T1
  proposal to add the `links` edge instead of writing it silently. Keeps the
  explicit-links commitment and the human-in-the-loop governance.

## CLI follow-ups

- Lightweight `mem status`: one cheap call returning store size, index
  health, pending-proposal count, distillation backlog size. Distinct from
  `doctor`, which performs live reasoner requests and stays heavyweight.
- Named profiles: first-class store profiles (`work`, `personal`,
  project-scoped) selectable by name instead of only exporting an absolute
  `AGENT_MEMORY_STORE` path per shell.

## Muse Code follow-ups

- Run the isolated Muse shell, lifecycle hook, and stdio MCP sandbox preflight on an installed,
  authenticated Muse build, then record the observed compatibility result.
- Run Muse-to-Muse, Muse-to-Codex, and Codex-to-Muse portability smoke before the full four-host
  matrix.
- Map `MUSE_SESSION_ID` into shared MCP source context only if provenance can accept it without a
  Muse-specific Store field.
- Validate the isolated root-session fixture against an exported log from the supported Muse
  version before treating raw-log fallback as release-ready.
