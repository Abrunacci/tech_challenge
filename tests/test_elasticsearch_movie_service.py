from unittest.mock import MagicMock

from src.mappings.movies import mapping
from src.services.elasticsearch_movies import ElasticSearchMovieService
from .mocks.movies_es_service_mocks import example_movie_list, transformed_movie_list


def test_elasticsearch_movie_service_create_index():
    """Test index creation call"""
    ElasticSearchMovieService.es = MagicMock()
    ElasticSearchMovieService.es.indices.create.return_value = None
    ElasticSearchMovieService.create_index()
    ElasticSearchMovieService.es.indices.create.assert_called_once_with(
        index=ElasticSearchMovieService.index_name, mapping=mapping
    )


def test_elasticsearch_movie_service_process_movies():
    """Test generator response"""
    assert transformed_movie_list == list(
        ElasticSearchMovieService.process_movies(example_movie_list)
    )


def test_elasticsearch_movie_service_insert_movies():
    """Test elasticsearch bulk insert call"""
    ElasticSearchMovieService.es = MagicMock()
    ElasticSearchMovieService.es.indices.exists.return_value = True
    ElasticSearchMovieService.process_movies = MagicMock(
        return_value=transformed_movie_list
    )
    ElasticSearchMovieService.insert_movies(movies=example_movie_list)
    ElasticSearchMovieService.es.bulk.assert_called_once_with(transformed_movie_list)


def test_elasticsearch_movie_service_insert_movies_calling_index_creation():
    """Test elasticsearch bulk insert call"""
    ElasticSearchMovieService.es = MagicMock()
    ElasticSearchMovieService.es.indices.exists.return_value = False

    ElasticSearchMovieService.insert_movies(movies=example_movie_list)

    ElasticSearchMovieService.es.indices.create.assert_called_once_with(
        index=ElasticSearchMovieService.index_name, mapping=mapping
    )
    ElasticSearchMovieService.process_movies = MagicMock(
        return_value=transformed_movie_list
    )
    ElasticSearchMovieService.es.bulk.assert_called_once_with(transformed_movie_list)
