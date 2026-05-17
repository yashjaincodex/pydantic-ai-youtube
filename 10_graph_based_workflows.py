# ============================================================
# 10: Graph-Based Workflows — Complex Control Flow
# ============================================================

from __future__ import annotations

import asyncio
from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic_ai import Agent

# Graph lives in the standalone `pydantic_graph` package (underscore, not dot)
# It is installed automatically with pydantic-ai — no extra pip install needed
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

load_dotenv()


# ── Shared state object — all nodes read from and write to this ──
@dataclass
class ResearchState:
    topic: str
    research: str = ""
    draft: str = ""
    revision_count: int = 0
    final: str = ""


# ── Each node is a dataclass that implements a run() method ──
# Nodes return the NEXT node to run — this is how the graph flows


@dataclass
class ResearchNode(BaseNode[ResearchState]):
    async def run(self, ctx: GraphRunContext[ResearchState]) -> WriteNode:
        # Research the topic and store result in shared state
        print("Research starts")
        agent = Agent(
            "openai:gpt-4o-mini",
            instructions="Research topics thoroughly.",
        )
        result = await agent.run(f"Research: {ctx.state.topic}")
        ctx.state.research = result.output
        print("Research end")
        return WriteNode()  # always proceeds to writing


@dataclass
class WriteNode(BaseNode[ResearchState]):
    async def run(self, ctx: GraphRunContext[ResearchState]) -> ReviewNode:
        # Use the research from state to write a draft
        print("Writing starts")
        agent = Agent(
            "openai:gpt-4o-mini",
            instructions="Write clear articles.",
        )
        result = await agent.run(f"Write article based on:\n{ctx.state.research}")
        ctx.state.draft = result.output
        print("Writing end")
        return ReviewNode()  # always proceeds to review


@dataclass
class ReviewNode(BaseNode[ResearchState]):
    # Return type union — this node can branch: loop back OR end the graph
    async def run(self, ctx: GraphRunContext[ResearchState]) -> WriteNode | End[str]:
        print("Review starts")
        agent = Agent(
            "openai:gpt-4o-mini",
            output_type=bool,
            instructions="Review articles. Return True if good, False if needs revision.",
        )
        result = await agent.run(f"Is this article publication-ready?\n{ctx.state.draft}")

        # Stop if approved OR if we've already revised twice (avoid infinite loops)
        if result.output or ctx.state.revision_count >= 2:
            ctx.state.final = ctx.state.draft
            print("Review end")
            return End(ctx.state.final)  # End the graph, return the final article
        else:
            # Not good enough — increment counter and send back for rewriting
            ctx.state.revision_count += 1
            ctx.state.research += "\n\nNeeds improvement: add more examples and depth."
            print("Review end")
            return WriteNode()


async def main():
    # Register all nodes with the graph
    graph = Graph(nodes=[ResearchNode, WriteNode, ReviewNode])
    state = ResearchState(topic="Harry Potter Books vs Movies!")
    # graph.run() returns a GraphRunResult
    # Access the final value from End() via result.output
    run_result = await graph.run(ResearchNode(), state=state)
    print(f"Revisions needed: {state.revision_count}")
    print(f"Article preview: {run_result.output}")


asyncio.run(main())
