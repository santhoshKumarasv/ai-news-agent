"""Command-line argument handling."""

from __future__ import annotations

from collections.abc import Sequence


def parse_topic(args: Sequence[str], default: str) -> str:
    """Join CLI args into a single topic, falling back to ``default``.

    ``["AI", "policy"]`` -> ``"AI policy"``; empty/whitespace -> ``default``.
    """

    topic = " ".join(args).strip()
    return topic or default
