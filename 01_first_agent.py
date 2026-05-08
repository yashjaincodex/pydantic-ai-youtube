# ============================================================
# 01: What is Pydantic AI? — Setup & Your First Agent
# ============================================================


import asyncio

from dotenv import load_dotenv
from pydantic_ai import Agent

# Load the OPENAI_API_KEY from the .env file
load_dotenv()

# Create the simplest possible agent — just a model name + instructions
agent = Agent(
    "openai:gpt-4o-mini",
    instructions="You are a helpful assistant. Be concise.",
)

# run_sync() is great for simple scripts — blocks until the response is ready
result = agent.run_sync("What is the capital of India?")
print(result.output)


# For production apps, always use the async version inside an async function
async def main():
    result = await agent.run("Explain Pydantic AI in one sentence.")
    print(result.output)


asyncio.run(main())
