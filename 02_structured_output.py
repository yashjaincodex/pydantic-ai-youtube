# ============================================================
# 02: Structured Outputs — Type-Safe LLM Responses
# ============================================================


from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent

load_dotenv()


# Define a Pydantic model to represent the shape of the LLM's response
# Field() lets us add validation rules and descriptions for each field
class MovieReview(BaseModel):
    title: str
    rating: float = Field(ge=0, le=10, description="Rating out of 10")
    summary: str = Field(max_length=200)
    pros: list[str]
    cons: list[str]
    recommended: bool


# Pass the model class as output_type — Pydantic AI forces the LLM to return
# valid JSON matching this schema, and validates it automatically
agent = Agent(
    "openai:gpt-4o-mini",
    output_type=MovieReview,
    instructions="You are a movie critic. Provide detailed reviews.",
)

result = agent.run_sync("Review the movie Inception")

# result.output is already a fully validated MovieReview Python object!
review = result.output
print(f"Title:  {review.title}")
print(f"Rating: {review.rating}/10")
print(f"Pros:   {review.pros}")
print(f"Recommended: {review.recommended}")

# If the LLM returns invalid/malformed data, Pydantic AI automatically
# retries the request with the validation errors fed back to the model
