import pytest
from pydantic import ValidationError

from news_agent.config import Settings, load_settings


def test_missing_api_key_raises(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_defaults_applied():
    settings = Settings(_env_file=None, anthropic_api_key="test-key")
    assert settings.model == "claude-opus-4-8"
    assert settings.max_turns == 12
    assert settings.default_topic == "Data & AI"
    assert settings.output_dir == "~/news-digests"
    assert settings.output_format == "txt"


def test_env_overrides(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("MAX_TURNS", "5")
    monkeypatch.setenv("DEFAULT_TOPIC", "energy")
    settings = Settings(_env_file=None)
    assert settings.max_turns == 5
    assert settings.default_topic == "energy"


def test_load_settings_exports_key_to_environ(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    import os

    load_settings(_env_file=None, anthropic_api_key="exported-key")
    assert os.environ["ANTHROPIC_API_KEY"] == "exported-key"
