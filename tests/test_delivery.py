from datetime import datetime
from pathlib import Path

from news_agent.delivery import SINKS, FileSink, Sink, TextFileSink
from news_agent.models import Digest

WHEN = datetime(2026, 6, 29, 20, 30, 15)


def test_sinks_are_sinks():
    assert issubclass(TextFileSink, Sink)
    assert issubclass(FileSink, Sink)


def test_sinks_registry_maps_formats():
    assert SINKS == {"txt": TextFileSink, "md": FileSink}


def test_text_sink_writes_timestamped_txt(tmp_path):
    location = TextFileSink(tmp_path / "out").deliver(
        Digest("AI policy", "- point one", WHEN)
    )
    path = Path(location)
    assert path.name == "2026-06-29_2030-15-ai-policy.txt"
    assert path.exists()
    body = path.read_text(encoding="utf-8")
    assert body.startswith("News Digest: AI policy")
    assert "- point one" in body


def test_file_sink_writes_timestamped_md(tmp_path):
    location = FileSink(tmp_path / "out").deliver(Digest("x", "y", WHEN))
    path = Path(location)
    assert path.name == "2026-06-29_2030-15-x.md"
    assert "# News Digest: x" in path.read_text(encoding="utf-8")


def test_sink_expands_user_and_creates_dir(tmp_path, monkeypatch):
    # Treat tmp_path as $HOME so "~/sub" resolves under it.
    monkeypatch.setenv("HOME", str(tmp_path))
    location = TextFileSink("~/sub").deliver(Digest("x", "y", WHEN))
    assert Path(location).parent == tmp_path / "sub"
    assert (tmp_path / "sub").is_dir()
