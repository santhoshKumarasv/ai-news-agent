"""Write a digest to a dated local Markdown file (Phase 1 delivery)."""

from __future__ import annotations

from pathlib import Path

from ..models import Digest
from ..output import digest_filename, render_markdown
from .base import Sink


class FileSink(Sink):
    """Persist the digest as Markdown under ``output_dir``."""

    def __init__(self, output_dir: str | Path) -> None:
        self.output_dir = Path(output_dir)

    def deliver(self, digest: Digest) -> str:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        path = self.output_dir / digest_filename(digest)
        path.write_text(render_markdown(digest), encoding="utf-8")
        return str(path)
