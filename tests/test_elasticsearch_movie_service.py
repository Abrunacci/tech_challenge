from unittest.mock import patch, MagicMock

from elasticsearch_dsl.query import MatchAll, Match, Wildcard, Bool

from src.mappings.movies import mapping
from src.services.elasticsearch_movies import ElasticSearchMovieService
from tests.mocks.movies_es_service_mocks import example_movie_list


def test_create_index():
    """test create_index"""
    ElasticSearchMovieService.es = MagicMock()
    ElasticSearchMovieService.create_index()
    ElasticSearchMovieService.es.indices.create.assert_called_once_with(
        index="test_index", body=mapping
    )


@patch("src.services.elasticsearch_movies.bulk")
def test_insert_movies(mocked_bulk):
    """test insert_movies"""
    expected_result = {"created": 23, "failed": []}
    ElasticSearchMovieService.es.indices.exists = MagicMock(return_value=True)
    ElasticSearchMovieService.es.delete_by_query = MagicMock()
    mocked_bulk.return_value = (23, [])
    result = ElasticSearchMovieService.insert_movies(movies=example_movie_list)
    ElasticSearchMovieService.es.indices.create.assert_called_once_with(
        index="test_index", body=mapping
    )
    ElasticSearchMovieService.es.delete_by_query.assert_called_once_with(
        index="test_index", body={"query": {"match_all": {}}}
    )
    assert result == expected_result


@patch("src.services.elasticsearch_movies.bulk")
def test_insert_movies_create_index(mocked_bulk):
    """test insert_movies index creation call"""
    expected_result = {"created": 23, "failed": []}
    ElasticSearchMovieService.es.indices.exists = MagicMock(return_value=False)
    ElasticSearchMovieService.es.delete_by_query = MagicMock()
    ElasticSearchMovieService.create_index = MagicMock(return_value=False)
    mocked_bulk.return_value = (23, [])

    result = ElasticSearchMovieService.insert_movies(movies=example_movie_list)

    ElasticSearchMovieService.es.indices.create.assert_called_once_with(
        index="test_index", body=mapping
    )
    ElasticSearchMovieService.es.delete_by_query.assert_called_once_with(
        index="test_index", body={"query": {"match_all": {}}}
    )
    ElasticSearchMovieService.create_index.assert_called_once()
    assert result == expected_result


@patch("src.services.elasticsearch_movies.Search")
def test_get_movies_without_args(mocked_search):
    """test get_movies without args"""
    ElasticSearchMovieService.es = MagicMock(return_value="es_connector")
    ElasticSearchMovieService.get_movies()
    mocked_search.assert_called_once_with(
        using=ElasticSearchMovieService.es, index=ElasticSearchMovieService.index_name
    )
    mocked_search().query.assert_called_once_with(MatchAll())


@patch("src.services.elasticsearch_movies.Search")
def test_get_movies_with_year(mocked_search):
    """test get_movies with year"""
    ElasticSearchMovieService.es = MagicMock(return_value="es_connector")
    ElasticSearchMovieService.get_movies(year=2013)
    mocked_search.assert_called_once_with(
        using=ElasticSearchMovieService.es, index=ElasticSearchMovieService.index_name
    )
    mocked_search().query.assert_called_once_with(Match(Year="2013"))


@patch("src.services.elasticsearch_movies.Search")
def test_get_movies_with_title(mocked_search):
    """test get_movies with title"""
    ElasticSearchMovieService.es = MagicMock(return_value="es_connector")
    ElasticSearchMovieService.get_movies(title="test")
    mocked_search.assert_called_once_with(
        using=ElasticSearchMovieService.es, index=ElasticSearchMovieService.index_name
    )
    mocked_search().query.assert_called_once_with(Wildcard(Title="*test*"))


@patch("src.services.elasticsearch_movies.Search")
def test_get_movies_with_title_and_year(mocked_search):
    """test get_movies with title and year"""
    ElasticSearchMovieService.es = MagicMock(return_value="es_connector")
    ElasticSearchMovieService.get_movies(title="test", year=2013)
    mocked_search.assert_called_once_with(
        using=ElasticSearchMovieService.es, index=ElasticSearchMovieService.index_name
    )
    mocked_search().query.assert_called_once_with(
        Bool(must=[Match(Year="2013"), Wildcard(Title="*test*")])
    )
