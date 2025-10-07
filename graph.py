# === Python Modules ===
import os
from langgraph.graph.state import StateGraph
from langgraph.graph import END
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import AsyncMongoDBSaver
from pymongo import AsyncMongoClient

# === Agent State ===
from rag_pipeline.agent_state import AgentState

## === Question Rewriter ===
from rag_pipeline.agents.query_rewriter import query_rewriter

## === Document Retriever ===
from rag_pipeline.agents.doc_retriever import doc_retriever

## === Document Grader ===
from rag_pipeline.agents.grader import doc_grader

## === Answer Generation ===
from rag_pipeline.agents.generation import answer_generation

## === Fallback ===
from rag_pipeline.agents.fallback import fallback_agent

## === Final Answer ===
from rag_pipeline.agents.answer import final_answer

## === Routes ===
from rag_pipeline.router.routes import no_relevant_docs

load_dotenv()

# === Env Imports ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

def run_graph():
    """
    Runs the state graph for the RAG pipeline.
    """
    # === Initialize MongoDB Saver ===
    # === MongoClient ===
    mongo_client = AsyncMongoClient(MONGODB_URI)
    checkpointer = AsyncMongoDBSaver(
        client = mongo_client,
        db_name = DB_NAME,
        checkpoint_collection_name = COLLECTION_NAME
    )

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

    ## === 2. Retriever ===
    workflow.add_node(
        "doc_retriever_node",
        RunnableLambda(doc_retriever).with_config(
            {
                "run_async": True
            }
        )
    )

    ## === 3. Doc Grader ===
    workflow.add_node(
        "doc_grader_node",
        RunnableLambda(doc_grader).with_config(
            {
                "run_async": True
            }
        )
    )

    ## === 4. Generation ===
    workflow.add_node(
        "answer_generation_node",
        RunnableLambda(answer_generation).with_config(
            {
                "run_async": True
            }
        )
    )

    ## === 5. Fallback ===
    workflow.add_node(
        "fallback_agent_node",
        RunnableLambda(fallback_agent).with_config(
            {
                "run_async": True
            }
        )
    )

    ## === 6. Final Answer Node ===
    workflow.add_node(
        "final_answer_node",
        RunnableLambda(final_answer).with_config(
            {
                "run_async": True
            }
        )
    )

    workflow.set_entry_point("query_rewriter_node")
    workflow.add_edge("query_rewriter_node", "doc_retriever_node")
    workflow.add_edge("doc_retriever_node", "doc_grader_node")
    workflow.add_conditional_edges(
        "doc_grader_node",
        no_relevant_docs,
        {
            "generate_answer": "answer_generation_node",
            "fallback": "fallback_agent_node"
        }
    ) 
    workflow.add_edge("answer_generation_node", "final_answer_node")
    workflow.add_edge("fallback_agent_node", "final_answer_node")
    workflow.add_edge("final_answer_node", END)

    return workflow.compile(
        checkpointer = checkpointer
    )