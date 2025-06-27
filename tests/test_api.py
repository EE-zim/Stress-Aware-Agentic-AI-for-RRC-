"""API endpoint tests."""
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_status_endpoint():
    resp = client.get("/status")
    assert resp.status_code == 200
    assert resp.json()["status"] == "idle"
