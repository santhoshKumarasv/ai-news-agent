from datetime import datetime

from news_agent.models import Digest
from news_agent.output import (
    render_markdown,
    render_text,
    slugify,
    timestamped_filename,
)

WHEN = datetime(2026, 6, 29, 20, 30, 15)


def _digest(topic="AI policy", body="- point one"):
    return Digest(topic=topic, body=body, generated_at=WHEN)


def test_slugify_basic():
    assert slugify("AI Policy") == "ai-policy"


def test_slugify_strips_punctuation_and_edges():
    assert slugify("  AI & Data!! ") == "ai-data"


def test_slugify_empty_falls_back():
    assert slugify("!!!") == "digest"


def test_timestamped_filename_includes_time_and_ext():
    assert (
        timestamped_filename(_digest("AI policy"), "txt")
        == "2026-06-29_2030-15-ai-policy.txt"
    )


def test_timestamped_filename_honors_ext():
    assert timestamped_filename(_digest("x"), "md").endswith("-x.md")


def test_render_markdown_has_title_and_timestamp():
    out = render_markdown(_digest(body="  - point one\n"))
    assert out.startswith("# News Digest: AI policy\n")
    assert "_Generated 2026-06-29 20:30_" in out
    assert "- point one" in out
    assert out.endswith("\n")


def test_render_text_is_plain_with_header():
    out = render_text(_digest(body="  - point one\n"))
    assert out.startswith("News Digest: AI policy\n")
    assert "Generated 2026-06-29 20:30" in out
    assert "#" not in out.splitlines()[0]  # no Markdown heading
    assert "- point one" in out
