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


@agent.tool_plain
def roll_dice(sides: int = 6) -> int:
    """Roll a die with the given number of sides."""
    result = random.randint(1, sides)
    print(f"Roll Dice Tool Result: {result}")
    return result


@agent.tool_plain
def get_weather(city: str) -> str:
    """Get the current weather for a city (mock)."""
    result = f"Weather in {city}: 28°C, partly cloudy"
    print(f"Get Weather Tool Result: {result}")
    return result


@agent.tool_plain
def calculate(expression: str) -> float:
    """Evaluate a basic math expression like '2 + 2 * 3'."""
    result = eval(expression, {"__builtins__": {}})  # Use safer eval in prod!
    print(f"Calculate Tool Result: {result}")
    return result


result = agent.run_sync("Roll a 20-sided die, get the weather in Bengaluru, and calculate 15 * 7 + 3")
print("\n=== Final Output ===")
print(result.output)
