# ============================================================
# 01: What is Pydantic AI? — Setup & Your First Agent
# ============================================================

import asyncio

from dotenv import load_dotenv
from pydantic_ai import Agent

load_dotenv()  # loads OPENAI_API_KEY from .env

# Simplest possible agent
agent = Agent(
    "openai:gpt-4o-mini",
    instructions="You are a helpful assistant. Be concise.",  # System Prompt
)

# Synchronous run (great for scripts)
print("== Synchronous Run ==")
result = agent.run_sync("What is the capital of India?")
print(result.output)


# Asynchronous run (great for production)
async def main():
    result = await agent.run("What is the difference between Pydantic Validation vs Pydantic AI?")
    print(result.output)


print("== Asynchronous Run ==")
asyncio.run(main())
