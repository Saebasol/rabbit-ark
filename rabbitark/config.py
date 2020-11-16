from typing import Any, Dict, List, Optional


class _Config:
    __slots__: List[str] = ["BASE_DIRECTORY", "FOLDER", "COOKIES", "YOUTUBE_PAGE_LIMIT"]

    def __init__(self) -> None:
        self.BASE_DIRECTORY: str = "."
        self.FOLDER: Optional[str] = None
        self.COOKIES: Dict[str, Any] = {}

        # Optinal
        self.YOUTUBE_PAGE_LIMIT: int = 6


config: _Config = _Config()
