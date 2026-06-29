"""The delivery contract: where a digest can be sent."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Digest


class Sink(ABC):
    """A destination a digest can be delivered to.

    Implementations: :class:`~news_agent.delivery.file_sink.FileSink` today;
    an email/Graph sink for Phase 2 next. Keep delivery logic behind this
    interface so the agent and CLI never depend on a concrete destination.
    """

    @abstractmethod
    def deliver(self, digest: Digest) -> str:
        """Deliver ``digest`` and return a human-readable location.

        e.g. a file path for a file sink, or a recipient/message id for email.
        """
