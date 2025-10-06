# === Python Modules ===
from typing import TypedDict

# === Agent State ===
class AgentState(TypedDict):
    """
    State of the Agent that can be passed between calls.
    """
    ## === User Query ===
    question: str

    ## === Rephrased Question ===
    rephrased_question: str | None

    ## === Documents ===
    documents: list | None
    proceed_to_generate: bool