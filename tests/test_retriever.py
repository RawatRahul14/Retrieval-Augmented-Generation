import pytest
from pathlib import Path
from rag_pipeline.components.retriever import create_retriever

def test_create_retriever_with_texts(tmp_path):
    """
    Tests the create_retriever function with sample text chunks and no tables.
    """

    # === Prepare mock data ===
    texts = [
        {
            "content": "This is a mock text chunk for testing.",
            "metadata": {
                "source": "mock.txt"
            }
        }
    ]
    tables = []

    # === Run retriever creation ===
    retriever, save_path = create_retriever(
        texts = texts,
        tables = tables,
        session_id = "test_session"
    )

    # === Validate retriever and output path ===
    assert retriever is not None, "❌ Retriever should not be None."
    assert isinstance(save_path, Path), "❌ save_path must be a Path object."
    assert "test_session" in str(save_path), "❌ save_path does not contain session_id."

    print("✅ test_create_retriever_with_texts passed!")