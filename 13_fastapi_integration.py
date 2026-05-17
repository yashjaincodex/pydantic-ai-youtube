# ============================================================
# 13: FastAPI Integration — Production REST API
# ============================================================


from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_ai import Agent

load_dotenv()

app = FastAPI(title="Pydantic AI API")


# ── Request / Response schemas (separate from agent output schemas) ──
class ChatRequest(BaseModel):
    message: str
    user_id: int = 1


class ChatResponse(BaseModel):
    reply: str
    usage_tokens: int  # expose token usage so clients can track costs


class SummaryRequest(BaseModel):
    text: str


# Pydantic Model for Agent
class SummaryResponse(BaseModel):
    summary: str
    key_points: list[str]
    word_count: int


# ── Agents — defined once at module level, reused across all requests ──
chat_agent = Agent(
    "openai:gpt-4o-mini",
    instructions="You are a helpful assistant.",
)

# This agent returns a structured SummaryResponse directly
summary_agent = Agent(
    "openai:gpt-4o-mini",
    output_type=SummaryResponse,
    instructions="Summarize text into structured format.",
)


# ── Endpoints ──
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        result = await chat_agent.run(req.message)
        return ChatResponse(
            reply=result.output,
            usage_tokens=result.usage().total_tokens,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summarize", response_model=SummaryResponse)
async def summarize(req: SummaryRequest):
    # result.output is already a SummaryResponse — return it directly
    result = await summary_agent.run(req.text)
    return result.output


# Run with: uvicorn video13_fastapi:app --reload
