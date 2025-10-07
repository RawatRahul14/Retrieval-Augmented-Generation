import pytest
from rag_pipeline.pipeline.data_extract import extract_data_pipeline


def test_extract_data_pipeline(tmp_path):
    """
    Tests the extract_data_pipeline function using a temporary session folder.
    """

    # === Prepare mock session folder ===
    session_folder = tmp_path / "session_001"
    session_folder.mkdir()

    # === Create a dummy text file ===
    (session_folder / "mock.txt").write_text("This is a mock document for testing.")

    # === Run the extraction pipeline ===
    texts, tables, metadata = extract_data_pipeline(session_folder=session_folder)

    # === Validate output types ===
    assert isinstance(texts, list), "❌ 'texts' should be a list."
    assert isinstance(tables, list), "❌ 'tables' should be a list."
    assert isinstance(metadata, list), "❌ 'metadata' should be a list."

    # === Validate content extraction ===
    assert len(texts) > 0, "❌ No text content extracted from mock file."

    print("✅ test_extract_data_pipeline passed!")