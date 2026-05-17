# ============================================================
# 09: Multi-Agent Systems — Orchestration
# ============================================================

import asyncio

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent

load_dotenv()

# ── Specialized sub-agents — each has a focused, single responsibility ──
researcher = Agent(
    "openai:gpt-4o-mini",
    instructions="You research topics and return detailed factual summaries.",
)

writer = Agent(
    "openai:gpt-4o-mini",
    instructions="You write engaging blog posts based on research summaries.",
)

# output_type=str keeps the editor's output as plain text for easy chaining
editor = Agent(
    "openai:gpt-4o-mini",
    output_type=str,
    instructions="You proofread and improve writing. Return the final polished text.",
)


# ── Orchestrator — coordinates the sub-agents and produces the final output ──
class FinalArticle(BaseModel):
    title: str
    body: str
    word_count: int


orchestrator = Agent(
    "openai:gpt-4o-mini",
    output_type=FinalArticle,
    instructions="You coordinate research, writing, and editing to produce articles.",
)


# ── Agent-as-tool pattern — sub-agents are registered as tools on the orchestrator ──
# The orchestrator calls these tools just like any other function tool
@orchestrator.tool_plain
async def research_topic(topic: str) -> str:
    """Research a topic and return a detailed summary."""
    result = await researcher.run(f"Research this topic in depth: {topic}")
    print("=" * 60)
    print(f"Research: {result}")
    return result.output


@orchestrator.tool_plain
async def write_article(research_summary: str) -> str:
    """Write a blog article from a research summary."""
    result = await writer.run(f"Write a blog post based on:\n{research_summary}")
    print("=" * 60)
    print(f"Writer: {result}")
    return result.output


@orchestrator.tool_plain
async def edit_article(draft: str) -> str:
    """Edit and polish an article draft."""
    result = await editor.run(f"Edit this draft:\n{draft}")
    print("=" * 60)
    print(f"Editor: {result}")
    return result.output


async def main():
    result = await orchestrator.run("Create a complete article about Pydantic AI for Python developers")
    article = result.output
    print("=" * 60)
    print(f"Title: {article.title}")
    print(f"Words: {article.word_count}")
    print(article.body[:500])


asyncio.run(main())
