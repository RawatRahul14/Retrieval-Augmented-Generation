from fastapi.testclient import TestClient
from main import app
import io

client = TestClient(app)

# === Upload Endpoint ===
def test_upload_endpoint(monkeypatch):
    """
    Tests the /upload/ endpoint by mocking all file-processing logic.
    """

    # === Mock data extraction ===
    monkeypatch.setattr(
        "main.extract_data_pipeline",
        lambda session_folder: (
            [{"content": "mock text", "metadata": {"source": "mock.pdf"}}],
            [],
            [{"file_name": "mock.pdf"}]
        )
    )

    # === Mock retriever creation ===
    monkeypatch.setattr(
        "main.create_retriever",
        lambda texts, tables, session_id = None: ("mock_retriever", "mock_path")
    )

    # === Mock metadata upload ===
    async def mock_upload_metadata(session_id, file_metadata):
        return None

    monkeypatch.setattr("main.upload_file_metadata", mock_upload_metadata)

    # === Prepare file for upload (matching FastAPI param name: 'files') ===
    file_content = io.BytesIO(b"fake content")
    files = [
        ("files", ("mock.pdf", file_content, "application/pdf"))
    ]

    # === Make POST request ===
    response = client.post("/upload/", files = files)

    # === Validate ===
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert "session_id" in data
    assert "uploaded_file" in data
    assert data["uploaded_file"].endswith(".pdf")
    assert "✅ Uploaded" in data["message"]
    print("✅ test_upload_endpoint passed!")