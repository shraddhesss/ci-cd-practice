from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    # Check that it returns HTML now instead of JSON
    assert "text/html" in response.headers["content-type"]
    # Check that our specific website text is in the HTML
    assert "DevOps Dashboard" in response.text