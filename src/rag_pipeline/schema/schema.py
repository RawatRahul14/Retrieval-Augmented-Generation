# === Python Modules ===
from pydantic import BaseModel, Field

# === Query Rewriter Schema ===
class QueryRewrite(BaseModel):
    """
    Schema for the output of the query rewriter agent.
    """
    rephrased_question: str = Field(
        description = "The rephrased question that is more specific and context-aware."
    )