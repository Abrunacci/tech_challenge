import asyncio
from typing import Any
from unittest.mock import MagicMock


def async_function_mock(expected_response: Any):
    """
    This function will be used to mock all the async function in the API services

    :param expected_response:
        Any object you need that matches the mocked function response
    :return:
        asyncio future
    """
    f = asyncio.Future()
    f.set_result(expected_response)
    return f


async def async_generator_mock(expected_response: list):
    """
    This function will be used to mock all the async function that returns async generator in the API services

    :param expected_response:
        The list that will be processed
    :return:
        async iterator
    """
    a = MagicMock()
    a.__aiter__.return_value = expected_response
    return a
