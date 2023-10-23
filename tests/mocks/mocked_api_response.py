import json
from unittest.mock import AsyncMock

from requests import Response


class AsyncMockedClient(AsyncMock):
    response = ""

    def __init__(self, *args, **kwargs):
        super(AsyncMock).__init__()

    @classmethod
    async def get(cls, url):
        return MockedResponse(response=cls.response)

    async def __aenter__(self):
        return None

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


class MockedResponse(Response):
    """Mocked response for testing"""

    def __init__(self, *args, **kwargs) -> None:
        """class initialization"""
        self.status_code = kwargs.get("status_code")
        self.reason = kwargs.get("reason", "")
        self.encoding = "UTF-8"
        self._content = str.encode(json.dumps(kwargs.get("response")))
        super(Response).__init__()
