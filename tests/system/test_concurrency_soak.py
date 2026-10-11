"""Track 5, slice 3 — concurrent writers at volume: nothing lost, index consistent."""

import multiprocessing as mp

import pytest
from agent_memory.core.recall import Recall
from agent_memory.core.store import Store

WRITERS = 4
PER_WRITER = 150


def _write_batch(root: str, worker: int) -> None:
    store = Store(root, agent=f"soak-writer-{worker}")
    for index in range(PER_WRITER):
        store.record(
            type="fact",
            name=f"cw-{worker}-{index:04d}",
            abstract=f"writer {worker} detail-{index} concurrent soak",
            body=f"Notes from writer {worker}, detail {index}.",
        )


@pytest.mark.stress
def test_concurrent_writers_at_volume_lose_nothing(tmp_path):
    root = tmp_path / "store"
    Store(root).init()
    context = mp.get_context("spawn")
    workers = [
        context.Process(target=_write_batch, args=(str(root), worker))
        for worker in range(WRITERS)
    ]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join(300)
    assert [worker.exitcode for worker in workers] == [0] * WRITERS

    store = Store(root)
    store.sync_index()
    names = {record.name for record in store.records()}
    expected = {f"cw-{w}-{i:04d}" for w in range(WRITERS) for i in range(PER_WRITER)}
    assert expected <= names, f"lost {len(expected - names)} records"

    for worker in (0, WRITERS - 1):
        hits = Recall(store).recall(
            f"writer {worker} detail-0 concurrent soak", limit=10, log=False
        )
        assert f"cw-{worker}-0000" in {hit.name for hit in hits}
