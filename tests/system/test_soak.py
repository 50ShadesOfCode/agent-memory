"""Track 5, slice 2 — soak: 10k seeded in chunks, recall p99 vs size, rebuild cheap."""

import time

import pytest
from agent_memory.core.recall import Recall

SOAK_N = 10_000
CHUNK = 500
CHECKPOINTS = (1_000, 5_000, 10_000)
BUDGET_RECALL_P99_MS = 500.0
BUDGET_REBUILD_S = 120.0
PROBES_PER_CHECKPOINT = 20


def _percentile(values, rank):
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(len(ordered) * rank))]


def _seed_chunk(store, start, count):
    specs = [
        {
            "type": "fact",
            "name": f"soak-{start + index:05d}",
            "abstract": (
                f"topic-{(start + index) % 50} detail-{start + index} "
                f"marker-s{start + index}"
            ),
            "body": f"Notes on topic, detail {start + index}.",
        }
        for index in range(count)
    ]
    result = store.record_many(specs)
    assert not result.rejected
    assert len(result.written) == count


def _probe(store, seeded):
    latencies = []
    for probe in range(0, seeded, max(1, seeded // PROBES_PER_CHECKPOINT))[:PROBES_PER_CHECKPOINT]:
        query = f"detail-{probe} topic-{probe % 50}"
        started = time.perf_counter()
        hits = Recall(store).recall(query, limit=5, log=False)
        latencies.append((time.perf_counter() - started) * 1000.0)
        assert hits and hits[0].name == f"soak-{probe:05d}", query
    return _percentile(latencies, 0.99)


@pytest.mark.stress
def test_soak_recall_p99_vs_size_and_rebuild(store):
    p99_by_size = {}
    seeded = 0
    while seeded < SOAK_N:
        _seed_chunk(store, seeded, CHUNK)
        seeded += CHUNK
        if seeded in CHECKPOINTS:
            p99 = _probe(store, seeded)
            p99_by_size[seeded] = round(p99, 1)
            assert p99 <= BUDGET_RECALL_P99_MS, f"recall p99 at n={seeded}: {p99:.1f}ms"

    assert len(list(store.records())) == SOAK_N

    sample = [f"detail-{i} topic-{i % 50}" for i in (0, 1234, 5678, 9999)]
    before = {
        query: [hit.name for hit in Recall(store).recall(query, limit=3, log=False)]
        for query in sample
    }

    started = time.perf_counter()
    report = store.rebuild_index()
    elapsed = time.perf_counter() - started
    assert elapsed <= BUDGET_REBUILD_S, f"rebuild 10k took {elapsed:.1f}s"
    assert len(report.reindexed) == SOAK_N

    after = {
        query: [hit.name for hit in Recall(store).recall(query, limit=3, log=False)]
        for query in sample
    }
    assert after == before
    print(f"\nrecall p99 vs size (ms): {p99_by_size}, rebuild 10k: {elapsed:.1f}s")
