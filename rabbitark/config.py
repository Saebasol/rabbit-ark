class _Config:
    __slots__ = ["BASE_DIRECTORY", "FOLDER"]

    def __init__(self):
        self.BASE_DIRECTORY: str = "."
        self.FOLDER: str = None


config = _Config()