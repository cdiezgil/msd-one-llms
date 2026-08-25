from unittest.mock import patch
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch("server.main.send_image")
def test_update_state(mock_send_image):
    payload = {"llm": "claude", "h5": 80, "weekly": 45, "monthly": 10}
    response = client.post("/update", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "updated"
    assert data["light"] == "YELLOW"
    
    mock_send_image.assert_called_once()
    args, _ = mock_send_image.call_args
    assert args[0] == 1
    assert isinstance(args[1], bytes)
