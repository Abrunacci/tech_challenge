from os import environ
from time import sleep
from unittest import TestCase
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from src.connectors.external_api_connector import ExternalAPIConnector
from src.main import app
from src.services.elasticsearch_movies import ElasticSearchMovieService
from tests.mocks.async_functions_mocs import async_generator_mock
from tests.mocks.movies_es_service_mocks import example_movie_list


class TestAPIIntegration(TestCase):
    """Test API Integration"""

    original_api_connector = None
    index_name = None

    @classmethod
    def setUpClass(cls) -> None:
        """Test case setup"""
        cls.original_api_connector = ExternalAPIConnector.get_movies_from_external_api
        ExternalAPIConnector.get_movies_from_external_api = MagicMock()
        ExternalAPIConnector.get_movies_from_external_api.return_value = (
            async_generator_mock(example_movie_list)
        )
        cls.index_name = environ["ELASTICSEARCH_INDEX_NAME"]
        environ["ELASTICSEARCH_INDEX_NAME"] = "test_index"
        ElasticSearchMovieService.index_name = "test_index"
        cls.test_client = TestClient(app)

    def setUp(self):
        sleep(1)  # cooldown

    def test_es_seed(self):
        """Test seed elasticsearch"""
        response = self.test_client.put("/api/movies/seed/")
        assert response.status_code == 201
        assert response.json() == {"created": len(example_movie_list), "failed": []}

    def test_get_all_movies(self):
        """Test get endpoint without parameters"""
        response = self.test_client.get("/api/movies")
        assert response.status_code == 200
        assert response.json() == example_movie_list

    def test_get_movies_by_year(self):
        """Test get endpoint with year parameter"""
        response = self.test_client.get("/api/movies", params={"year": 1977})
        assert response.status_code == 200
        assert response.json() == [example_movie_list[0]]

    def test_get_movies_by_title(self):
        """Test get endpoint with title parameter"""
        response = self.test_client.get("/api/movies", params={"title": "jedi"})
        assert response.status_code == 200
        assert response.json() == [example_movie_list[2], example_movie_list[3]]

    def test_get_movies_by_title_and_year(self):
        """Test get endpoint with title and year"""
        response = self.test_client.get(
            "/api/movies", params={"title": "jedi", "year": 1983}
        )
        assert response.status_code == 200
        assert response.json() == [example_movie_list[2]]

    @classmethod
    def tearDownClass(cls):
        """Test case teardown"""
        ExternalAPIConnector.get_movies_from_external_api = cls.original_api_connector
        ElasticSearchMovieService.es.indices.delete(index="test_index")
        environ["ELASTICSEARCH_INDEX_NAME"] = cls.index_name
