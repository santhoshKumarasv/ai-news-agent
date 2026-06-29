"""Delivery sinks for a produced digest.

Add new destinations (e.g. an Outlook/Graph email sink for Phase 2) by
subclassing :class:`Sink` and exporting them here.
"""

from .base import Sink
from .file_sink import FileSink

__all__ = ["Sink", "FileSink"]
