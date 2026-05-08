# ============================================================
# 03: Tools & Function Calling
# ============================================================

import random

from dotenv import load_dotenv
from pydantic_ai import Agent

load_dotenv()

agent = Agent(
    "openai:gpt-4o-mini",
    instructions="You are a helpful assistant with tool access.",
)


# @agent.tool_plain — a simple tool that doesn't need access to agent context or deps
# Pydantic AI auto-generates the JSON schema from type hints + docstring
@agent.tool_plain
def roll_dice(sides: int = 6) -> int:
    """Roll a die with the given number of sides."""
    return random.randint(1, sides)


# Another plain tool — in production you'd call a real weather API here
@agent.tool_plain
def get_weather(city: str) -> str:
    """Get the current weather for a city (mock)."""
    return f"Weather in {city}: 28°C, partly cloudy"


# Tools can also do math, call databases, call APIs — anything Python can do
@agent.tool_plain
def calculate(expression: str) -> float:
    """Evaluate a basic math expression like '2 + 2 * 3'."""
    return eval(expression, {"__builtins__": {}})  # Use safer eval in prod!


# The LLM decides which tools to call, in what order, based on the user message
result = agent.run_sync("Roll a 20-sided die, get the weather in Bengaluru, and calculate 15 * 7 + 3")
print(result.output)
