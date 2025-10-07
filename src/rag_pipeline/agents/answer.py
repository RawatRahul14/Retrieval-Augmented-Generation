# === AgentState ===
from rag_pipeline.agent_state import AgentState

# === BaseAnswerAgent ===
async def final_answer(
        state: AgentState
) -> AgentState:
    """
    Final answer agent that returns the final answer from the state.

    Args:
        state (AgentState): The current state of the agent.

    Returns:
        AgentState: The updated state with the final answer.
    """
    if state.get("fallback_used"):
        state["generated_answer"] = state.get("fallback_message")

    return state