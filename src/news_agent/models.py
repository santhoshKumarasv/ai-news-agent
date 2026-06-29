"""Core data types shared across the agent."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Digest:
    """A produced digest, ready to be rendered and delivered.

    The agent yields the ``body`` text; ``topic`` and ``generated_at`` give it a
    title and a stable identity. Delivery sinks consume this object.
    """

    topic: str
    body: str
    generated_at: datetime
