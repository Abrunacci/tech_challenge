from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_app_creation():
    """Testing app creation"""
    response = client.get("/")
    assert response.status_code == 200
