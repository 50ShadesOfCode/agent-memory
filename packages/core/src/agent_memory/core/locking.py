"""Pipeline-level serialization. Every writer passes through one advisory lock."""

from __future__ import annotations

import contextlib
import fcntl
import threading
import time
from collections.abc import Iterator

from .errors import LockTimeoutError
from .paths import StoreLayout

_held = threading.local()


@contextlib.contextmanager
def store_lock(layout: StoreLayout) -> Iterator[None]:
    """Re-entrant in the holding thread: nested writers share the outer hold."""
    if getattr(_held, "depth", 0):
        yield
        return
    layout.state_dir.mkdir(parents=True, exist_ok=True)
    timeout = layout.config.storage.lock_timeout_seconds
    poll = layout.config.storage.lock_poll_seconds
    deadline = time.monotonic() + timeout
    with layout.lock_file.open("a+", encoding="utf-8") as handle:
        while True:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise LockTimeoutError(f"store lock busy for {timeout}s") from None
                time.sleep(poll)
        _held.depth = 1
        try:
            yield
        finally:
            _held.depth = 0
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
