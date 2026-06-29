import pytest

from news_agent.cli import RunOptions, parse_args, parse_topic
from news_agent.config import Settings


@pytest.fixture
def settings():
    return Settings(_env_file=None, anthropic_api_key="test-key")


# --- parse_topic -----------------------------------------------------------


def test_joins_multiple_args():
    assert parse_topic(["AI", "policy"], "technology") == "AI policy"


def test_single_arg():
    assert parse_topic(["healthcare"], "technology") == "healthcare"


def test_empty_falls_back_to_default():
    assert parse_topic([], "technology") == "technology"


def test_whitespace_only_falls_back_to_default():
    assert parse_topic(["   "], "technology") == "technology"


def test_strips_surrounding_whitespace():
    assert parse_topic(["  AI policy  "], "technology") == "AI policy"


# --- parse_args ------------------------------------------------------------


def test_parse_args_defaults(settings):
    opts = parse_args([], settings)
    assert opts == RunOptions(
        topic=settings.default_topic,
        output_dir=settings.output_dir,
        model=settings.model,
        max_turns=settings.max_turns,
        save=True,
    )


def test_parse_args_focus(settings):
    assert parse_args(["AI", "policy"], settings).topic == "AI policy"


def test_parse_args_no_save(settings):
    assert parse_args(["--no-save"], settings).save is False


def test_parse_args_output_dir_override(settings):
    assert parse_args(["--output-dir", "/tmp/out"], settings).output_dir == "/tmp/out"


def test_parse_args_model_and_turns_override(settings):
    opts = parse_args(["--model", "claude-x", "--max-turns", "3"], settings)
    assert opts.model == "claude-x"
    assert opts.max_turns == 3


def test_parse_args_focus_with_flags(settings):
    opts = parse_args(["--no-save", "enterprise", "AI"], settings)
    assert opts.topic == "enterprise AI"
    assert opts.save is False
