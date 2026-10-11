"""Replayed batches must not duplicate memories: application is idempotent."""

import json

from agent_memory.core import distill, sessions


def _supersede(handle, abstract="Queue timeout is 30 seconds"):
    return json.dumps(
        {
            "type": "fact",
            "op": "supersede",
            "handle": handle,
            "fields": {"project": "pipeline", "subject": "queue timeout"},
            "abstract": abstract,
            "provenance": ["0-1"],
        }
    )


def test_replayed_supersede_writes_once(store):
    store.record(
        abstract="Queue timeout is 20 seconds",
        type="fact",
        name="queue-timeout",
        fields={"project": "pipeline", "subject": "queue timeout"},
    )
    pointer = store.archive.append_session("replay", ["user: timeout raised", "user: to thirty"])
    messages = sessions.resolve(store.layout, pointer)
    store.config.write.max_rounds = 1

    first = distill.distill(store, "replay", messages, lambda prompt: _supersede("queue-timeout"))
    successor = [name for name in first.batches[0].written if name != "queue-timeout"]
    assert len(successor) == 1
    second = distill.distill(
        store, "replay", messages, lambda prompt: _supersede(successor[0])
    )

    assert second.batches[0].written == ()
    assert second.batches[0].pending == 0
    actives = [
        record.name
        for record in store.records()
        if record.abstract == "Queue timeout is 30 seconds"
    ]
    assert actives == successor


def test_skipped_ops_and_parse_errors_are_reported_not_dropped(store):
    pointer = store.archive.append_session("audit", ["user: nothing durable here"])
    messages = sessions.resolve(store.layout, pointer)
    store.config.write.max_rounds = 1
    replies = [
        json.dumps({"op": "skip"}) + "\n" + json.dumps({"op": "frobnicate"}),
        "not a JSON operation",
    ]
    report = distill.distill(store, "audit", messages, lambda prompt: replies.pop(0))
    batch = report.batches[0]

    assert batch.skipped == 1
    assert any("line 1" in item for item in batch.rejected)
    assert batch.pending == 1
    assert batch.as_dict()["skipped"] == 1
