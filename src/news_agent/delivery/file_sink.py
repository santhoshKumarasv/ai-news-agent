"""Filesystem delivery sinks: write a digest to a dated local file."""

from __future__ import annotations

from pathlib import Path

from ..models import Digest
from ..output import render_markdown, render_text, timestamped_filename
from .base import Sink


class _FilesystemSink(Sink):
    """Shared logic: render the digest and write it under ``output_dir``.

    Subclasses set the file extension and how the digest is rendered.
    """

    ext: str

    def __init__(self, output_dir: str | Path) -> None:
        # expanduser so paths like "~/news-digests" resolve to the home dir.
        self.output_dir = Path(output_dir).expanduser()

    def render(self, digest: Digest) -> str:  # pragma: no cover - overridden
        raise NotImplementedError

    def deliver(self, digest: Digest) -> str:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        path = self.output_dir / timestamped_filename(digest, self.ext)
        path.write_text(self.render(digest), encoding="utf-8")
        return str(path)


class TextFileSink(_FilesystemSink):
    """Write the digest as a plain ``.txt`` file (easy local verification)."""

    ext = "txt"

    def render(self, digest: Digest) -> str:
        return render_text(digest)


class FileSink(_FilesystemSink):
    """Write the digest as a Markdown ``.md`` file."""

    ext = "md"

    def render(self, digest: Digest) -> str:
        return render_markdown(digest)
