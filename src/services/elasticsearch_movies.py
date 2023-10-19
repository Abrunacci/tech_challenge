"""src.services.elasticsearch_movies"""

from logging import getLogger
from typing import List, Iterator

from src.main import es as es_connection
from src.mappings.movies import mapping as movies_index_mapping

logger = getLogger(__name__)


class ElasticSearchMovieService:
    """Elasticsearch service"""

    es = es_connection
    index_name = "movies"

    @classmethod
    def create_index(cls) -> None:
        """create_index
        This function creates the desired elasticsearch index
        """
        response = cls.es.indices.create(
            index=cls.index_name, mapping=movies_index_mapping
        )
        logger.debug(response)

    @classmethod
    def process_movies(cls, movies: List[dict]) -> Iterator[dict]:
        """process_movies
        This function process the movies list in order to transform the dicts
        into movie index mapping.

        :arguments:
            movies: List of dicts with movies objects.
            ex:
            [
              {
                "Title": "Star Wars: Episode IV - A New Hope",
                "Year": 1977,
                "imdbID": "tt0076759"
              },
              {
                "Title": "Star Wars: Episode V - The Empire Strikes Back",
                "Year": 1980,
                "imdbID": "tt0080684"
              },
              {
                "Title": "Star Wars: Episode VI - Return of the Jedi",
                "Year": 1983,
                "imdbID": "tt0086190"
              },
            ]
        :returns:
            Iterator: Movies index mapping iterator
        """

        for movie in movies:
            yield {
                "_op_type": "create",
                "_index": cls.index_name,
                "_type": "document",
                "_id": movie.get("imdbID"),
                "doc": movie,
            }

    @classmethod
    def insert_movies(cls, movies: List[dict]) -> None:
        """insert_movies

        This function inserts the movies list into elasticsearch movie index.

        If the index doesn't exist, it calls the create_index function before
        trying to insert the data.

        :arguments:
            movies - A list of dicts with movies objects.
            ex:
            [
              {
                "Title": "Star Wars: Episode IV - A New Hope",
                "Year": 1977,
                "imdbID": "tt0076759"
              },
              {
                "Title": "Star Wars: Episode V - The Empire Strikes Back",
                "Year": 1980,
                "imdbID": "tt0080684"
              },
              {
                "Title": "Star Wars: Episode VI - Return of the Jedi",
                "Year": 1983,
                "imdbID": "tt0086190"
              },
            ]

        :returns:
            None
        """
        if not cls.es.indices.exists(cls.index_name):
            cls.create_index()

        cls.es.bulk(cls.process_movies(movies))
