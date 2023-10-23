"""src.services.elasticsearch_movies"""
import logging
from os import environ
from typing import List

from elasticsearch.helpers import bulk
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.query import Match, Wildcard, MatchAll

from src.connectors.elasticsearch import es as es_connector
from src.mappings.movies import mapping as movies_index_mapping

logger = logging.getLogger(__name__)


class ElasticSearchMovieService:
    """Elasticsearch service"""

    es = es_connector
    index_name = environ.get("ELASTICSEARCH_INDEX_NAME")

    @classmethod
    def create_index(cls) -> None:
        """create_index
        This function creates the desired elasticsearch index
        """
        cls.es.indices.create(
            index=cls.index_name,
            body=movies_index_mapping,
        )

    @classmethod
    def insert_movies(cls, movies: list) -> dict:
        if not cls.es.indices.exists(index=cls.index_name):
            logger.info("index not exists")
            cls.create_index()
        cls.es.delete_by_query(index=cls.index_name, body={"query": {"match_all": {}}})
        ok, failed = bulk(cls.es, actions=movies, index=cls.index_name)
        return {"created": ok, "failed": failed}

    @classmethod
    def get_movies(cls, title: str = None, year: int = None) -> List[dict]:
        year_query = None
        title_query = None
        total_documents = cls.es.count(index=cls.index_name).get("count")
        if year:
            year_query = Match(Year=str(year))

        if title:
            title_query = Q(Wildcard(Title=f"*{title}*"))

        if year_query and title_query:
            q = year_query & title_query
        elif year_query:
            q = year_query
        elif title_query:
            q = title_query
        else:
            q = Q(MatchAll())
        s = Search(using=cls.es, index=cls.index_name)
        s = s.query(q).extra(size=total_documents)
        movies = s.execute()

        return [movie.to_dict() for movie in movies]
