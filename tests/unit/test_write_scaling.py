"""Single writes cost the touched files, not the store size."""

import time

FLAT_N_SMALL = 300
FLAT_N_LARGE = 1200
FLAT_RATIO_CEILING = 3.0


def _seed(store, count, prefix):
    for index in range(count):
        store.record(
            type="fact",
            name=f"{prefix}-{index:05d}",
            abstract=f"topic detail-{index}",
            body="x",
        )


def _median_write_ms(store, prefix):
    samples = []
    for index in range(5):
        started = time.perf_counter()
        store.record(
            type="fact",
            name=f"{prefix}-{index}",
            abstract="probe detail",
            body="x",
        )
        samples.append((time.perf_counter() - started) * 1000.0)
    return sorted(samples)[len(samples) // 2]


def test_single_write_cost_is_flat(store):
    _seed(store, FLAT_N_SMALL, "flat-small")
    small = _median_write_ms(store, "probe-small")
    _seed(store, FLAT_N_LARGE - FLAT_N_SMALL, "flat-large")
    large = _median_write_ms(store, "probe-large")
    assert large <= small * FLAT_RATIO_CEILING


def test_memory_index_fresh_after_single_write(store):
    record = store.record(type="fact", name="fresh-fact", abstract="fresh detail", body="x")
    assert record.is_active()
    text = store.layout.memory_index.read_text(encoding="utf-8")
    assert "fresh-fact" in text
