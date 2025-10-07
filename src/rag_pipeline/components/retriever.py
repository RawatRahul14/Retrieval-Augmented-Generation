# === Python Modules ===
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
import os

# === Function to CREATE the FAISS Retriever ===
def create_retriever(
    texts: Optional[List[Dict[str, str]]] = None,
    tables: Optional[List[list]] = None,
    session_id: str = None,
    model_name: str = "text-embedding-3-small"
) -> Tuple[FAISS, Path]:
    """
    Creates a FAISS retriever index from extracted text (and optional table) chunks.

    Args:
        texts (List[Dict[str, str]], optional): Text chunks with metadata from extraction pipeline.
        tables (List[list], optional): Extracted tables (if any).
        save_path (Path): Directory path to save FAISS index.
        model_name (str): Embedding model name.

    Returns:
        Tuple[FAISS, Path]: The retriever object and the path where it's saved.
    """
    if not texts and not tables:
        raise ValueError("❌ No texts or tables provided. Please extract data first.")
    
    # === Data Directory ===
    DIR = Path("models")
    file_path = DIR / session_id

    # === Convert text data into LangChain Documents ===
    docs = []

    # === Add text chunks ===
    if texts:
        docs.extend([
            Document(
                page_content = item["content"],
                metadata = item["metadata"]
            )
            for item in texts if item.get("content")
        ])

    # === Add tables (flatten if any) ===
    if tables:
        for idx, table in enumerate(tables, start = 1):
            table_text = "\n".join([", ".join(map(str, row)) for row in table])
            docs.append(Document(
                page_content = table_text,
                metadata = {
                    "type": "table",
                    "table_id": idx
                }
            ))

    print(f"📚 Preparing {len(docs)} documents for indexing...")

    # === Initialize embeddings ===
    embeddings = OpenAIEmbeddings(
        model = model_name
    )

    # === Build FAISS index ===
    db = FAISS.from_documents(docs, embeddings)

    # === Ensure folder exists ===
    os.makedirs(file_path, exist_ok=True)

    # === Save the FAISS index ===
    db.save_local(str(file_path))
    print(f"✅ Retriever (FAISS index) created and saved at: {file_path}")

    # === Create the retriever object ===
    retriever = db.as_retriever(search_kwargs={"k": 5})

    return retriever, file_path