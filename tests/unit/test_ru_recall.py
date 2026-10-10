"""Russian recall: Cyrillic query tokens must reach the FTS index."""

from agent_memory.core.recall import Recall


def test_cyrillic_query_retrieves_russian_record(store):
    store.record(
        abstract="Файлы — единый источник правды",
        type="decision",
        body="Индексы — пересобираемые кэши.",
        name="istochnik-pravdy",
    )

    hits = Recall(store).recall("источник правды")

    assert "istochnik-pravdy" in [hit.name for hit in hits]
