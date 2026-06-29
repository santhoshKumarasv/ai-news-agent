from datetime import datetime

from news_agent.output import (
    digest_filename,
    format_digest,
    slugify,
    write_digest,
)

WHEN = datetime(2026, 6, 29, 14, 30)


def test_slugify_basic():
    assert slugify("AI Policy") == "ai-policy"


def test_slugify_strips_punctuation_and_edges():
    assert slugify("  AI & Data!! ") == "ai-data"


def test_slugify_empty_falls_back():
    assert slugify("!!!") == "digest"


def test_digest_filename_is_dated_and_slugged():
    assert digest_filename("AI policy", WHEN) == "2026-06-29-ai-policy.md"


def test_format_digest_has_title_and_timestamp():
    out = format_digest("AI policy", "  - point one\n", WHEN)
    assert out.startswith("# News Digest: AI policy\n")
    assert "_Generated 2026-06-29 14:30_" in out
    assert "- point one" in out
    assert out.endswith("\n")


def test_write_digest_creates_file(tmp_path):
    path = write_digest("AI policy", "- point one", WHEN, tmp_path / "digests")
    assert path.name == "2026-06-29-ai-policy.md"
    assert path.exists()
    assert "# News Digest: AI policy" in path.read_text(encoding="utf-8")
