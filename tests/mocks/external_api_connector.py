from typing import Generator

from .movies_es_service_mocks import example_movie_list


async def fake_get_movies_from_api() -> Generator[int, None, None]:
    for movie in example_movie_list:
        yield movie
