from os.path import exists
from typing import Any, Literal, Optional

from aiofiles import open
from aiofiles.os import mkdir
from aiohttp.client import ClientSession

from rabbitark.config import Config
from rabbitark.data import DownloadInfo
from rabbitark.request import SessionPoolRequest


class Downloader(SessionPoolRequest):
    def __init__(self, config: Config) -> None:
        self.config = config
        super().__init__()

    async def download(
        self,
        session: ClientSession,
        url: str,
        method: Literal["GET"],
        _: Any,
        **kwargs: Any,
    ):
        filename = kwargs.pop("filename")
        response = await session.request(method, url, **kwargs)
        async with open(filename[url], "wb") as f:
            async for data, _ in response.content.iter_chunks():
                await f.write(data)

    async def create_folder(self, title: Optional[str] = None) -> None:
        if not exists(f"{self.config.BASE_DIRECTORY}/{self.config.FOLDER}"):
            await mkdir(f"{self.config.BASE_DIRECTORY}/{self.config.FOLDER}")

        if title:
            if not exists(f"{self.config.BASE_DIRECTORY}/{self.config.FOLDER}/{title}"):
                await mkdir(
                    f"{self.config.BASE_DIRECTORY}/{self.config.FOLDER}/{title}"
                )

    async def start_download(self, download_info: DownloadInfo):
        filename_mapping = download_info.to_download(self.config.BASE_DIRECTORY)
        url_list = list(filename_mapping.keys())
        await self.request_using_session_pool(
            self.download,
            url_list,
            "GET",
            request_per_session=self.config.REQUEST_PER_SESSION,
            filename=filename_mapping,
            **download_info.kwargs,
        )
