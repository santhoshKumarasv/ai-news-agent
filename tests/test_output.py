from datetime import datetime

from news_agent.models import Digest
from news_agent.output import digest_filename, render_markdown, slugify

WHEN = datetime(2026, 6, 29, 14, 30)


def _digest(topic="AI policy", body="- point one"):
    return Digest(topic=topic, body=body, generated_at=WHEN)


def test_slugify_basic():
    assert slugify("AI Policy") == "ai-policy"


def test_slugify_strips_punctuation_and_edges():
    assert slugify("  AI & Data!! ") == "ai-data"


def test_slugify_empty_falls_back():
    assert slugify("!!!") == "digest"


def test_digest_filename_is_dated_and_slugged():
    assert digest_filename(_digest("AI policy")) == "2026-06-29-ai-policy.md"


def test_render_markdown_has_title_and_timestamp():
    out = render_markdown(_digest(body="  - point one\n"))
    assert out.startswith("# News Digest: AI policy\n")
    assert "_Generated 2026-06-29 14:30_" in out
    assert "- point one" in out
    assert out.endswith("\n")
