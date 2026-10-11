"""Offline recall benchmark: fixed corpus, fixed queries, pinned floors.

Deterministic and model-free: the same store, the same queries, every run.
Thresholds below are the measured baseline plus margin, not aspirations —
tighten them when the engine genuinely improves.
"""

import time

from agent_memory.core.recall import Recall

PINNED_AT_1 = 0.90
PINNED_AT_5 = 0.95
PINNED_P99_MS = 500.0

TOPICS = [
    ("deploy", ["pipeline", "release", "rollback", "canary", "freeze"]),
    ("database", ["backup", "migration", "index", "replica", "vacuum"]),
    ("oncall", ["pager", "rotation", "escalation", "handoff", "ticket"]),
    ("api", ["ratelimit", "token", "version", "deprecation", "quota"]),
    ("storage", ["bucket", "retention", "snapshot", "tier", "archive"]),
    ("network", ["dns", "proxy", "timeout", "retry", "certificate"]),
    ("ci", ["runner", "cache", "artifact", "matrix", "flaky"]),
    ("observability", ["dashboard", "alert", "trace", "slo", "log"]),
    ("auth", ["login", "token", "scope", "refresh", "mfa"]),
    ("cache", ["ttl", "eviction", "warming", "stampede", "shard"]),
    ("queue", ["worker", "poison", "delay", "priority", "drain"]),
    ("search", ["index", "facet", "synonym", "ranking", "suggest"]),
]

RU_TOPICS = [
    ("деплой", ["пайплайн", "релиз", "откат", "заморозка"]),
    ("база", ["бэкап", "миграция", "индекс", "реплика"]),
    ("дежурство", ["пейджер", "смена", "эскалация"]),
    ("хранилище", ["корзина", "снимок", "архив"]),
    ("поиск", ["выдача", "фильтр", "ранжирование"]),
    ("очередь", ["воркер", "задержка", "приоритет"]),
]

FAMILIES = [
    ("deploy", "pipeline window", [
        "morning",
        "evening",
        "friday",
        "hotfix",
        "nightly",
        "weekly",
    ]),
    ("database", "backup retention", [
        "daily",
        "hourly",
        "monthly",
        "offsite",
        "local",
        "encrypted",
    ]),
    ("api", "rate limit", [
        "perkey",
        "global",
        "burst",
        "trial",
        "enterprise",
        "legacy",
    ]),
    ("oncall", "rotation schedule", [
        "primary",
        "secondary",
        "weekend",
        "holiday",
        "shadow",
        "split",
    ]),
    ("storage", "snapshot policy", [
        "retain",
        "purge",
        "lock",
        "copy",
        "verify",
        "expire",
    ]),
    ("network", "timeout budget", [
        "connect",
        "read",
        "write",
        "idle",
        "retry",
        "total",
    ]),
    ("деплой", "окно заморозки", [
        "утро",
        "вечер",
        "пятница",
        "ночь",
        "релиз",
        "срочно",
    ]),
    ("база", "срок хранения", [
        "день",
        "час",
        "месяц",
        "год",
        "внешний",
        "локально",
    ]),
    ("поиск", "выдача результаты", [
        "фильтр",
        "сортировка",
        "страница",
        "подсветка",
        "кеш",
        "синонимы",
    ]),
    ("очередь", "воркер задачи", [
        "яд",
        "повтор",
        "задержка",
        "приоритет",
        "пачка",
        "таймаут",
    ]),
]


def _seeded_store(store):
    names = []
    for topic, aspects in TOPICS:
        for index, aspect in enumerate(aspects):
            name = f"{topic}-{aspect}-{index}"
            store.record(
                type="fact",
                name=name,
                abstract=f"{topic} {aspect} marker-{topic}-{index}",
                body=f"Notes on {topic} {aspect}, detail {index}.",
            )
            names.append((name, f"{aspect} {topic}"))
    for topic_index, (topic, aspects) in enumerate(RU_TOPICS):
        for index, aspect in enumerate(aspects):
            name = f"ru-{topic_index}-{index}"
            store.record(
                type="fact",
                name=name,
                abstract=f"{topic} {aspect} метка-{index}",
                body=f"Заметки про {topic} {aspect}.",
            )
            names.append((name, f"{aspect} {topic}"))
    for family_index, (topic, shared, details) in enumerate(FAMILIES):
        for detail_index, detail in enumerate(details):
            name = f"fam-{family_index}-{detail_index}"
            store.record(
                type="fact",
                name=name,
                abstract=f"{topic} {shared} {detail}",
                body=f"Notes on {topic} {shared}, detail {detail}.",
            )
            names.append((name, f"{detail} {topic}"))
    return names


def test_recall_benchmark(store):
    expected = _seeded_store(store)
    ranks = []
    latencies = []
    for name, query in expected:
        started = time.perf_counter()
        hits = Recall(store).recall(query, limit=5, log=False)
        latencies.append((time.perf_counter() - started) * 1000.0)
        found = [hit.name for hit in hits]
        ranks.append(found.index(name) + 1 if name in found else None)

    measured = [rank for rank in ranks if rank is not None]
    assert len(measured) / len(ranks) >= PINNED_AT_5
    assert sum(1 for rank in measured if rank == 1) / len(ranks) >= PINNED_AT_1
    ordered = sorted(latencies)
    assert ordered[int(len(ordered) * 0.99)] <= PINNED_P99_MS
