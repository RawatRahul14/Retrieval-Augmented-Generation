# === Python Modules ===
import uuid
from pathlib import Path
from typing import List
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import aiofiles

# === Local Imports ===
from rag_pipeline.pipeline.data_extract import extract_data_pipeline
from rag_pipeline.components.upload import upload_file_metadata
from rag_pipeline.components.retriever import create_retriever

# === Schema Imports ===
from src.rag_pipeline.schema.response import (
    UploadResponse,
    UserQueryResponse
)
from rag_pipeline.schema.requests import QueryRequest

# === Graph Compiler ===
from graph import run_graph

# === Load ENV ===
load_dotenv()

## === Startup event ===
@asynccontextmanager
async def lifespan(
    app: FastAPI
):
    """
    Initiates the graph
    """
    print("Starting up the graph...")
    app.state.graph = run_graph()
    yield
    print("Shutting down the graph...")

# === Initialize FastAPI ===
app = FastAPI(
    title = "Retrieval-Augmented Generation API",
    version = "1.0",
    lifespan = lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# === Base Data Directory ===
BASE_DATA_PATH = Path("data")
BASE_DATA_PATH.mkdir(
    exist_ok = True
)

# === Upload Endpoint ===
@app.post("/upload/", response_model = UploadResponse)
async def upload_files(
    session_id: str = Form(None),
    files: List[UploadFile] = File(...)
):
    """
    Upload multiple files into a session-specific folder inside `data/`.
    If no session_id is provided, a new one is generated.
    Extracts metadata and stores it in MongoDB.
    """
    # === Generate session_id if not provided ===
    if not session_id:
        session_id = f"session_{uuid.uuid4().hex[:8]}"

    # === Create a folder for this session ===
    session_folder = BASE_DATA_PATH / session_id
    session_folder.mkdir(
        parents = True,
        exist_ok = True
    )

    saved_files = []

    try:
        # === Save all uploaded files asynchronously ===
        for file in files:
            file_path = session_folder / file.filename
            async with aiofiles.open(
                file_path,
                "wb"
            ) as f:
                await f.write(await file.read())
            saved_files.append(file.filename)

        # === Extract text, tables, metadata from ONLY this session folder ===
        texts, tables, metadata = extract_data_pipeline(
            session_folder = Path(session_folder)
        )

        # === Create retriever for this session ===
        retriever, _ = create_retriever(
            texts = texts,
            tables = tables,
            session_id = session_id
        )

        # === Store retriever in FastAPI app state ===
        if not hasattr(app.state, "retrievers"):
            app.state.retrievers = {}

        app.state.retrievers[session_id] = retriever

        # === Upload metadata to MongoDB ===
        await upload_file_metadata(
            session_id = session_id,
            file_metadata = metadata
        )

        return UploadResponse(
            status =  "success",
            session_id = session_id,
            saved_path = str(session_folder.resolve()),
            uploaded_file = ", ".join(saved_files),
            message = f"✅ Uploaded {len(saved_files)} files for session '{session_id}'."
        )

    except Exception as e:
        return UploadResponse(
            status = "failure",
            session_id = session_id,
            message = f"❌ Error in uploading files: {str(e)}"
        )

# === User Query Endpoint ===
@app.post("/query/", response_model=UserQueryResponse)
async def user_query(request: QueryRequest):
    """
    Handles user query for a given session_id.
    Executes the LangGraph RAG pipeline using the retriever associated with that session.
    """
    try:
        session_id = request.session_id
        user_query = request.user_query

        retriever = app.state.retrievers[session_id]

        # === Step 1: Access pre-initialized LangGraph ===
        if not hasattr(app.state, "graph"):
            return UserQueryResponse(
                status = "failure",
                session_id = session_id,
                message = "LangGraph not initialized. Please restart the server."
            )

        graph = app.state.graph

        # === Step 2: Run the RAG pipeline ===
        response = await graph.ainvoke(
            input = {"question": user_query},
            config = {
                "configurable": {
                    "retriever": retriever,
                    "thread_id": session_id
                }
            }
        )

        # === Step 3: Extract structured output ===
        answer = response.get("generated_answer", "No answer generated.")

        return UserQueryResponse(
            status = "success",
            session_id = session_id,
            answer = answer
        )

    except Exception as e:
        import traceback
        print("⚠️ Error during query:", traceback.format_exc())
        return UserQueryResponse(
            status = "failure",
            message = f"Error while processing query: {e}"
        )