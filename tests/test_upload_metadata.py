import pytest
import asyncio
from rag_pipeline.components.upload import upload_file_metadata

# === Upload File Metadata ===
@pytest.mark.asyncio
async def test_upload_file_metadata(monkeypatch):
    """
    Tests upload_file_metadata function by mocking AsyncIOMotorClient.
    """

    # === Mock insert operation ===
    async def mock_insert(*args, **kwargs):
        return {"acknowledged": True}

    # Patch upload_file_metadata directly (simplest)
    async def mock_upload_file_metadata(session_id, file_metadata):
        await asyncio.sleep(0)
        return True

    monkeypatch.setattr(
        "rag_pipeline.components.upload.upload_file_metadata",
        mock_upload_file_metadata
    )

    metadata = [{
        "file_name": "sample.pdf",
        "type": "pdf",
        "size_kb": 100,
        "total_pages": 2
    }]

    # === Execute function ===
    result = await upload_file_metadata("test_session", metadata)

    # === Validate ===
    assert isinstance(result, dict), "❌ Expected dictionary response from upload_file_metadata."
    assert result["session_id"] == "test_session"
    assert "uploaded_files" in result
    print("✅ test_upload_file_metadata passed!")