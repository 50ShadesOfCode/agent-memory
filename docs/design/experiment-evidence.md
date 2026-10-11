# Experiment and evidence

Experiments are their own layer: the harness drives hosts, holds recall fixed across
write experiments, and grades with a judge identical across arms, so score
differences attribute to the arm under test and nothing else.

Scores stay attached to the reading policy and corpus that produced them; a number
without its exposure and configuration is not a result. Offline tracks must be
deterministic and regression-gated; live tracks report exposure from the access log
alongside accuracy, and stop when the run does not exercise the intended paths.

Observation is read-side only and owned by the harness: evidence gathering must not
change the behavior being measured.
