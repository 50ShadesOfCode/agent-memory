# Experiment protocol

An experiment result must be reproducible, attributable and honest about its
limits. Every run leaves behind episodes, transcripts, a machine-readable report
and notes stating what the numbers do and do not show.

## What counts as a result

- Recall is held fixed across write experiments, so score differences attribute
  to the write arm alone.
- Grading is identical across arms. Markers are anti-guessing evidence only;
  answers are graded on facts, with paraphrase tolerance.
- Live arms report exposure from the access log alongside accuracy. A score
  without exposure proves nothing about the path under test.
- Scores stay attached to the reading policy and corpus that produced them.

## Instrument rules

- Prompts and episodes are generated deterministically from templates with
  planted markers, never hand-written per episode.
- Free-model runs tolerate provider quota failures by rerunning after cooldown
  and patching the report; a quota error is an instrument failure, not a result.
- Known methodology gaps (empty-store recalls logging nothing, strict verbatim
  judges) are recorded in the run's notes.

## Cost discipline

Offline deterministic tracks run in CI. Live pilots use free-tier models first
and scale only when the pilot justifies it. Costly matrix runs require an
explicit budget approval.
