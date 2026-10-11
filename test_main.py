from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Command Center" in response.text

def test_metrics_api():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "cpu" in response.json()
    assert "ram" in response.json()