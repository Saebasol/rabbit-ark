from os.path import exists
from typing import Any, Literal, Optional

from aiofiles import open
from aiofiles.os import mkdir
from aiohttp.client import ClientSession

from rabbitark.config import Config
from rabbitark.dataclass import DownloadInfo
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

    async def create_folder(self, title: Optional[str] = None) -> str:
        default_dir = f"{self.config.BASE_DIRECTORY}/{self.config.FOLDER}/"
        if not exists(default_dir):
            await mkdir(default_dir)

        if title:
            if not exists(f"{default_dir}/{title}"):
                await mkdir(f"{default_dir}/{title}")

            return f"{default_dir}/{title}/"

        return default_dir

    async def start_download(self, download_info: DownloadInfo):
        directory = await self.create_folder(download_info.title)
        filename_mapping = download_info.to_download(directory)
        url_list = list(filename_mapping.keys())
        await self.request_using_session_pool(
            self.download,
            url_list,
            "GET",
            request_per_session=self.config.REQUEST_PER_SESSION,
            filename=filename_mapping,
            **download_info.kwargs,
        )
