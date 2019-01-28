class RequestError(Exception):
    """
    Twitter's requesting error base class
    """

    @property
    def message(self):
        """
        Returns the first argument
        """
        return self.args[0]
