from abc import abstractmethod
from typing import Any, List, Optional, Union
import abc

from rabbitark.utils.utils import split


class Image:
    def __init__(self, url: str, filename: str = None) -> None:
        self.url: str = url
        self.filename: str = filename if filename else split(url)


class DownloadInfo:
    def __init__(
        self, image: List[Image], title: Optional[Any] = None, headers: Any = None
    ) -> None:
        self.title: Optional[Any] = title
        self.image: Any = image
        self.headers: Any = headers


class RequestInfo:
    def __init__(self, url: str, directory: str, headers: Any = None) -> None:
        self.url: str = url
        self.directory: str = directory
        self.headers: Any = headers


class Response:
    def __init__(self, status: int, message: Optional[Any], body: Any) -> None:
        self.status: int = status
        self.message: Optional[Any] = message
        self.body: Any = body


class RabbitArkABC(metaclass=abc.ABCMeta):
    @abstractmethod
    async def extractor_download(self, downloadable) -> DownloadInfo:
        pass

    @abstractmethod
    async def extractor_multiple_download(self, downloadable) -> List[DownloadInfo]:
        pass