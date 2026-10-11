# Experiment and evidence

Experiments are their own layer: the harness drives hosts, holds recall fixed across
write experiments, and grades with a judge identical across arms, so score
differences attribute to the arm under test and nothing else.

Scores stay attached to the reading policy and corpus that produced them; a number
without its exposure and configuration is not a result. The protocol that decides what
counts as a result — deterministic offline tracks, exposure alongside live accuracy,
read-only observation — lives in the experiment protocol doc; this file states only the
boundary it enforces.
