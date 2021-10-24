from typing import Any, Union
from dataclasses import dataclass
from yarl import URL
from multidict import CIMultiDictProxy


@dataclass
class Response:
    status: int
    data: Any
    url: URL
    headers: CIMultiDictProxy[str]


@dataclass
class Info:
    url: str
    filename: str


class DownloadInfo:
    info: Union[Info, list[Info]]
    path: str
    headers: dict[str, str]

    def __init__(self, info: Union[Info, list[Info]], path: str):
        self.info = info
        self.path = path
        self.headers = {}

    def set_headers(self, headers: dict[str, str]):
        self.headers = headers
