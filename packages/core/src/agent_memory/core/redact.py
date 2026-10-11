"""Secret-aware text scrubbing with a single home.

Hook logs, executor errors and observation evidence all pass through here so a key
typed once into a conversation does not resurface in a file the user never opens.
"""

from __future__ import annotations

import re

_PATTERNS = (
    re.compile(r"sk-or-[A-Za-z0-9_-]+"),
    re.compile(
        r"(?i)(bearer\s+|(?:api[_-]?key|token|password|secret)[\"']?\s*[=:]\s*[\"']?)"
        r"[^\s,\"']+"
    ),
)


def _replacement(match: re.Match[str]) -> str:
    return f"{match.group(1)}[REDACTED]" if match.groups() else "[REDACTED]"


def redacted(text: str) -> str:
    """Scrub credential-shaped values, keeping any label that names them."""
    clean = text.strip()
    for pattern in _PATTERNS:
        clean = pattern.sub(_replacement, clean)
    return clean
