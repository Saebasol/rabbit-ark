import os
from typing import Any
from rabbitark.downloader.downloader import Downloader
from rabbitark.utils.extractor_dict import extractor
from rabbitark.utils.load_dynamic_module import load_extensions
from rabbitark.error import ExtractorNotFound


class RabbitArk(Downloader):
    def __init__(self, option, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.option = option

    async def start(self, downloadable: Any):
        if self.option in extractor:
            init_class = extractor[self.option]()

        elif os.path.isfile(self.option):
            init_class = load_extensions(self.option)

        else:
            raise ExtractorNotFound(self.option)

        if isinstance(downloadable, list):
            infos = await init_class.multiple_download_info(downloadable)
            await self.start_multiple_download(infos)
        else:
            info = await init_class.download_info(downloadable)
            await self.start_download(info)
