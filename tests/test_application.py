
import json
from src.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from requests.exceptions import HTTPError
from .mocks.mocked_api_response import MockedResponse

client = TestClient(app)


def test_app_creation():
    """Testing app creation"""
    response = client.get("/")
    assert response.status_code == 200
