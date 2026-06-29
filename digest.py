"""News-digest agent.

Given a topic, the agent searches the web for recent coverage and writes a
short, sourced digest. Built on the Claude Agent SDK.

Usage:
    python digest.py "AI policy"
    python digest.py            # defaults to the topic below
"""

import asyncio
import sys

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    query,
)
from dotenv import load_dotenv

# Load ANTHROPIC_API_KEY (and anything else) from .env into the environment.
load_dotenv()

DEFAULT_TOPIC = "technology"

SYSTEM_PROMPT = (
    "You are a news-digest assistant. Given a topic, search the web for "
    "recent, reputable coverage and write a concise digest of the most "
    "important developments. Structure the output as 3-5 bullet points, each "
    "one or two sentences, and cite the source for every point. Lead with the "
    "single most significant item. Prefer the last few days of coverage."
)


async def build_digest(topic: str) -> None:
    options = ClaudeAgentOptions(
        model="claude-opus-4-8",
        system_prompt=SYSTEM_PROMPT,
        allowed_tools=["WebSearch", "WebFetch"],
        max_turns=12,
    )

    prompt = f"Produce today's news digest on the topic: {topic}"

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
        elif isinstance(message, ResultMessage):
            print()  # trailing newline after the streamed answer


def main() -> None:
    topic = " ".join(sys.argv[1:]).strip() or DEFAULT_TOPIC
    asyncio.run(build_digest(topic))


if __name__ == "__main__":
    main()
