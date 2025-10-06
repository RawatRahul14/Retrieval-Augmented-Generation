# === Python Modules ===
import os
from langgraph.graph.state import StateGraph
from langgraph.graph import END
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv

# === Agent State ===
from rag_pipeline.agent_state import AgentState

## === Question Rewriter ===
from rag_pipeline.agents.query_rewriter import query_rewriter

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def run_graph():
    """
    Runs the state graph for the RAG pipeline.
    """
    # === Initialize the state graph ===
    workflow = StateGraph(AgentState)

    # === Nodes ===
    ## === 1. Rewriter ===
    workflow.add_node(
        "query_rewriter_node",
        RunnableLambda(query_rewriter).with_config(
            {
                "run_async": True
            }
        )
    )

    workflow.set_entry_point("query_rewriter_node")
    workflow.add_edge("query_rewriter_node", END)

    return workflow.compile()