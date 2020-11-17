import os
from typing import Any, List

from rabbitark.config import config
from rabbitark.downloader.downloader import Downloader
from rabbitark.error import ExtractorNotFound
from rabbitark.utils.default_class import DownloadInfo, RabbitArkABC
from rabbitark.utils.load_dynamic_module import import_dynamic_module


class RabbitArk(
    Downloader,
):
    extractor_dict: dict = {}

    def __init__(self, option: str) -> None:
        super().__init__()
        self.option: str = option

    @classmethod
    def register(cls, extractor_name: str):
        def wrapper(wrapped_class):
            cls.extractor_dict[extractor_name] = wrapped_class
            return wrapped_class

        return wrapper

    async def start(self, downloadable: Any = None) -> None:
        if config.CUSTOM_EXTRACTOR:
            if os.path.isfile(config.CUSTOM_EXTRACTOR):
                import_dynamic_module(config.CUSTOM_EXTRACTOR)
        elif self.option not in self.extractor_dict:
            raise ExtractorNotFound(self.option)

        init_class: RabbitArkABC = self.extractor_dict[self.option]()
        if isinstance(downloadable, list):
            infos: List[DownloadInfo] = await init_class.extractor_multiple_download(
                downloadable
            )
            await self.start_multiple_download(infos)
        else:
            info: DownloadInfo = await init_class.extractor_download(downloadable)
            await self.start_download(info)
