# Benchmark and experiment design

Five tracks, ordered by cost. Each states its question, arms, metric, scale,
cost, and what counts as done. Offline tracks are deterministic and CI-able;
live tracks report exposure alongside scores, and stop when the pilot does
not exercise the intended paths.

## 1. Offline recall benchmark

Question: does recall return the right memories, and how fast.
Corpus: ~200 seeded memories (English and Russian, mixed types) with a fixed
query set (~120: keywords, paraphrases, translations), each query mapped to
its expected memory.
Metric: Recall@1/@5, latency p50/p99 per query.
Arms: BM25 baseline; optional vector fusion where enabled.
Scale: seconds, offline, no models. A fast subset runs in CI, the full set
locally.
Done: documented baseline numbers plus a regression gate (no drop beyond
the pinned threshold).

## 2. Scaled read pilot

Question: does the memory-first reading policy change answers, with proof
the agent used the read path.
Arms: full store vs empty store (plus skill vs bare instruction if cheap).
Episodes: 30–50 template-generated practical questions, fixed prompt,
fact-graded (markers are anti-guessing evidence only).
Metric: accuracy delta plus exposure rate from the store access log
(recalls with hits, reads). Report both; a score without exposure
means nothing.
Scale/cost: 1–2 hours of a free-tier host model.
Done: honest read numbers that justify — or cancel — scaling to track 4.

## 3. Write-strategy comparison

Question: which write policy yields better answers under identical
recall (recall held fixed, so deltas attribute to Write only).
Arms: boundary distillation vs manual agent record.
Shape: multi-session buildup phase, then exam questions with markers.
Metric: answer accuracy.
Scale/cost: tens of runs; reasoning may need paid models.
Done: an attributable answer to what drives improvement, write or read.

## 4. Full harness matrix

Question: end-to-end standing on a standard probe.
Shape: the stock `mem-exp run` — LongMemEval-S, 120 episodes,
host × judge matrix with calibration.
Gate: tracks 1–3 must show something worth scaling.
Scale/cost: days and costly models (`ALLOW_COSTLY`).
Done: a result that follows the repo's experiment protocol.

## 5. Stress and soak

Question: does growth break correctness or budgets.
Shape: 10k scripted memories; record throughput, recall p99 versus size,
index rebuild time, correctness under concurrent writers.
Scale/cost: offline, no models.
Done: latency budgets plus confidence that scale does not corrupt.

Measured 2026-10-11 (after the touched-files projection fix):
single-write cost flat across sizes, recall p99 4.7 / 18.2 / 34.1 ms at
1k / 5k / 10k, full rebuild of 10k in 23.2 s, 4 parallel writers x 150
records with zero loss.
