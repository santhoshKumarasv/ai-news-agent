# AI & Data News Digest Agent

Guidance for Claude Code when working in this repository.

## What this is
A weekly Data & AI news-intelligence agent for **Sugansa Solutions** (a Data &
AI services company: Data Engineering, AI Architecture, Modern Data Platforms,
Agentic AI). Each run searches the web for the previous week's most important,
in-scope developments and produces a brief that positions Sugansa as a thought
leader for business/technology/data/AI leaders and enterprise transformation
teams. Built on the Claude Agent SDK (Python).

> Note: the current code produces **PART 1** only - a "Weekly News Intelligence
> Summary" of 5-7 items, each with headline, source, summary, why-it-matters
> for Sugansa, relevance area, and a suggested LinkedIn angle (defined in
> `prompts.py`). It writes a timestamped `.txt` to `~/news-digests` for local
> verification. The CLI argument is an optional *focus* that narrows within the
> Sugansa scope (default: the full scope).
>
> Deferred / planned:
> - **PART 2** - a ready-to-post LinkedIn post (~250-350 words, branded
>   hashtags, soft CTA) synthesised from PART 1.
> - **Poster** - a 1200x1200 image styled to sample posters (needs an image
>   model + the user's samples; not the text agent).
> - Weekly **Sunday-evening scheduling** and **email delivery** (new `Sink`).

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
  - `models.py`         - `Digest` dataclass (the produced artifact)
  - `output.py`         - render a `Digest` to text/Markdown (pure, tested)
  - `delivery/`         - where a digest goes: `Sink` ABC, `TextFileSink`
                          (.txt) and `FileSink` (.md), and a `SINKS` registry;
                          add an Outlook/Graph sink here for Phase 2
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
    python -m news_agent                       # full Data & AI top-10
    python -m news_agent "AI policy"           # optional focus
    news-digest "AI policy"                     # installed script form
    news-digest --no-save                       # print only, don't write a file
    news-digest --format md                     # save Markdown instead of .txt
    news-digest --output-dir out --max-turns 8  # override config per run
    news-digest --help                          # all flags

By default a run saves a timestamped plain-text file (e.g.
`2026-06-29_2031-40-data-ai.txt`) to `~/news-digests` for easy local
verification before email delivery exists. Flags (`--output-dir`, `--format`,
`--model`, `--max-turns`, `--no-save`) override the `config.py` defaults for a
single run; parsing lives in `cli.py`.

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
- Output is streamed: every `TextBlock` is printed live (including between-tool
  narration) so the user sees progress, but `build_digest()` returns only
  `ResultMessage.result` - the final digest - so saved files don't contain the
  intermediate narration. The run cost is printed from `total_cost_usd`.
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
