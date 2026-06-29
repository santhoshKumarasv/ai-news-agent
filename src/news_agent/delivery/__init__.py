"""Delivery sinks for a produced digest.

Add new destinations (e.g. an Outlook/Graph email sink for Phase 2) by
subclassing :class:`Sink` and exporting them here.
"""

from collections.abc import Callable
from pathlib import Path

from .base import Sink
from .file_sink import FileSink, TextFileSink

# Map a format name (the --format flag / config) to a sink factory that takes
# the output directory. A future email sink is constructed separately, not here.
SINKS: dict[str, Callable[[str | Path], Sink]] = {
    "txt": TextFileSink,
    "md": FileSink,
}

__all__ = ["Sink", "FileSink", "TextFileSink", "SINKS"]
