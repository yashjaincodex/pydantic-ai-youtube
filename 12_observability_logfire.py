# ============================================================
# 12: Observability with Pydantic Logfire
# ============================================================


import os

import logfire
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent

load_dotenv()

# Get your token from: https://logfire.pydantic.dev
logfire_token = os.getenv("LOGFIRE_TOKEN")
logfire.configure(
    token=logfire_token,
    service_name="youtube-demo",
)

# This single call instruments ALL agent runs automatically —
# traces, token usage, latency, tool calls, retries, and more
logfire.instrument_pydantic_ai()


class AnalysisResult(BaseModel):
    sentiment: str  # "positive" | "negative" | "neutral"
    score: float  # 0.0 (very negative) to 1.0 (very positive)
    keywords: list[str]  # key words that drove the sentiment


agent = Agent(
    "openai:gpt-4o-mini",
    output_type=AnalysisResult,
    instructions="Analyze text sentiment.",
)

# logfire.span() creates a trace span — everything inside is grouped in the dashboard
with logfire.span("analyze_customer_feedback"):
    result = agent.run_sync("I absolutely hare this product! Slow delivery and bad quality.")
    # Log structured data alongside the trace for easy filtering in the dashboard
    logfire.info(
        "Analysis complete",
        sentiment=result.output.sentiment,
        score=result.output.score,
    )

print(result.output)
# View traces, token costs, latency at: https://logfire.pydantic.dev
