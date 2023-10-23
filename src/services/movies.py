"""src.service.movies
Movie Services.
This service is responsible for the movies insertion into ElasticSearch.
"""
import logging
from os import environ
from typing import List

from src.connectors.external_api_connector import ExternalAPIConnector
from src.exceptions.get_movie_exception import GetMovieException
from src.exceptions.seed_movie_exception import SeedMovieException
from src.services.elasticsearch_movies import ElasticSearchMovieService

logger = logging.getLogger(__name__)


class MoviesService:
    """MovieService"""

    @classmethod
    def process_movie(cls, movie: dict) -> dict:
        """
        process_movie:

        This method transforms the dict representation of the movie object into the dict representation of an ElasticSearch document.

        :param movie:
            Movie dict representation, will be added to the elasticsearch _source document for creation.

            ex: {
                "Title": "Star Wars VI -  A new hope",
                "Year": 1977
                "imdbID": "imdbIDCode"
            }

        :return:
            Elasticsearch document dict representation

            ex: {
            "_op_type": "create",
            "_index": "movies",
            "_id": "imdbIDCode",
            "_source": {
                "Title": "Star Wars VI -  A new hope",
                "Year": 1977
                "imdbID": "imdbIDCode"
                }
            }
        """
        return {
            "_op_type": "create",
            "_index": environ.get("ELASTICSEARCH_INDEX_NAME"),
            "_id": movie.get("imdbID"),
            "_source": movie,
        }

    @classmethod
    async def seed_movies(cls, page: int = None, title: str = None) -> dict:
        """
        seed_movies
        This method receive the filters to get the movies from the external API service
        and once it gets the response, it calls ElasticSearchMovieService to impact the data into
        the index

        :param page:
            An integer that represent the page number to look at the external API movie service.
        :param title:
            A string that represents the full or partial movie name that will be searched at the external API movie service.

        :return:
            A dictionary with the total amount of data created and a list with the failed objects
            ex:
                {"created": 8, "failed":[{"Title": "Star Wars I - The phantom menace", ...}, ...]}
        :raises:
            SeedMovieException
        """
        try:
            movies = await ExternalAPIConnector.get_movies_from_external_api(
                substring=title, page=page
            )

            return ElasticSearchMovieService.insert_movies(
                [cls.process_movie(movie) async for movie in movies]
            )
        except Exception as e:
            logger.exception(f"Exception happened while trying to seed the index:  {e}")
            raise SeedMovieException(message=e.__str__())

    @classmethod
    async def get_movies(cls, title: str = None, year: int = None) -> List[dict]:
        """
        get_movies
        This method will call ElasticSearchMovieService.get_movies function to get
        the requested movies filtered by the received parameters.

        :param title:
            The string representation of the full or partial movie title.
        :param year:
            Integer that represents the year field of the movie.
        :return:
            A list of dictionaries
            ex:
            [
                {"Title":"Waterworld","Year":1995,"imdbID":"tt0114898"},
                {"Title":"Waterworld","Year":1995,"imdbID":"tt0189200"},
                ...,
            ]
        :raises:
            GetMovieException
        """
        try:
            return ElasticSearchMovieService.get_movies(year=year, title=title)
        except Exception as e:
            raise GetMovieException(message=e.__str__())
