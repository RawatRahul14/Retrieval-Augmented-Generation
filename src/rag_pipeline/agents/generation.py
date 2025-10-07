# === Python Modules ===
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# === Agent State ===
from rag_pipeline.agent_state import AgentState

# === Components ===
from rag_pipeline.components.prompts import render_prompt
from rag_pipeline.components.models import ModelConfig

# === Schema ===
from rag_pipeline.schema.schema import AnswerGeneration

# === Utils ===
from rag_pipeline.utils.conversation import update_recent_chats

# === Answer Generation Agent ===
async def answer_generation(
        state: AgentState
) -> AgentState:
    """
    Generates the final answer based on the rephrased question and relevant documents.

    Args:
        state (AgentState): The current state of the agent containing the rephrased question and documents.

    Returns:
        AgentState: The updated state with the generated answer.
    """
    ## === Render Prompt ===
    prompt = render_prompt(
        prompt_name = "answer_generation",
        user_query = state.get("rephrased_question"),
        documents = state.get("documents")
    )

    ## === Load Model Configuration ===
    model = ModelConfig()
    model_name = model.get_agent_model(
        agent_name = "answer_generation"
    ).get("name")

    # === Initialize Language Model ===
    llm = ChatOpenAI(
        model_name = model_name,
        temperature = 0.0
    ).with_structured_output(AnswerGeneration)

    message = [
        SystemMessage(content = prompt["system"]),
        HumanMessage(content = prompt["user"])
    ]

    response = await llm.ainvoke(
        message
    )

    ## === Outputs ===
    state["generated_answer"] = response.answer
    state["messages"] = update_recent_chats(
        recent_chats = state.get("messages", []),
        latest_question = state.get("rephrased_question"),
        latest_answer = response.answer_history
    )

    return state