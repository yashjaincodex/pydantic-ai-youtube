# ============================================================
# 07: Built-in Capabilities — Web Search & Reasoning
# ============================================================

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.capabilities import Thinking, WebSearch
from pydantic_ai.models.openai import OpenAIResponsesModel

load_dotenv()

# IMPORTANT: WebSearch requires OpenAIResponsesModel (OpenAI Responses API)
# The default "openai:gpt-4o-mini" shorthand uses the Chat Completions API
# which does NOT support native WebSearch — gpt-4o-mini also doesn't support it,
# so we use gpt-4o here specifically for WebSearch capability
responses_model = OpenAIResponsesModel("gpt-4o")

# Agent with web search — model will search the web before answering
search_agent = Agent(
    responses_model,
    instructions="Answer questions using up-to-date web information.",
    capabilities=[WebSearch()],
)

result = search_agent.run_sync("What are the top Python frameworks in 2025?")
print(result.output)

# Thinking capability — tells the model to reason before answering
# effort levels: 'minimal' | 'low' | 'medium' | 'high' | 'xhigh'
# o3-mini is OpenAI's dedicated reasoning model
thinking_agent = Agent(
    OpenAIResponsesModel("o3-mini"),
    instructions="Think step-by-step before answering complex questions.",
    capabilities=[Thinking(effort="high")],
)

result = thinking_agent.run_sync(
    "Solve: A train travels 120km at 60km/h, then 180km at 90km/h. What is the average speed?"
)
print(result.output)

# Web search with gpt-4o using Responses API
power_agent = Agent(
    OpenAIResponsesModel("gpt-4o"),
    capabilities=[WebSearch()],
)

result = power_agent.run_sync("Research the latest Pydantic AI release and explain its key new features.")
print(result.output)
