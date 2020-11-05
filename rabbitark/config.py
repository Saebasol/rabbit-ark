class _Config:
    __slots__ = ["BASE_DIRECTORY", "FOLDER", "COOKIES"]

    def __init__(self):
        self.BASE_DIRECTORY: str = "."
        self.FOLDER: str = None
        self.COOKIES: str = {}


config = _Config()
