from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_update_state():
    payload = {"llm": "claude", "h5": 80, "weekly": 45, "monthly": 10}
    response = client.post("/update", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "updated"
    assert data["light"] == "YELLOW"
