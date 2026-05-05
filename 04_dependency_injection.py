# ============================================================
# 04: Dependency Injection — Production-Grade Agents
# ============================================================

from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

load_dotenv()


@dataclass
class AppDeps:
    user_id: int
    user_name: str
    db_url: str


class SupportResponse(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    escalate_to_human: bool


support_agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=AppDeps,
    output_type=SupportResponse,
    instructions="You are a helpful customer support agent.",
)


@support_agent.instructions
def personalized_instructions(ctx: RunContext[AppDeps]) -> str:
    return f"Always greet the user as '{ctx.deps.user_name}'. User ID: {ctx.deps.user_id}"


@support_agent.tool
def get_user_orders(ctx: RunContext[AppDeps]) -> list[dict]:
    """Retrieve recent orders for the current user."""
    return [
        {"order_id": "ORD-001", "item": "Laptop", "status": "Delivered"},
        {"order_id": "ORD-002", "item": "Headphones", "status": "Shipped"},
    ]


deps = AppDeps(
    user_id=42,
    user_name="Yash",
    db_url="postgresql://localhost/mydb",
)
result = support_agent.run_sync(
    # "Where is my last order?",
    "How many orders delivered? Provide name of the order! and Also mention the user name",
    deps=deps,
)
print(result.output.answer)
print(f"Escalate: {result.output.escalate_to_human}")
