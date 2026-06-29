from datetime import datetime
from pathlib import Path

from news_agent.delivery import FileSink, Sink
from news_agent.models import Digest

WHEN = datetime(2026, 6, 29, 14, 30)


def test_file_sink_is_a_sink():
    assert issubclass(FileSink, Sink)


def test_file_sink_writes_and_returns_path(tmp_path):
    sink = FileSink(tmp_path / "digests")
    location = sink.deliver(Digest("AI policy", "- point one", WHEN))

    path = Path(location)
    assert path.name == "2026-06-29-ai-policy.md"
    assert path.exists()
    assert "# News Digest: AI policy" in path.read_text(encoding="utf-8")


def test_file_sink_creates_nested_dir(tmp_path):
    nested = tmp_path / "a" / "b"
    FileSink(nested).deliver(Digest("x", "y", WHEN))
    assert nested.is_dir()
