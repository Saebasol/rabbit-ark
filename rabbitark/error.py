class RabbitArkException(Exception):
    pass


class HTTPException(RabbitArkException):
    pass


class NotFound(HTTPException):
    def __init__(self, arg):
        super().__init__(f"Can't found '{arg}'")


class ExtractorNotFound(RabbitArkException):
    def __init__(self, option):
        super().__init__(f"Can't found '{option}'")
