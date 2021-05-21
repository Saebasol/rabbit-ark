from typing import Optional


class Config:
    __slots__: list[str] = [
        "BASE_DIRECTORY",
        "FOLDER",
        "COOKIES",
        "YOUTUBE_PAGE_LIMIT",
        "CUSTOM_EXTRACTOR",
        "REQUEST_PER_SESSION",
    ]

    def __init__(self) -> None:
        self.BASE_DIRECTORY: str = "."
        self.FOLDER: Optional[str] = None
        self.COOKIES: dict[str, Optional[str]] = {}
        self.CUSTOM_EXTRACTOR: Optional[str] = None

        # extractor config
        self.YOUTUBE_PAGE_LIMIT: int = 6

        # download config
        self.REQUEST_PER_SESSION: int = 10
