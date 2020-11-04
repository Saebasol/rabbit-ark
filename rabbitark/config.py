class _Config:
    __slots__ = ["BASE_DIRECTORY"]

    def __init__(self):
        self.BASE_DIRECTORY: str = "."


config = _Config()