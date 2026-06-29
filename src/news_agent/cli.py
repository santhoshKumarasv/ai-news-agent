"""Command-line argument handling."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from dataclasses import dataclass

from .config import Settings


def parse_topic(args: Sequence[str], default: str) -> str:
    """Join CLI args into a single topic, falling back to ``default``.

    ``["AI", "policy"]`` -> ``"AI policy"``; empty/whitespace -> ``default``.
    """

    topic = " ".join(args).strip()
    return topic or default


@dataclass(frozen=True)
class RunOptions:
    """Resolved options for a single digest run (CLI flags over config)."""

    topic: str
    output_dir: str
    model: str
    max_turns: int
    save: bool


def build_parser(settings: Settings) -> argparse.ArgumentParser:
    """Build the arg parser, seeding defaults from ``settings``."""

    parser = argparse.ArgumentParser(
        prog="news-digest",
        description="Generate a ranked top-10 Data & AI news digest.",
    )
    parser.add_argument(
        "focus",
        nargs="*",
        help="optional focus within Data & AI, e.g. 'AI policy' "
        f"(default: {settings.default_topic})",
    )
    parser.add_argument(
        "--output-dir",
        default=settings.output_dir,
        help=f"directory for saved digests (default: {settings.output_dir})",
    )
    parser.add_argument(
        "--model",
        default=settings.model,
        help=f"model id to use (default: {settings.model})",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=settings.max_turns,
        help=f"cap on agent turns (default: {settings.max_turns})",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="print the digest only; do not write a Markdown file",
    )
    return parser


def parse_args(argv: Sequence[str], settings: Settings) -> RunOptions:
    """Parse ``argv`` into resolved :class:`RunOptions`."""

    ns = build_parser(settings).parse_args(list(argv))
    return RunOptions(
        topic=parse_topic(ns.focus, settings.default_topic),
        output_dir=ns.output_dir,
        model=ns.model,
        max_turns=ns.max_turns,
        save=not ns.no_save,
    )
