# === AgentState ===
from rag_pipeline.agent_state import AgentState

# === Fallback BaseAgent ===
async def fallback_agent(
        state: AgentState
) -> AgentState:
    """
    A fallback agent that responds with a default message when no relavant documents are found.
    """
    state["fallback_message"] = "I'm sorry, I couldn't find any relevant information to answer your question. Can you please provide more details."
    state["fallback_used"] = True

    return state