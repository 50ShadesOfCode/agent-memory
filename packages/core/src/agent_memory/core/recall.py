"""Eligibility before relevance, then relevance × weight × recency. Zero LLM (ADR-002).

The default surface holds active files only. `--as-of` is the one reader of the history
surface, and it judges a file by its validity interval, never by its text alone.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import pathlib
import sqlite3

from . import observation, timestamp
from .access_log import KIND_RECALL, AccessEntry, AccessLog
from .config import Config
from .database import SURFACE_ACTIVE, SURFACE_HISTORY, Database
from .search_index import LINK_SEPARATOR, Candidate, SearchIndex, normalize_scope
from .store import Store
from .vector_index import VectorIndex


def fuse_candidates(
    lexical: list[Candidate], dense: list[Candidate], pool: int, k: int, sources: int
) -> list[Candidate]:
    """Reciprocal-rank fusion by chunk identity, normalized to a stable 0..1 scale."""

    def identity(item: Candidate) -> tuple[str, str, str, str]:
        return (item.name, item.kind, item.anchor, item.heading)

    scores: dict[tuple[str, str, str, str], float] = {}
    exemplars: dict[tuple[str, str, str, str], Candidate] = {}
    for candidates in (lexical, dense):
        seen: set[tuple[str, str, str, str]] = set()
        for rank, candidate in enumerate(candidates, 1):
            key = identity(candidate)
            if key in seen:
                continue
            seen.add(key)
            exemplars.setdefault(key, candidate)
            scores[key] = scores.get(key, 0.0) + 1.0 / (k + rank)
    maximum = sources / (k + 1)
    fused = [
        dataclasses.replace(exemplars[key], relevance=score / maximum)
        for key, score in scores.items()
    ]
    fused.sort(key=lambda item: (-item.relevance, identity(item)))
    return fused[:pool]


@dataclasses.dataclass(frozen=True)
class Hit:
    name: str
    path: str
    abstract: str
    anchor: str
    heading: str
    type: str
    updated: str
    status: str
    weight: float
    relevance: float
    recency: float
    score: float
    source: str = "memory"
    provenance: tuple[str, ...] = ()
    cited_by: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        payload = dataclasses.asdict(self)
        payload["provenance"] = list(self.provenance)
        payload["cited_by"] = list(self.cited_by)
        return payload


class Recall:
    def __init__(self, store: Store):
        self._store = store
        self._config: Config = store.config
        self._database = Database(store.layout)

    def recall(
        self,
        query: str,
        scope: str | None = None,
        as_of: str | None = None,
        limit: int | None = None,
        log: bool = True,
    ) -> list[Hit]:
        limit = self._config.recall.default_limit if limit is None else limit
        if limit < 1:
            raise ValueError("limit must be positive")
        pool = limit * self._config.recall.candidate_pool_multiplier
        scope_path = normalize_scope(scope)
        with self._database.connect() as connection:
            index = SearchIndex(connection)
            candidates = index.match(query, pool, SURFACE_ACTIVE, scope_path=scope_path)
            if as_of is not None:
                candidates = candidates + index.match(
                    query, pool, SURFACE_HISTORY, scope_path=scope_path
                )
            eligible = self._eligible(index.eligibility_rows(), scope=scope, as_of=as_of)
            if self._config.index.vector_enabled:
                assert self._store.embedder is not None
                dense = VectorIndex(
                    connection, self._store.embedder, self._config.index.vector_model
                ).match(query, pool, eligible_names=set(eligible))
                if dense:
                    candidates = fuse_candidates(
                        candidates,
                        dense,
                        pool,
                        self._config.recall.rrf_k,
                        self._config.recall.rrf_source_count,
                    )
            hits = self._rank(candidates, eligible, as_of=as_of, index=index)
            hits = hits[:limit]
            if not log:
                return hits
            entries = [
                AccessEntry(
                    self._store.clock.now().isoformat(),
                    hit.name,
                    query,
                    KIND_RECALL,
                    self._store.agent,
                )
                for hit in hits
            ]
        if entries:
            with self._database.connect() as logged:
                AccessLog(logged).append(entries)
        observation.emit(
            "recall_return", query=query, scope=scope, as_of=as_of,
            effective_limit=limit, hits=[hit.as_dict() for hit in hits],
        )
        return hits

    def _eligible(
        self,
        rows: list[sqlite3.Row],
        scope: str | None,
        as_of: str | None,
    ) -> dict[str, sqlite3.Row]:
        eligible: dict[str, sqlite3.Row] = {}
        moment = timestamp.parse(as_of) if as_of else None
        for row in rows:
            name = str(row["name"])
            if scope and not self._in_scope(str(row["path"]), scope):
                continue
            if moment is None:
                if row["invalid_at"]:
                    continue
            elif not self._current_at(row, moment):
                continue
            eligible[name] = row
        return eligible

    def _in_scope(self, path: str, scope: str) -> bool:
        normalized = normalize_scope(scope)
        if not normalized:
            return False
        scope_parts = pathlib.PurePath(normalized).parts
        return pathlib.PurePath(path).parts[: len(scope_parts)] == scope_parts

    def _current_at(self, row: sqlite3.Row, moment: dt.datetime) -> bool:
        if timestamp.parse(str(row["valid_from"])) > moment:
            return False
        ended = row["invalid_at"]
        return not (ended and timestamp.parse(str(ended)) <= moment)

    def _rank(
        self,
        candidates: list[Candidate],
        eligible: dict[str, sqlite3.Row],
        as_of: str | None,
        index: SearchIndex,
    ) -> list[Hit]:
        best: dict[str, tuple[float, str, str]] = {}
        for candidate in candidates:
            if candidate.name not in eligible:
                continue
            weighted = candidate.relevance * self._kind_weight(candidate.kind)
            current = best.get(candidate.name)
            if current is None or weighted > current[0]:
                best[candidate.name] = (weighted, candidate.anchor, candidate.heading)

        reference = timestamp.parse(as_of) if as_of else self._store.clock.now()
        full = index.rows_for_names(set(best))
        hits: list[Hit] = []
        for name, (relevance, anchor, heading) in best.items():
            row = full[name]
            recency = self._recency(str(row["updated"]), reference)
            weight = float(row["weight"])
            hits.append(
                Hit(
                    name=name,
                    path=str(self._store.root / str(row["path"])),
                    abstract=str(row["abstract"]),
                    anchor=anchor,
                    heading=heading,
                    type=str(row["type"]),
                    updated=str(row["updated"]),
                    status="invalid" if row["invalid_at"] else "active",
                    weight=weight,
                    relevance=relevance,
                    recency=recency,
                    score=relevance * weight * recency,
                    provenance=tuple(
                        item for item in str(row["provenance"]).split(LINK_SEPARATOR) if item
                    ),
                )
            )
        hits.sort(key=lambda hit: (-hit.score, hit.name))
        return hits

    def _kind_weight(self, kind: str) -> float:
        from .chunking import KIND_ABSTRACT

        if kind == KIND_ABSTRACT:
            return self._config.index.bm25_abstract_weight
        return self._config.index.bm25_body_weight

    def _recency(self, updated: str, reference: dt.datetime) -> float:
        age_days = max(0.0, timestamp.days_between(reference, timestamp.parse(updated)))
        decayed = self._config.recall.recency_decay_base ** (
            age_days / self._config.recall.recency_half_life_days
        )
        return max(self._config.recall.recency_floor, decayed)
