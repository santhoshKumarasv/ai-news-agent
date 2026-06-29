"""Render and persist a digest to a local Markdown file (Phase 1 delivery)."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

_SLUG_STRIP = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Lowercase, hyphenate, and strip a string for safe use in a filename."""

    slug = _SLUG_STRIP.sub("-", text.lower()).strip("-")
    return slug or "digest"


def digest_filename(topic: str, generated_at: datetime) -> str:
    """Dated, slugged filename, e.g. ``2026-06-29-ai-policy.md``."""

    return f"{generated_at:%Y-%m-%d}-{slugify(topic)}.md"


def format_digest(topic: str, body: str, generated_at: datetime) -> str:
    """Wrap the agent's output in a titled, timestamped Markdown document."""

    return (
        f"# News Digest: {topic}\n\n"
        f"_Generated {generated_at:%Y-%m-%d %H:%M}_\n\n"
        f"{body.strip()}\n"
    )


def write_digest(
    topic: str,
    body: str,
    generated_at: datetime,
    output_dir: str | Path,
) -> Path:
    """Format and write the digest under ``output_dir``; return the file path."""

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / digest_filename(topic, generated_at)
    path.write_text(format_digest(topic, body, generated_at), encoding="utf-8")
    return path
