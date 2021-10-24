from typing import Any

from aiohttp.connector import TCPConnector
from rabbitark.abc import BaseExtractor
from rabbitark.request import Request


class Extractor(BaseExtractor):
    headers: dict[str, Any] = {}
    connect_limit: int = 10
    session_options: dict[str, Any] = {"connecter": TCPConnector(limit=connect_limit)}

    def __init__(self, request: Request) -> None:
        super().__init__(request)
