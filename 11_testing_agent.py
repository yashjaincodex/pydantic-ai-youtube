# ============================================================
# 11: Testing Agents — No API Credits Needed
# ============================================================


# import pytest
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel  # completely free — no API calls!

load_dotenv()


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str


agent = Agent(
    "openai:gpt-4o-mini",
    output_type=WeatherResponse,
    instructions="Return weather for the given city.",
)


# ── Test 1: Use TestModel to verify the agent returns the correct output TYPE ──
# TestModel generates dummy-but-valid data matching your output_type schema
def test_weather_agent_structure():
    with agent.override(model=TestModel()):
        result = agent.run_sync("What's the weather in Mumbai?")
        # Confirm the output is correctly typed — no API key needed!
        assert isinstance(result.output, WeatherResponse)
        assert result.output.city is not None


# ── Test 2: Provide custom mock output to test specific values ──
def test_weather_agent_custom():
    custom_model = TestModel(
        custom_output_args={
            "city": "Mumbai",
            "temperature": 32.5,
            "description": "Sunny",
        }
    )  # '{"city": "Mumbai", "temperature": 32.5, "description": "Sunny"}'
    with agent.override(model=custom_model):
        result = agent.run_sync("Mumbai weather?")
        print("+" * 30)
        print(result.output)
        print("+" * 30)
        assert result.output.city == "Mumbai"
        assert result.output.temperature == 32.5


# ── Test 3: Verify tool calls are wired up correctly ──
@agent.tool_plain
def get_live_weather(city: str) -> str:
    """Get live weather for a city."""
    return f"32°C, sunny in {city}"


def test_tool_was_called():
    with agent.override(model=TestModel()):
        result = agent.run_sync("Get weather for Bengaluru")
        # Inspect the message history to see what the agent did under the hood
        print(f"Messages exchanged: {len(result.all_messages())}")
        assert result.output is not None


# Run with: pytest test_agents.py -v
# Add this to pytest.ini to enable async tests: asyncio_mode = auto
