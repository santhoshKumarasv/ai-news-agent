"""Application configuration.

Settings are loaded from environment variables (and a local ``.env`` file via
pydantic-settings). Keep all tunables here so the app stays config-driven and
portable to a cloud host - no machine-specific paths or hardcoded values.
"""

from __future__ import annotations

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings, validated on construction."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Required: the Claude Agent SDK authenticates with this.
    anthropic_api_key: str

    # Tunables (override via env or .env).
    model: str = "claude-opus-4-8"
    max_turns: int = 12
    default_topic: str = "Data & AI"
    output_dir: str = "~/news-digests"
    output_format: str = "txt"


def load_settings(**overrides: object) -> Settings:
    """Load settings and make the API key visible to the SDK.

    The Claude Agent SDK reads ``ANTHROPIC_API_KEY`` straight from the process
    environment, so we mirror the validated value back into ``os.environ``.
    Raises ``pydantic.ValidationError`` if the key is missing.
    """

    settings = Settings(**overrides)  # type: ignore[arg-type]
    os.environ.setdefault("ANTHROPIC_API_KEY", settings.anthropic_api_key)
    return settings
