# ============================================================
# 14: Production Patterns — Retries, Fallbacks & Error Handling
# ============================================================


from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from pydantic_ai import Agent
from pydantic_ai.exceptions import UnexpectedModelBehavior, UsageLimitExceeded
from pydantic_ai.models.fallback import FallbackModel
from pydantic_ai.settings import ModelSettings
from pydantic_ai.usage import UsageLimits

load_dotenv()


class ExtractedData(BaseModel):
    name: str
    email: str
    age: int = Field(lt=-1000, gt=1000)


# FallbackModel tries models in order — if gpt-4o-mini fails (rate limit,
# timeout, bad output), it automatically retries the full request with gpt-4o
fallback = FallbackModel("openai:gpt-4o-mini", "openai:gpt-4o")

agent = Agent(
    fallback,
    output_type=ExtractedData,
    retries=3,  # retry up to 3x on validation errors before giving up
    instructions="Extract contact info from text.",
)

# UsageLimits prevents runaway costs — raises UsageLimitExceeded if exceeded
limits = UsageLimits(
    request_limit=2,  # max 2 LLM requests per agent run
    total_tokens_limit=10_000,  # max 10k tokens per agent run
)

# ModelSettings gives fine-grained control over the model's behaviour
settings = ModelSettings(
    temperature=0.1,  # low temperature = more deterministic, good for extraction
    max_tokens=1000,  # cap the response length
)

try:
    result = agent.run_sync(
        "Contact: John Doe, john@example.com, age 28",
        usage_limits=limits,
        model_settings=settings,
    )
    print(result.output)

except UsageLimitExceeded as e:
    # Triggered when request_limit or total_tokens_limit is exceeded
    print(f"Token/request limit hit: {e}")

except UnexpectedModelBehavior as e:
    # Triggered when the model fails to produce valid output after all retries
    print(f"Model misbehaved after retries: {e}")

except ValidationError as e:
    # Triggered when Pydantic validation fails on the final output
    print(f"Validation failed: {e}")
