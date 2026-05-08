# ============================================================
# 05: Multi-Turn Conversations & Message History
# ============================================================


import asyncio

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessagesTypeAdapter

load_dotenv()

agent = Agent(
    "openai:gpt-4o-mini",
    instructions="You are a helpful tutor. Remember the conversation context.",
)


async def chat_session():
    # history holds the full message list from all previous turns
    history = []

    questions = [
        "What is a Python decorator?",
        "Can you show me a simple example?",
        "How is that different from a closure?",  # relies on previous context!
    ]

    for q in questions:
        print(f"\nUser: {q}")
        # Pass history so the agent remembers previous messages in this session
        result = await agent.run(q, message_history=history)
        print(f"Agent: {result.output}")
        # all_messages() returns ALL messages including this turn — save for next
        history = result.all_messages()

    # Serialize history to JSON bytes for persistent storage (DB, file, Redis, etc.)
    serialized = ModelMessagesTypeAdapter.dump_json(history)
    # Deserialize it back — full round-trip support
    loaded = ModelMessagesTypeAdapter.validate_json(serialized)
    print(f"\nConversation saved. Total messages: {len(loaded)}")


asyncio.run(chat_session())
