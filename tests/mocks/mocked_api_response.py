from requests import Response


class MockedResponse(Response):
    """Mocked response for testing"""

    def __init__(self, *args, **kwargs) -> None:
        """class initialization"""
        self.status_code = kwargs.get("status_code")
        self.reason = kwargs.get("reason", "")
        super(Response).__init__()
