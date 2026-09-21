from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert "compilerCoreInstalled" in body


def test_source_size_limit():
    response = client.post("/api/v1/compile", json={"source": "x" * 102401})
    assert response.status_code == 413
