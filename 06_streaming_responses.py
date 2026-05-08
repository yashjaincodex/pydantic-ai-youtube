# ============================================================
# 06: Streaming Responses — Real-Time Output
# ============================================================

import asyncio

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent

load_dotenv()

agent = Agent(
    "openai:gpt-4o-mini",
    instructions="You are a creative writer.",
)


# Stream plain text — delta=True gives you only the new chunk each iteration
async def stream_text():
    print("Streaming story:\n")
    # run_stream() returns a context manager — the stream is live inside the block
    async with agent.run_stream("Write a 3-sentence story about a robot") as stream:
        async for chunk in stream.stream_text(delta=True):
            # Print each chunk immediately without newline for live effect
            print(chunk, end="", flush=True)
    # Usage stats are available after the stream closes
    print("\n\nDone! Total usage:", stream.usage())


# Stream structured output — get partial Pydantic objects as they arrive
class BlogPost(BaseModel):
    title: str
    intro: str
    sections: list[str]
    conclusion: str


structured_agent = Agent(
    "openai:gpt-4o-mini",
    output_type=BlogPost,
)


async def stream_structured():
    async with structured_agent.run_stream("Write a blog post about Pydantic AI") as s:
        # stream_output() replaces the deprecated stream()
        # debounce_by=0.05 batches updates every 50ms — avoids too many re-renders
        async for partial in s.stream_output(debounce_by=0.05):
            print(f"\r[streaming] title={partial.title!r}", end="", flush=True)
        # get_output() returns the final fully validated BlogPost object
        final = await s.get_output()
        print(f"\n\nFinal title: {final.title}")
        print(f"Sections: {final.sections}")


asyncio.run(stream_text())
asyncio.run(stream_structured())
