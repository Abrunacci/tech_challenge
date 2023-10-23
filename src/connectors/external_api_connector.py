import asyncio
import logging
from os import environ
from typing import AsyncGenerator

import httpx

logger = logging.getLogger(__name__)


class ExternalAPIConnector:
    """External API connector"""

    @staticmethod
    def _generate_url(page: int = None, substring: str = None) -> str:
        external_api_url = environ.get("EXTERNAL_API_URL")
        if substring and page:
            external_api_url = f"{external_api_url}?Title={substring}&page={page}"
        elif substring:
            external_api_url = f"{external_api_url}?Title={substring}"
        elif page:
            external_api_url = f"{external_api_url}?page={page}"
        return external_api_url

    @staticmethod
    async def _perform_request(client, url) -> dict:
        """Function that calls external API"""
        response = await client.get(url)
        return response.json()

    @classmethod
    async def get_all(
        cls, substring: str = None, page: int = None
    ) -> AsyncGenerator[dict, None]:
        all_requests = []
        async with httpx.AsyncClient() as client:
            first_request = await cls._perform_request(
                client, cls._generate_url(page=page, substring=substring)
            )
            logger.info(first_request)
            for i in range(
                first_request.get("page"), first_request.get("total_pages") + 1
            ):
                all_requests.append(
                    cls._perform_request(
                        client, cls._generate_url(page=i, substring=substring)
                    )
                )

            responses = await asyncio.gather(*all_requests)
            for response in responses:
                for movie in response.get("data"):
                    yield movie

    @classmethod
    async def get_movies_from_external_api(
        cls, page: int = None, substring: str = None
    ) -> AsyncGenerator[dict, None]:
        return cls.get_all(substring=substring, page=page)
