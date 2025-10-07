# === Python Modules ===
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# === Agent State ===
from rag_pipeline.agent_state import AgentState

# === Components ===
from rag_pipeline.components.prompts import render_prompt
from rag_pipeline.components.models import ModelConfig

# === Schema ===
from rag_pipeline.schema.schema import QueryRewrite

# === Utils ===
from rag_pipeline.utils.conversation import format_conversation_for_llm

# === Main Agent Body ===
async def query_rewriter(
        state: AgentState
) -> AgentState:
    """
    Rewrites the user's query to be more specific and context-aware.
    """
    ## === Rephrased Question ===
    state["rephrased_question"] = None

    ## === Current Question ===
    current_question: str = state.get("question", "")

    ## === Document List ===
    state["documents"] = []

    ## === Fallback Message ===
    state["fallback_message"] = None
    state["fallback_used"] = False

    ## === Flag to proceed further ===
    state["proceed_to_generate"] = False

    ## === Generated Answer ===
    state["generated_answer"] = None

    ## === Conversation ===
    if "messages" not in state or state["messages"] is None:
        state["messages"] = []

    ## === Convert Conversation to appropriate form ===
    conversation = format_conversation_for_llm(
        recent_chats = state.get("messages", {})
    )

    ## === Prompt ===
    prompt = render_prompt(
        prompt_name = "question_rewriter",
        current_question = current_question,
        conversation = conversation
    )

    ## === Get Model ===
    model = ModelConfig()
    model_name = model.get_agent_model(
        agent_name = "question_rewriter"
    ).get("name")

    ## === LLM ===
    llm = ChatOpenAI(
        model = model_name,
        temperature = 0.0
    ).with_structured_output(QueryRewrite)

    messages = [
        SystemMessage(content = prompt["system"]),
        HumanMessage(content = prompt["user"])
    ]

    response = await llm.ainvoke(
        messages
    )

    ## === Output ===
    state["rephrased_question"] = response.rephrased_question

    return state