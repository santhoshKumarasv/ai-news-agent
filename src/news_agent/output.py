"""Render a :class:`~news_agent.models.Digest` to text/Markdown.

Pure rendering only - no file IO. Persisting/sending lives in ``delivery/``.
"""

from __future__ import annotations

import re

from .models import Digest

_SLUG_STRIP = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Lowercase, hyphenate, and strip a string for safe use in a filename."""

    slug = _SLUG_STRIP.sub("-", text.lower()).strip("-")
    return slug or "digest"


def timestamped_filename(digest: Digest, ext: str) -> str:
    """Timestamped, slugged filename, e.g. ``2026-06-29_2030-15-ai-policy.txt``.

    Includes the time so repeated runs (same day, same focus) never overwrite.
    """

    stamp = f"{digest.generated_at:%Y-%m-%d_%H%M-%S}"
    return f"{stamp}-{slugify(digest.topic)}.{ext}"


def render_markdown(digest: Digest) -> str:
    """Wrap the digest body in a titled, timestamped Markdown document."""

    return (
        f"# News Digest: {digest.topic}\n\n"
        f"_Generated {digest.generated_at:%Y-%m-%d %H:%M}_\n\n"
        f"{digest.body.strip()}\n"
    )


def render_text(digest: Digest) -> str:
    """Plain-text version for quick local verification."""

    return (
        f"News Digest: {digest.topic}\n"
        f"Generated {digest.generated_at:%Y-%m-%d %H:%M}\n"
        f"{'=' * 60}\n\n"
        f"{digest.body.strip()}\n"
    )
