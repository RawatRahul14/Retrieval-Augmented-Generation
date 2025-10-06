# === Python Modules ===
from pydantic import BaseModel, Field
from typing import Literal

# === Query Rewriter Schema ===
class QueryRewrite(BaseModel):
    """
    Schema for the output of the query rewriter agent.
    """
    rephrased_question: str = Field(
        description = "The rephrased question that is more specific and context-aware."
    )

class DocGrader(BaseModel):
    """
    Schema for the output of the document grader agent.
    """
    score: Literal["Yes", "No"] = Field(
        description = "Document is relevant to the question? If yes -> 'Yes' if not -> 'No'"
    )