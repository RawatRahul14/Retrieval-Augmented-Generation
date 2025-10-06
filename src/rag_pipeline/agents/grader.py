# === Python Modules ===
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# === Agent State ===
from rag_pipeline.agent_state import AgentState

# === Components ===
from rag_pipeline.components.prompts import render_prompt
from rag_pipeline.components.models import ModelConfig

# === Schema ===
from rag_pipeline.schema.schema import DocGrader

# === Main Agent Body ===
async def doc_grader(
        state: AgentState
) -> AgentState:
    """
    Grades the relevance of retrieved documents to the user's query.

    Args:
        state (AgentState): The current state of the agent, including the user's question and retrieved documents.

    Returns:
        AgentState: The updated state with graded documents.
    """
    relavant_docs: list = []
    for document in state.get("documents"):
        ## === Prompt ===
        prompt = render_prompt(
            prompt_name = "retrieval_grader",
            question = state.get("rephrased_question"),
            document = document.page_content
        )

        ## === Get Model ===
        model = ModelConfig()
        model_name = model.get_agent_model(
            agent_name = "retrieval_grader"
        ).get("name")

        ## === LLM ===
        llm = ChatOpenAI(
            model = model_name,
            temperature = 0.0
        ).with_structured_output(DocGrader)

        messages = [
            SystemMessage(content = prompt["system"]),
            HumanMessage(content = prompt["user"])
        ]

        response = await llm.ainvoke(
            messages
        )

        if response.score.strip().lower() == "yes":
            relavant_docs.append(document)
    
    ## === Output ===
    state["documents"] = relavant_docs
    state["proceed_to_generate"] = len(relavant_docs) > 0

    return state