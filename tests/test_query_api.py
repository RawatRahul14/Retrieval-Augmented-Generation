from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_query_endpoint(monkeypatch):
    """
    Tests the /query/ endpoint using mocked retriever and LangGraph.
    """

    # === Mock retriever for session ===
    app.state.retrievers = {
        "session_001": "mock_retriever"
    }

    # === Mock LangGraph class ===
    class MockGraph:
        async def ainvoke(self, input, config):
            return {
                "generated_answer": "Mock answer for testing"
            }

    # === Inject mock graph into app state ===
    app.state.graph = MockGraph()

    # === Prepare mock user query payload ===
    payload = {
        "session_id": "session_001",
        "user_query": "What is RAG?"
    }

    # === Make POST request ===
    response = client.post("/query/", json=payload)

    # === Validate ===
    assert response.status_code == 200, "❌ Response code not 200."
    data = response.json()

    assert data["status"] == "success", "❌ Query failed unexpectedly."
    assert "answer" in data, "❌ 'answer' key missing in response."
    assert data["answer"] == "Mock answer for testing", "❌ Mock answer mismatch."

    print("✅ test_query_endpoint passed!")