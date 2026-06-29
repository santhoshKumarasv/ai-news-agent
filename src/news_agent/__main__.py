"""Entry point: ``python -m news_agent "<focus>"`` or the ``news-digest`` script."""

from __future__ import annotations

import asyncio
import sys
from datetime import datetime

from .agent import build_digest
from .cli import parse_args
from .config import load_settings
from .delivery import FileSink
from .models import Digest


def main() -> None:
    settings = load_settings()
    opts = parse_args(sys.argv[1:], settings)

    # Apply per-run CLI overrides (model, max_turns) on top of config.
    run_settings = settings.model_copy(
        update={"model": opts.model, "max_turns": opts.max_turns}
    )

    body = asyncio.run(build_digest(opts.topic, run_settings))
    digest = Digest(topic=opts.topic, body=body, generated_at=datetime.now())

    if not opts.save:
        print("\n(--no-save: digest not written to disk)")
        return

    location = FileSink(opts.output_dir).deliver(digest)
    print(f"\nSaved digest to {location}")


if __name__ == "__main__":
    main()
