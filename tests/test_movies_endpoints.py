
import json
from os import environ

from src.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from requests.exceptions import HTTPError
from .mocks.mocked_api_response import MockedResponse

client = TestClient(app)


@patch("requests.get")
def test_seed_endpoint_external_success_response(mocked_get):
    """Testing external API success response from seed endpoint"""
    mocked_get.return_value = MockedResponse(status_code=200)
    response = client.post('/api/movies/seed/')
    assert response.status_code == 201


@patch("requests.get")
def test_seed_endpoint_external_error_response(mocked_get):
    """Testing external API failed response from seed endpoint"""
    expected_response = {
        'detail': 'ups, something went wrong'
    }
    mocked_get.return_value = MockedResponse(status_code=403, reason='ups, something went wrong')
    response = client.post('/api/movies/seed/')
    assert response.status_code == 403
    assert json.loads(response.content) == expected_response


@patch("requests.get")
def test_seed_endpoint_external_call(mocked_get):
    """Testing external API success response from seed endpoint"""
    mocked_get.return_value = MockedResponse(status_code=200)
    client.post('/api/movies/seed/')
    mocked_get.assert_called_once_with(environ.get('EXTERNAL_API_URL'))
