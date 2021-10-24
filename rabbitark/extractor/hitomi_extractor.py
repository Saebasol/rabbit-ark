from rabbitark.base import Extractor
from rabbitark.client import RabbitArk
from rabbitark.request import Request


@RabbitArk.register("hitomi")
class HitomiExtractor(Extractor):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }

    def __init__(self, request: Request):
        self.request = request

    async def get_download_info(self, download_source: str):
        return await self.request.get("https://example.com", "text")
