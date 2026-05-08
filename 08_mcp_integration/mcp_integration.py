# ============================================================
# 08: MCP (Model Context Protocol) Integration
# ============================================================


import asyncio

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerSSE, MCPServerStdio

load_dotenv()


# ── APPROACH 1: Stdio (local subprocess) ─────────────────────
# MCPServerStdio launches mcp_server.py as a subprocess
# and communicates via stdin/stdout — no network port needed
async def agent_with_stdio_mcp():
    # Point to the local server file — Pydantic AI manages its lifecycle
    mcp_server = MCPServerStdio("python", args=["08_mcp_integration/mcp_server.py"])

    # Use toolsets= (replaces deprecated mcp_servers=)
    # The agent automatically discovers all tools exposed by the MCP server
    agent = Agent(
        "openai:gpt-4o-mini",
        instructions=(
            "You are a math assistant. Use the available tools to solve problems. " "Show your working step by step."
        ),
        toolsets=[mcp_server],
    )

    # Use the agent as a context manager to manage the server subprocess lifecycle
    async with agent:
        result = await agent.run(
            "Calculate: (3 + 7) * 4, then raise the result to the power of 2. "
            "Also summarize the numbers [10, 20, 30, 40, 50]."
        )
        print(result.output)


# ── APPROACH 2: SSE (remote server over HTTP) ─────────────────
# MCPServerSSE connects to a running MCP server via HTTP + Server-Sent Events
# Use this when your MCP server runs on a remote machine or a separate process
async def agent_with_sse_mcp():
    # The server must already be running at this URL before this is called
    # e.g. run: fastmcp run mcp_server.py --transport sse --port 8000
    mcp_server = MCPServerSSE(url="http://localhost:8000/sse")

    agent = Agent(
        "openai:gpt-4o-mini",
        instructions="You are a math assistant with remote tool access.",
        toolsets=[mcp_server],  # toolsets= replaces deprecated mcp_servers=
    )

    async with agent:
        result = await agent.run("What is 12 multiplied by 15?")
        print(result.output)


# Run the stdio example (no server process needed separately — agent starts it)
asyncio.run(agent_with_stdio_mcp())
