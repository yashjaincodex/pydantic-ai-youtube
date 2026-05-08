# ============================================================
# 04: Dependency Injection — Production-Grade Agents
# ============================================================

from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

load_dotenv()


# Dependencies are typed objects (dataclasses work great) passed at runtime
# Use them to inject DB connections, user context, API clients, etc.
@dataclass
class AppDeps:
    user_id: int
    user_name: str
    db_url: str  # In production: a real DB connection pool


# Define the structured response shape for the support agent
class SupportResponse(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    escalate_to_human: bool


# Tell the agent what dependency type to expect via deps_type
support_agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=AppDeps,
    output_type=SupportResponse,
    instructions="You are a helpful customer support agent.",
)


# @agent.instructions lets you generate dynamic instructions using deps at runtime
# RunContext[AppDeps] gives you type-safe access to the injected dependencies
@support_agent.instructions
def personalized_instructions(ctx: RunContext[AppDeps]) -> str:
    return f"Always greet the user as '{ctx.deps.user_name}'. User ID: {ctx.deps.user_id}"


# @agent.tool (not tool_plain) — this tool receives RunContext to access deps
@support_agent.tool
def get_user_orders(ctx: RunContext[AppDeps]) -> list[dict]:
    """Retrieve recent orders for the current user."""
    # In production: query DB using ctx.deps.db_url and ctx.deps.user_id
    return [
        {"order_id": "ORD-001", "item": "Laptop", "status": "Delivered"},
        {"order_id": "ORD-002", "item": "Headphones", "status": "Shipped"},
    ]


# Inject the deps at call time via the deps= parameter
deps = AppDeps(
    user_id=42,
    user_name="Yash",
    db_url="postgresql://localhost/mydb",
)
result = support_agent.run_sync(
    "Where is my last order?",
    deps=deps,
)
print(result.output.answer)
print(result.output.confidence)
print(f"Escalate: {result.output.escalate_to_human}")
