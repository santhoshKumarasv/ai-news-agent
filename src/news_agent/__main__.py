"""Entry point: ``python -m news_agent "<topic>"`` or the ``news-digest`` script."""

from __future__ import annotations

import asyncio
import sys
from datetime import datetime

from .agent import build_digest
from .cli import parse_topic
from .config import load_settings
from .output import write_digest


def main() -> None:
    settings = load_settings()
    topic = parse_topic(sys.argv[1:], settings.default_topic)

    body = asyncio.run(build_digest(topic, settings))

    path = write_digest(topic, body, datetime.now(), settings.output_dir)
    print(f"\nSaved digest to {path}")


if __name__ == "__main__":
    main()
