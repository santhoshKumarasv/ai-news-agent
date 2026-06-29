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
    """Run the agent for ``topic``, stream progress to stdout, return the digest.

    The model is granted web tools and decides when to use them; freshness comes
    from live search, not the model's training data. Every text block is
    streamed live so the user sees progress (including between-tool narration),
    but only the final result is returned for saving - the intermediate
    narration is not part of the digest.
    """

    options = ClaudeAgentOptions(
        model=settings.model,
        system_prompt=SYSTEM_PROMPT,
        allowed_tools=["WebSearch", "WebFetch"],
        max_turns=settings.max_turns,
    )

    prompt = PROMPT_TEMPLATE.format(topic=topic)

    final = ""
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
        elif isinstance(message, ResultMessage):
            print()  # trailing newline after the streamed output
            final = (message.result or "").strip()
            if message.total_cost_usd:
                print(f"(run cost: ${message.total_cost_usd:.4f})")

    return final
