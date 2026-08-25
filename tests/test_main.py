from unittest.mock import patch
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch("server.main.generate_key_image")
@patch("server.main.send_image")
def test_update_state(mock_send_image, mock_generate_key_image):
    mock_generate_key_image.return_value = b"mock_image_bytes"
    payload = {"llm": "claude", "h5": 80, "weekly": 45, "monthly": 10}
    response = client.post("/update", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "updated"
    assert data["light"] == "YELLOW"
    
    mock_generate_key_image.assert_called_once_with("claude", "YELLOW")
    mock_send_image.assert_called_once_with(1, b"mock_image_bytes")
