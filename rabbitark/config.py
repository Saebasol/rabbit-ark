from typing import Any, List, Dict, Optional


class _Config:
    __slots__: List[str] = ["BASE_DIRECTORY", "FOLDER", "COOKIES"]

    def __init__(self) -> None:
        self.BASE_DIRECTORY: str = "."
        self.FOLDER: Optional[str] = None
        self.COOKIES: Dict[str, Any] = {}


config: _Config = _Config()
