class RabbitArkException(Exception):
    pass


class ExtractorNotFound(RabbitArkException):
    def __init__(self, option):
        super().__init__(f"Can't found '{option}'")