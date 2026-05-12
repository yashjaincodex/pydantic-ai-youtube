# ============================================================
# 07: Built-in Capabilities — Web Search & Reasoning
# ============================================================

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.capabilities import Thinking, WebSearch

# from pydantic_ai.models.openai import OpenAIResponsesModel

load_dotenv()

# IMPORTANT: WebSearch requires OpenAIResponsesModel (OpenAI Responses API)
# The default "openai:gpt-4o-mini" shorthand uses the Chat Completions API
# which does NOT support native WebSearch — gpt-4o-mini also doesn't support it,
# so we use gpt-4o here specifically for WebSearch capability
# responses_model = OpenAIResponsesModel("gpt-4o")

# Agent with web search — model will search the web before answering
search_agent = Agent(
    "gpt-4o",
    instructions="Answer questions using up-to-date web information.",
    capabilities=[WebSearch()],
)

result = search_agent.run_sync("What is Pydantic AI and when it was released?")
print("=" * 60)
# print(result.output)

# Thinking capability — tells the model to reason before answering
# effort levels: 'minimal' | 'low' | 'medium' | 'high' | 'xhigh'
# o3-mini is OpenAI's dedicated reasoning model
thinking_agent = Agent(
    "o3-mini",
    instructions="Think step-by-step before answering complex questions.",
    capabilities=[Thinking(effort="high")],
)

result = thinking_agent.run_sync(
    "Solve: A train travels 120km at 60km/h, then 180km at 90km/h. What is the average speed?"
)
print("=" * 60)
# print(result.output)

# Web search with gpt-4o using Responses API
power_agent = Agent(
    "gpt-4o",
    capabilities=[WebSearch()],
)

result = power_agent.run_sync("Provide the Release Dates for all Harry Potter Movies along with there names!")
print("=" * 60)
print(result.output)
