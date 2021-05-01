from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Optional

from aiohttp.client import ClientSession

from rabbitark.config import Config
from rabbitark.dataclass import DownloadInfo


class BaseRequest(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self.session: Optional[ClientSession] = None


class BaseExtractor(BaseRequest, metaclass=ABCMeta):
    @abstractmethod
    async def get_download_info(
        self, download_source: Any, config: Config
    ) -> DownloadInfo:
        pass
