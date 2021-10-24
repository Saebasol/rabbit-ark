from aiohttp.client import ClientSession
from aiofile import async_open

from rabbitark.types import DownloadInfo  # type: ignore


class Downloader:
    def __init__(self, session: ClientSession):
        self.session = session

    def update_headers(self, headers: dict[str, str]):
        self.session.headers.update(headers)

    async def download(self, url: str, path: str):
        async with self.session.get(url) as response:
            async with async_open(path, "wb") as f:
                async for data, _ in response.content.iter_chunks():
                    await f.write(data)

    async def start(self, download_info: DownloadInfo):
        if download_info.headers:
            self.update_headers(download_info.headers)

        if isinstance(download_info.info, list):
            for info in download_info.info:
                await self.start(DownloadInfo(info, download_info.path))
