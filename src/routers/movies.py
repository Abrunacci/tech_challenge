"""src.routers.movies
All the movies related routers
"""
from typing import List, Union

from fastapi import APIRouter, Response, status

from src.exceptions.get_movie_exception import GetMovieException
from src.exceptions.seed_movie_exception import SeedMovieException
from src.services.movies import MoviesService

router = APIRouter()


@router.put("/movies/seed", tags=["Movies"], status_code=201)
async def seed_movies(response: Response, title: str = None, page: int = None) -> dict:
    """
    **[PUT] /movies/seed**:

    This endpoint will call the external movies provider and fill the elasticsearch index with the required data.

    Everytime this endpoint is called, the index will be replaced by the new seed request.

    **Filters**:

    - **title: str**

    Full or partial movie name.

    - **page: int**

    The external API page.

    **Query combination**:

    - The use of only one query param will seed the index with all the movies matching that parameter.
    - Using both parameters will seed the index with only the movies that fit both search criteria.
    - The lack of parameters will seed all the movies to the index.


    ***returns: dict**
        ex: {"created": 866, "failed": [<List of movies that wasn't inserted in the index>]}

    ***raises****
        in case of an internal error this endpoint will return a dict with the error string representation
    """
    try:
        seed_result = await MoviesService.seed_movies(page=page, title=title)
        return seed_result
    except SeedMovieException as e:
        response.status_code = status.HTTP_409_CONFLICT
        return {"reason": e.message}


@router.get("/movies", tags=["Movies"], status_code=200)
async def get_movies(
    response: Response, title: str = None, year: int = None
) -> Union[List[dict], dict]:
    """
    **[GET] /movies**:

    This endpoint returns all the movies required by the client.

    **Filters**:

    - **title: str**

    Full or partial movie name.

    - **year: int**

    The year of the movie release.

    **Query combination**:

    - The use one of the query params will return all the movies matching that parameter.
    - Using both parameters will return only the movies that fit both search criteria.
    - The lack of parameters will return all the movies in the elasticsearch index.

    **Pagination**:

    *Not implemented*

    ***raises****
      In case of an internal error this endpoint will return a dict with the error string representation
    """
    try:
        result = await MoviesService.get_movies(title=title, year=year)
        return result
    except GetMovieException as e:
        response.status_code = status.HTTP_409_CONFLICT
        return {"reason": e.message}
