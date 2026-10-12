"""The always-injected root index. A hard budget, enforced by dropping the lightest lines.

Injection is query-independent by design: it carries stable high-weight residents, never
query-sensitive picks. Light-but-relevant entries stay reachable through recall and context,
which rank by relevance as well as weight; the two tracks divide labor instead of agreeing."""

from __future__ import annotations

import dataclasses
import sqlite3
from collections.abc import Iterable

from .config import Config
from .paths import StoreLayout
from .record import MemoryRecord


@dataclasses.dataclass(frozen=True)
class Entry:
    """One injected line. Rows from the search index convert to these, so a write
    refreshes the injection without reparsing every truth file."""

    name: str
    abstract: str
    location: str
    weight: float
    updated: str
    active: bool


def render(records: list[MemoryRecord], config: Config, root: str = "") -> str:
    return render_entries([_entry_of(record, root) for record in records], config)


def render_entries(entries: list[Entry], config: Config) -> str:
    eligible = [
        entry
        for entry in entries
        if entry.active and entry.weight >= config.recall.memory_md_weight_floor
    ]
    eligible.sort(key=lambda entry: (-entry.weight, entry.updated, entry.name))

    header = config.memory_md.header + "\n\n"
    lines: list[str] = []
    used = len(header.encode("utf-8"))
    for entry in eligible:
        if len(lines) >= config.memory_md.max_lines:
            break
        line = f"- [{entry.name}]({entry.location}) — {entry.abstract}\n"
        cost = len(line.encode("utf-8"))
        if used + cost > config.memory_md.budget_bytes:
            break
        lines.append(line)
        used += cost
    return header + "".join(lines)


def write(layout: StoreLayout, records: list[MemoryRecord]) -> str:
    return write_entries(layout, [_entry_of(record, str(layout.root)) for record in records])


def write_entries(layout: StoreLayout, entries: list[Entry]) -> str:
    text = render_entries(entries, layout.config)
    layout.memory_index.write_text(text, encoding="utf-8")
    return text


def rows_to_entries(rows: Iterable[sqlite3.Row]) -> list[Entry]:
    return [
        Entry(
            name=str(row["name"]),
            abstract=str(row["abstract"]),
            location=str(row["path"]),
            weight=float(row["weight"]),
            updated=str(row["updated"]),
            active=row["invalid_at"] is None,
        )
        for row in rows
    ]


def _entry_of(record: MemoryRecord, root: str) -> Entry:
    location = str(record.path)
    if root and location.startswith(root):
        location = location[len(root) :].lstrip("/")
    return Entry(
        name=record.name,
        abstract=record.abstract,
        location=location,
        weight=record.weight,
        updated=record.updated,
        active=record.is_active(),
    )
