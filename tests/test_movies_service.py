import os
from unittest.mock import patch

import pytest

from src.exceptions.get_movie_exception import GetMovieException
from src.exceptions.seed_movie_exception import SeedMovieException
from src.services.movies import MoviesService
from .mocks.async_functions_mocs import async_generator_mock
from .mocks.external_api_connector import example_movie_list
from .mocks.movies_es_service_mocks import transformed_movie_list


def test_process_movie():
    """test the process movie function response"""
    expected_object = {
        "_id": "tt0076759",
        "_index": os.environ.get("ELASTICSEARCH_INDEX_NAME"),
        "_op_type": "create",
        "_source": {
            "Title": "Star Wars: Episode IV - A New Hope",
            "Year": 1977,
            "imdbID": "tt0076759",
        },
    }
    assert expected_object == MoviesService.process_movie(example_movie_list[0])


@pytest.mark.asyncio
@patch("src.services.movies.ExternalAPIConnector")
@patch("src.services.movies.ElasticSearchMovieService")
async def test_seed_movies(mocked_es, mocked_connector):
    """test the seed_movie function internal calls to other services"""
    mocked_es.index_name = os.environ.get("ELASTICSEARCH_INDEX_NAME")
    external_api_response = example_movie_list
    es_response = {"created": 10, "failed": []}
    mocked_connector.get_movies_from_external_api.return_value = async_generator_mock(
        external_api_response
    )
    mocked_es.insert_movies.return_value = es_response
    response = await MoviesService.seed_movies(page=1, title="test")
    assert response == es_response
    mocked_connector.get_movies_from_external_api.assert_called_once_with(
        page=1, substring="test"
    )

    mocked_es.insert_movies.assert_called_once_with(transformed_movie_list)


@pytest.mark.asyncio
@patch("src.services.movies.ExternalAPIConnector")
async def test_seed_movies_exception_calling_external_api(mocked_connector):
    """test the seed_movie function internal calls to other services raising exceptions"""
    mocked_connector.get_movies_from_external_api.side_effect = Exception()
    with pytest.raises(SeedMovieException) as exception:
        await MoviesService.seed_movies(page=1, title="test")


@pytest.mark.asyncio
@patch("src.services.movies.ExternalAPIConnector")
@patch("src.services.movies.ElasticSearchMovieService")
async def test_seed_movies_exception_inserting_movies(mocked_es, mocked_connector):
    """test the seed_movie function internal calls to other services"""
    external_api_response = example_movie_list
    mocked_connector.get_movies_from_external_api.return_value = async_generator_mock(
        external_api_response
    )
    mocked_es.insert_movies.side_effect = Exception()
    with pytest.raises(SeedMovieException) as exception:
        await MoviesService.seed_movies(page=1, title="test")


@pytest.mark.asyncio
@patch("src.services.movies.ElasticSearchMovieService")
async def test_get_movies_exception_getting_movies(mocked_es):
    """test the seed_movie function internal calls to other services"""
    mocked_es.get_movies.side_effect = Exception()
    with pytest.raises(GetMovieException) as exception:
        await MoviesService.get_movies(year=1, title="test")
