from news_agent.cli import parse_topic


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
