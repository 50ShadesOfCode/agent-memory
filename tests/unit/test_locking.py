"""The advisory lock must always release its file handle, even on error."""

import pathlib
import threading

import pytest
from agent_memory.core import sessions
from agent_memory.core.config import Config
from agent_memory.core.database import Database
from agent_memory.core.errors import MemoryStoreError
from agent_memory.core.locking import store_lock
from agent_memory.core.paths import StoreLayout
from agent_memory.core.watermark import Watermark


def _layout(tmp_path: pathlib.Path) -> StoreLayout:
    config = Config.default()
    layout = StoreLayout(root=tmp_path / "store", config=config)
    layout.ensure()
    return layout


def test_store_lock_acquires_and_releases(tmp_path):
    layout = _layout(tmp_path)
    entered = False
    with store_lock(layout):
        entered = True
    assert entered
    # Lock file exists after first use
    assert layout.lock_file.exists()


def test_connections_use_wal_with_busy_timeout(tmp_path):
    layout = _layout(tmp_path)
    with Database(layout).connect() as connection:
        mode = connection.execute("PRAGMA journal_mode").fetchone()[0]
        timeout = connection.execute("PRAGMA busy_timeout").fetchone()[0]
    assert mode.lower() == "wal"
    assert timeout == 5000


def test_store_lock_creates_state_dir_if_missing(tmp_path):
    config = Config.default()
    layout = StoreLayout(root=tmp_path / "new-store", config=config)
    # state_dir does not exist yet
    assert not layout.state_dir.exists()
    with store_lock(layout):
        pass
    assert layout.state_dir.exists()
    assert layout.lock_file.exists()


def test_store_lock_releases_after_body_error(tmp_path):
    layout = _layout(tmp_path)
    with pytest.raises(RuntimeError, match="body failed"), store_lock(layout):
        raise RuntimeError("body failed")

    with store_lock(layout):
        pass


def test_store_lock_reenters_in_the_same_thread(tmp_path):
    layout = _layout(tmp_path)
    entered = []
    with store_lock(layout):
        entered.append(_reenter(layout))

    assert entered == [True]


def _reenter(layout) -> bool:
    with store_lock(layout):
        return True


def test_concurrent_mark_updates_lose_nothing(tmp_path, clock):
    layout = _layout(tmp_path)
    marks = Watermark(layout, clock)
    rounds = 250

    def advance_all():
        for index in range(rounds):
            marks.advance("s", index)

    def settle_all():
        for index in range(rounds):
            marks.settle("s", index)

    workers = [
        threading.Thread(target=advance_all if turn % 2 == 0 else settle_all)
        for turn in range(8)
    ]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()

    final = marks.read("s")
    assert (final.consumed, final.distilled) == (rounds - 1, rounds - 1)


def test_concurrent_session_appends_keep_contiguous_indices(tmp_path, clock):
    layout = _layout(tmp_path)
    per_thread = 50

    def append_all():
        for _ in range(per_thread):
            sessions.append(layout, "s", ["user: hello"], clock)

    workers = [threading.Thread(target=append_all) for _ in range(8)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()

    messages = sessions.read(layout, "s")
    assert [message.index for message in messages] == list(range(8 * per_thread))


def test_watermark_read_rejects_a_corrupt_file_loudly(tmp_path):
    layout = _layout(tmp_path)
    path = layout.watermarks / "s.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"consumed": 3, BROKEN', encoding="utf-8")

    with pytest.raises(MemoryStoreError, match=r"s\.json"):
        Watermark(layout).read("s")
