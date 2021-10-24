from abc import ABCMeta, abstractmethod
from typing import Any

from rabbitark.request import Request


class BaseExtractor(metaclass=ABCMeta):
    headers: dict[str, Any]
    connect_limit: int
    session_options: dict[str, Any]
    

    @abstractmethod
    def __init__(self, request: Request) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_download_info(self, download_source: Any) -> Any:
        raise NotImplementedError
