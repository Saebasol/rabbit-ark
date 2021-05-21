from typing import Any

from rabbitark.abc import BaseExtractor
from rabbitark.config import Config
from rabbitark.downloader import Downloader


class RabbitArk(Downloader):
    extractor_dict: dict[str, type[BaseExtractor]] = {}

    def __init__(self, extractor_name: str, config: Config) -> None:
        self.extractor_name = extractor_name
        super().__init__(config)

    @classmethod
    def register(cls, extractor_name: str):
        def wrapper(wrapped_class: type[BaseExtractor]):

            cls.extractor_dict[extractor_name] = wrapped_class
            return wrapped_class

        return wrapper

    async def start(self, download_source: Any) -> None:
        init_class = self.extractor_dict[self.extractor_name]()
        try:
            download_info = await init_class.get_download_info(
                download_source, self.config
            )
        finally:
            if init_class.session:
                await init_class.session.close()
        await self.start_download(download_info)
