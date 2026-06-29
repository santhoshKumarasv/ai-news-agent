# AI & Data News Digest Agent

Guidance for Claude Code when working in this repository.

## What this is
A personal news-research agent that finds the top Data & AI developments
worldwide, selects the most significant items, and produces a daily digest.
Built on the Claude Agent SDK (Python).

> Note: the current code is the single-agent starting point — it takes a topic
> (default `"technology"`), uses live web search, prints a 3-5 bullet sourced
> digest, and writes it to a dated Markdown file under `digests/`. The "top 10
> Data & AI, daily" shape is the target; align changes toward it.

## Roadmap (phase-gated)
- [x] Phase 1: Manual run -> digest written to a local Markdown file
- [ ] Phase 2: Deliver digest to Outlook/M365 via Microsoft Graph API (OAuth)
- [ ] Phase 3: Schedule the daily run
- [ ] Phase 4: Draft LinkedIn posts from the digest, with a human review
      gate before anything is posted

## Structure
- `src/news_agent/`     - the package
  - `__main__.py`       - entry point (`python -m news_agent`)
  - `cli.py`            - CLI arg -> topic (pure, tested)
  - `config.py`         - settings via pydantic-settings (env / `.env`)
  - `prompts.py`        - system prompt + prompt template
  - `agent.py`          - Claude Agent SDK query loop
  - `output.py`         - render + write the Markdown digest (pure, tested)
- `tests/`              - pytest unit tests for the pure modules
- `pyproject.toml`      - deps + tooling config (source of truth)
- `requirements.txt`    - pinned lockfile (generated via `pip freeze`)
- `.env` / `.env.example` - secrets (ANTHROPIC_API_KEY). `.env` is gitignored.
- `digests/`            - generated output (gitignored)
- `.venv/`              - virtual environment (gitignored)

## Setup
    python3 -m venv .venv
    .venv/bin/pip install -e ".[dev]"   # runtime + dev tools
    cp .env.example .env                # then fill in ANTHROPIC_API_KEY

## How to run
    source .venv/bin/activate
    python -m news_agent "AI policy"   # specific topic
    python -m news_agent               # defaults to "technology"
    # or, via the installed script:
    news-digest "AI policy"

## Dev workflow
    .venv/bin/ruff check .       # lint
    .venv/bin/ruff format .      # format
    .venv/bin/pytest             # tests
    .venv/bin/mypy src           # type-check

## How it works
- The agent is granted the `WebSearch` and `WebFetch` tools and decides when to
  use them. Freshness comes from live web search, NOT the model's training data
  - don't "fix" date wording in the prompt by assuming the model knows today.
- `max_turns` bounds the agentic loop to control cost (currently 12).
- Output is streamed: each `TextBlock` in an `AssistantMessage` is printed as it
  arrives; a `ResultMessage` signals completion. `build_digest()` also returns
  the full text so `output.py` can persist it.
- Model is `claude-opus-4-8`, set in `config.py` (`Settings.model`).

## Conventions
- Python 3.12, Claude Agent SDK (`claude-agent-sdk`).
- Secrets live only in `.env`; loaded through `config.py`. Never hardcode.
- All tunables (model, max_turns, default topic, output dir) live in
  `config.py` so the app stays config-driven and cloud-portable - no
  machine-specific paths.
- The digest agent's behaviour is defined by `SYSTEM_PROMPT` in `prompts.py`,
  NOT this file. This file is for you (Claude Code) when helping me build.
- Keep pure logic (parsing, formatting, file IO) separate from the SDK call so
  it stays unit-testable without hitting the API. Add tests for new pure code.
- After changing dependencies, update `pyproject.toml`, then regenerate the
  lock: `.venv/bin/pip freeze --exclude-editable > requirements.txt`.

## Current focus
Improving curation quality of the single-agent version before adding
subagent decomposition or email delivery.
