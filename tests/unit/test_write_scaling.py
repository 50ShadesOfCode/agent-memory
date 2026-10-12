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


def _min_write_ms(store, prefix):
    samples = []
    for index in range(7):
        started = time.perf_counter()
        store.record(
            type="fact",
            name=f"{prefix}-{index}",
            abstract="probe detail",
            body="x",
        )
        samples.append((time.perf_counter() - started) * 1000.0)
    return min(samples)


def test_single_write_cost_is_flat(store):
    _seed(store, FLAT_N_SMALL, "flat-small")
    small = _min_write_ms(store, "probe-small")
    _seed(store, FLAT_N_LARGE - FLAT_N_SMALL, "flat-large")
    large = _min_write_ms(store, "probe-large")
    assert large <= small * FLAT_RATIO_CEILING


def test_memory_index_fresh_after_single_write(store):
    record = store.record(type="fact", name="fresh-fact", abstract="fresh detail", body="x")
    assert record.is_active()
    text = store.layout.memory_index.read_text(encoding="utf-8")
    assert "fresh-fact" in text


def test_memory_index_fresh_after_move_supersede_merge(store):
    store.record(type="fact", name="move-me", abstract="move me detail", body="x")
    store.record(type="fact", name="old-fact", abstract="old detail", body="x")
    store.record(type="fact", name="new-fact", abstract="new detail", body="x")
    store.record(type="fact", name="first", abstract="first plan", body="x")
    store.record(type="fact", name="second", abstract="second plan", body="x")

    store.move("move-me", "project", "moved-project")
    assert "move-me" in store.layout.memory_index.read_text(encoding="utf-8")

    store.supersede("old-fact", "new-fact")
    text = store.layout.memory_index.read_text(encoding="utf-8")
    assert "new-fact" in text
    assert "old-fact" not in text

    store.merge(["first", "second"], "Combined plan", "Combined body")
    text = store.layout.memory_index.read_text(encoding="utf-8")
    assert "[first-merged]" in text
    assert "[first]" not in text and "[second]" not in text


def test_out_of_band_edit_visible_only_after_sync(store):
    store.record(type="fact", name="oob", abstract="out of band detail", body="x")
    target = store.find("oob")
    assert target is not None and target.path is not None
    target.path.write_text(target.to_text().replace("out of band detail", "changed detail"))
    assert "changed detail" not in store.layout.memory_index.read_text(encoding="utf-8")
    store.sync_index()
    assert "changed detail" in store.layout.memory_index.read_text(encoding="utf-8")
