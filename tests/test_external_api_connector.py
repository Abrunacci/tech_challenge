from unittest.mock import patch
from os import environ
from unittest.mock import patch

import pytest

from src.connectors.external_api_connector import ExternalAPIConnector
from tests.mocks.async_functions_mocs import async_generator_mock
from tests.mocks.mocked_api_response import AsyncMockedClient

environ["EXTERNAL_API_URL"] = "http://api.com"


def test_generate_urls():
    """Testing url generation"""
    url = ExternalAPIConnector._generate_url()
    assert url == "http://api.com"
    url = ExternalAPIConnector._generate_url(page=2)
    assert url == "http://api.com?page=2"
    url = ExternalAPIConnector._generate_url(substring="test")
    assert url == "http://api.com?Title=test"
    url = ExternalAPIConnector._generate_url(page=2, substring="test")
    assert url == "http://api.com?Title=test&page=2"


@pytest.mark.asyncio
async def test_perform_requests():
    """Testing perform requests"""
    expected_response = {"data": "mocked"}
    with patch(
        "src.connectors.external_api_connector.httpx.AsyncClient", new=AsyncMockedClient
    ) as client:
        client.response = expected_response
        response = await ExternalAPIConnector._perform_request(client, "http://api.com")
        assert response == expected_response


@pytest.mark.asyncio
async def test_get_movies_from_external_api_call():
    """Testing get movies from external api"""
    expected_response = {"data": "mocked"}
    with patch.object(ExternalAPIConnector, "get_all") as get_all:
        get_all.side_effect = [await async_generator_mock([expected_response])]
        result = await ExternalAPIConnector.get_movies_from_external_api()
        assert [movie async for movie in result] == [expected_response]
        get_all.assert_called_once_with(page=None, substring=None)


@pytest.mark.asyncio
async def test_get_all():
    """Testing get all function"""
    expected_response = {"page": 1, "data": [{"movie": "movie"}], "total_pages": 10}
    with patch.object(ExternalAPIConnector, "_perform_request") as perform_request:
        perform_request.return_value = expected_response
        movies = ExternalAPIConnector.get_all()
        assert [movie async for movie in movies] == [
            {"movie": "movie"} for i in range(0, 10)
        ]
