class GetMovieException(Exception):
    """raised in case of an error while trying to query the ES index"""

    def __init__(self, message=None):
        """
        Class initialization
        :param message:
            The message that will be added to the exception.
        """
        self.message = message
        super().__init__(self.message)
