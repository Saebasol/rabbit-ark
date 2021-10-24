from typing import Any, Callable

from logging import getLogger

from aiohttp.client import ClientSession

from rabbitark.abc import BaseExtractor
from rabbitark.request import Request

ExtractorType = type[BaseExtractor]

logger = getLogger(__name__)


class RabbitArk:
    extractor_dict: dict[str, ExtractorType] = {}

    @classmethod
    def register(cls, extractor_name: str) -> Callable[[ExtractorType], ExtractorType]:
        """
        Register a new extractor.
        :param extractor_name: The name of the extractor.
        :param kwargs: The kwargs to pass to the ClientSession
        """

        def wrapper(extractor: ExtractorType) -> ExtractorType:
            if extractor_name in cls.extractor_dict:
                logger.warning("Extractor %s already registered", extractor_name)

            cls.extractor_dict[extractor_name] = extractor
            logger.debug("Extractor %s registered", extractor_name)
            return extractor

        return wrapper
    
    async def make_session(self, **options: Any):
        session = ClientSession()

    async def run(self, extractor_name: str, downlaod_source: Any) -> None:
        extractor = self.extractor_dict[extractor_name]
        if extractor.session_options:
            request = Request(options=**extractor.session_options)
        else:
            request = Request()
        if extractor.headers:
            request.headers.update(extractor.headers)
        inited_extractor = extractor(request)
        download_info = await inited_extractor.get_download_info(downlaod_source)
