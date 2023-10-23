from unittest.mock import patch

from fastapi.testclient import TestClient

from src.exceptions.get_movie_exception import GetMovieException
from src.exceptions.seed_movie_exception import SeedMovieException
from src.main import app
from .mocks.async_functions_mocs import async_function_mock
from .mocks.movies_es_service_mocks import example_movie_list

client = TestClient(app)


@patch("src.routers.movies.MoviesService")
def test_seed_endpoint_seed_movies_call_with_page(mocked_movies_service):
    """Testing external API success response from seed endpoint with page param"""
    expected_response = {"created": 10, "failed": []}
    mocked_movies_service.seed_movies.return_value = async_function_mock(
        expected_response=expected_response
    )
    response = client.put("/api/movies/seed", params={"page": 10})
    mocked_movies_service.seed_movies.assert_called_once_with(page=10, title=None)
    assert response.json() == expected_response


@patch("src.routers.movies.MoviesService")
def test_seed_endpoint_seed_movies_call_with_title(mocked_movies_service):
    """Testing external API success response from seed endpoint with title param"""
    expected_response = {"created": 10, "failed": []}
    mocked_movies_service.seed_movies.return_value = async_function_mock(
        expected_response=expected_response
    )
    response = client.put(
        "/api/movies/seed", params={"title": "Star Wars IV - A New Hope"}
    )
    mocked_movies_service.seed_movies.assert_called_once_with(
        page=None, title="Star Wars IV - A New Hope"
    )
    assert expected_response == response.json()


@patch("src.routers.movies.MoviesService")
def test_seed_endpoint_seed_movies_call_without_arguments(mocked_movies_service):
    """Testing external API success response from seed endpoint without params"""
    expected_response = {"created": 10, "failed": []}
    mocked_movies_service.seed_movies.return_value = async_function_mock(
        expected_response=expected_response
    )
    response = client.put("/api/movies/seed")
    mocked_movies_service.seed_movies.assert_called_once_with(page=None, title=None)
    assert response.json() == expected_response


@patch("src.routers.movies.MoviesService")
def test_seed_endpoint_seed_movies_call_with_both_params(mocked_movies_service):
    """Testing external API success response from seed endpoint with both params"""
    expected_response = {"created": 10, "failed": []}
    mocked_movies_service.seed_movies.return_value = async_function_mock(
        expected_response=expected_response
    )
    response = client.put("/api/movies/seed", params={"title": "Star", "page": 3})
    mocked_movies_service.seed_movies.assert_called_once_with(page=3, title="Star")
    assert expected_response == response.json()


@patch("src.routers.movies.MoviesService")
def test_seed_endpoint_internal_error(mocked_movies_service):
    """Testing external API failed response due to SeedMovieException"""
    expected_response = {"reason": "Something went wrong, ups"}
    mocked_movies_service.seed_movies.side_effect = SeedMovieException(
        "Something went wrong, ups"
    )
    response = client.put("/api/movies/seed", params={"title": "Star", "page": 3})
    mocked_movies_service.seed_movies.assert_called_once_with(page=3, title="Star")
    assert expected_response == response.json()


@patch("src.routers.movies.MoviesService")
def test_get_movie_endpoint_internal_error(mocked_movies_service):
    """Testing get endpoint failed response due to GetMovieException"""
    expected_response = {"reason": "Something went wrong, ups"}
    mocked_movies_service.get_movies.side_effect = GetMovieException(
        "Something went wrong, ups"
    )
    response = client.get("/api/movies", params={"title": "Star", "year": 2023})
    mocked_movies_service.get_movies.assert_called_once_with(year=2023, title="Star")
    assert expected_response == response.json()


@patch("src.routers.movies.MoviesService")
def test_get_movie_endpoint_call_without_parameters(mocked_movies_service):
    """Testing get API endpoint success response without parameters"""
    expected_response = example_movie_list
    mocked_movies_service.get_movies.return_value = async_function_mock(
        expected_response
    )
    response = client.get("/api/movies")
    mocked_movies_service.get_movies.assert_called_once_with(year=None, title=None)
    assert expected_response == response.json()


@patch("src.routers.movies.MoviesService")
def test_get_movie_endpoint_call_with_both_parameters(mocked_movies_service):
    """Testing get API endpoint success response with both parameters"""
    expected_response = example_movie_list
    mocked_movies_service.get_movies.return_value = async_function_mock(
        expected_response
    )
    response = client.get("/api/movies", params={"title": "Star", "year": 2023})
    mocked_movies_service.get_movies.assert_called_once_with(year=2023, title="Star")
    assert expected_response == response.json()


@patch("src.routers.movies.MoviesService")
def test_get_movie_endpoint_call_with_title(mocked_movies_service):
    """Testing get API endpoint success response with just title parameter"""
    expected_response = example_movie_list
    mocked_movies_service.get_movies.return_value = async_function_mock(
        expected_response
    )
    response = client.get("/api/movies", params={"title": "Star"})
    mocked_movies_service.get_movies.assert_called_once_with(year=None, title="Star")
    assert expected_response == response.json()


@patch("src.routers.movies.MoviesService")
def test_get_movie_endpoint_call_with_year(mocked_movies_service):
    """Testing get API endpoint success response with just year parameter"""
    expected_response = example_movie_list
    mocked_movies_service.get_movies.return_value = async_function_mock(
        expected_response
    )
    response = client.get("/api/movies", params={"year": 2011})
    mocked_movies_service.get_movies.assert_called_once_with(year=2011, title=None)
    assert expected_response == response.json()
