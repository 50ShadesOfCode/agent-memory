# Write path

Agent writes and Manage rewrites share one validate, hash-diff and reindex pipeline.
Two write paths would diverge truth from projection silently.

Raw sessions and provenance append once and stay. Distillation is a projection of
that raw, not a move: anything the distiller misses remains recoverable from the
archive. Watermarks advance only past settled batches, so a missed trigger costs
latency, never knowledge.

Distillation triggers share one meaning: distill what the archive holds past the
last mark. Forcing a boundary, crossing message or token counts, idling, or an
explicit redistill request all settle the same backlog. Malformed replies and
exhausted negotiation leave the backlog unsettled for a later retry.
