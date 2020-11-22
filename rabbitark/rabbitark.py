import logging
import os
from typing import Any, List

from rabbitark.config import config
from rabbitark.downloader.downloader import Downloader
from rabbitark.error import ExtractorNotFound
from rabbitark.utils.default_class import DownloadInfo, RabbitArkABC
from rabbitark.utils.load_dynamic_module import import_dynamic_module

logger = logging.getLogger("rabbitark.rabbitark")


class RabbitArk(
    Downloader,
):
    extractor_dict: dict = {}

    def __init__(self, option: str) -> None:
        super().__init__()
        self.option: str = option

    @classmethod
    def register(cls, extractor_name: str):
        if extractor_name in cls.extractor_dict:
            logger.warning("%s is already register will overwrite", extractor_name)

        def wrapper(wrapped_class):
            logger.debug(
                "Register extractor: name: %s, class: %s",
                extractor_name,
                wrapped_class.__name__,
            )
            cls.extractor_dict[extractor_name] = wrapped_class
            return wrapped_class

        return wrapper

    async def start(self, downloadable: Any = None) -> None:
        if config.CUSTOM_EXTRACTOR:
            if os.path.isfile(config.CUSTOM_EXTRACTOR):
                logger.info("found custom extractor")
                import_dynamic_module(config.CUSTOM_EXTRACTOR)
        elif self.option not in self.extractor_dict:
            raise ExtractorNotFound(self.option)

        init_class: RabbitArkABC = self.extractor_dict[self.option]()
        logger.debug("init class: %s", init_class.__class__.__name__)

        if isinstance(downloadable, list):
            infos: List[DownloadInfo] = await init_class.extractor_multiple_download(
                downloadable
            )
            await self.start_multiple_download(infos)
        else:
            info: DownloadInfo = await init_class.extractor_download(downloadable)
            logger.info("start download")
            await self.start_download(info)
            logger.info("completed download")
