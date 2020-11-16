import os
from typing import Any, List

from rabbitark.downloader.downloader import Downloader
from rabbitark.error import ExtractorNotFound
from rabbitark.utils.default_class import Info
from rabbitark.utils.extractor_dict import extractor
from rabbitark.utils.load_dynamic_module import load_extensions


class RabbitArk(Downloader):
    def __init__(self, option: str) -> None:
        super().__init__()
        self.option: str = option

    async def start(self, downloadable: Any = None) -> None:
        if self.option in extractor:
            init_class: Any = extractor[self.option]()
        elif os.path.isfile(self.option):
            init_class = load_extensions(self.option)
        else:
            raise ExtractorNotFound(self.option)

        if isinstance(downloadable, list):
            infos: List[Info] = await init_class.multiple_download_info(downloadable)
            await self.start_multiple_download(infos)
        else:
            info: Info = await init_class.download_info(downloadable)
            await self.start_download(info)
