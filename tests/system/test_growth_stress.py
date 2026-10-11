"""Track 5, slice 1 — growth: 10k records keep recall fast and rebuild cheap."""

import time

import pytest
from agent_memory.core.recall import Recall

GROWTH_N = 10_000
BUDGET_RECORD_P99_MS = 500.0
BUDGET_RECALL_P99_MS = 500.0
BUDGET_REBUILD_S = 120.0


def _percentile(values, rank):
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(len(ordered) * rank))]


@pytest.mark.stress
def test_growth_keeps_recall_fast(store):
    record_lat = []
    for index in range(GROWTH_N):
        topic = f"topic-{index % 50}"
        started = time.perf_counter()
        store.record(
            type="fact",
            name=f"growth-{index:05d}",
            abstract=f"{topic} detail-{index} marker-g{index}",
            body=f"Notes on {topic}, detail {index}.",
        )
        record_lat.append((time.perf_counter() - started) * 1000.0)

    assert _percentile(record_lat, 0.99) <= BUDGET_RECORD_P99_MS

    recall_lat = []
    for probe in range(0, GROWTH_N, 100):
        query = f"detail-{probe} topic-{probe % 50}"
        started = time.perf_counter()
        hits = Recall(store).recall(query, limit=5, log=False)
        recall_lat.append((time.perf_counter() - started) * 1000.0)
        assert hits and hits[0].name == f"growth-{probe:05d}"

    assert _percentile(recall_lat, 0.99) <= BUDGET_RECALL_P99_MS

    started = time.perf_counter()
    store.sync_index()
    assert time.perf_counter() - started <= BUDGET_REBUILD_S

    assert len(list(store.records())) == GROWTH_N
