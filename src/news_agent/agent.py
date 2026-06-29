"""The Claude Agent SDK query loop that produces a digest."""

from __future__ import annotations

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    query,
)

from .config import Settings
from .prompts import PROMPT_TEMPLATE, SYSTEM_PROMPT


async def build_digest(topic: str, settings: Settings) -> str:
    """Run the agent for ``topic``, stream text to stdout, and return it.

    The model is granted web tools and decides when to use them; freshness comes
    from live search, not the model's training data.
    """

    options = ClaudeAgentOptions(
        model=settings.model,
        system_prompt=SYSTEM_PROMPT,
        allowed_tools=["WebSearch", "WebFetch"],
        max_turns=settings.max_turns,
    )

    prompt = PROMPT_TEMPLATE.format(topic=topic)

    parts: list[str] = []
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
                    parts.append(block.text)
        elif isinstance(message, ResultMessage):
            print()  # trailing newline after the streamed answer

    return "".join(parts)
