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
        save_path: Path = Path("vector_index/faiss_index"),
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
                metadata = {"type": "table", "table_id": idx}
            ))

    print(f"📚 Preparing {len(docs)} documents for indexing...")

    # === Initialize embeddings ===
    embeddings = OpenAIEmbeddings(model = model_name)

    # === Build FAISS index ===
    db = FAISS.from_documents(docs, embeddings)

    # === Create folder if missing and save ===
    os.makedirs(
        save_path,
        exist_ok = True
    )
    db.save_local(str(save_path))

    print(f"✅ Retriever (FAISS index) created and saved at: {save_path}")

    # === Create the retriever object ===
    retriever = db.as_retriever(
        search_kwargs = {
            "k": 5
        }
    )
    return retriever, save_path