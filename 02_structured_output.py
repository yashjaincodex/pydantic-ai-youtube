# ============================================================
# 02: Structured Outputs — Type-Safe LLM Responses
# ============================================================


from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent

load_dotenv()


class MovieReview(BaseModel):
    title: str
    rating: float = Field(ge=0, le=10, description="Rating out of 10")
    summary: str = Field(max_length=50)
    pros: list[str]
    cons: list[str]
    recommended: bool


agent = Agent(
    "openai:gpt-4o-mini",
    output_type=MovieReview,  # <-- structured output
    instructions="You are a movie critic. Provide detailed reviews.",
)

result = agent.run_sync("Review the movie Disaster Movie")
review = result.output  # Already a validated MovieReview object!

print(f"Title:          {review.title}")
print(f"Rating:         {review.rating}/10")
print(f"Summary:        {review.summary}")
print(f"Pros:           {review.pros}")
print(f"Cons:           {review.cons}")
print(f"Recommended:    {review.recommended}")

# If LLM returns invalid data, Pydantic AI auto-retries with validation errors!
