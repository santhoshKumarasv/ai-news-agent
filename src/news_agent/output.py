"""Render a :class:`~news_agent.models.Digest` to Markdown.

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


def digest_filename(digest: Digest) -> str:
    """Dated, slugged filename, e.g. ``2026-06-29-ai-policy.md``."""

    return f"{digest.generated_at:%Y-%m-%d}-{slugify(digest.topic)}.md"


def render_markdown(digest: Digest) -> str:
    """Wrap the digest body in a titled, timestamped Markdown document."""

    return (
        f"# News Digest: {digest.topic}\n\n"
        f"_Generated {digest.generated_at:%Y-%m-%d %H:%M}_\n\n"
        f"{digest.body.strip()}\n"
    )
