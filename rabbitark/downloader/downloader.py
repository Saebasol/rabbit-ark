import os

import aiofiles
import aiofiles.os as aioos
from aiomultiprocess import Pool

from rabbitark.config import config
from rabbitark.utils import Requester
from rabbitark.utils.default_class import DownloadInfo, Info


class Downloader(Requester):
    def __init__(self):
        super().__init__()
        self.base_directory = config.BASE_DIRECTORY

    async def create_folder(self, title) -> None:
        if not os.path.exists(f"{self.base_directory}/{title}"):
            await aioos.mkdir(f"{self.base_directory}/{title}")

    def directory_generator(self, info: Info) -> DownloadInfo:
        for image in info.image:
            yield DownloadInfo(
                image.url,
                f"{self.base_directory}/{info.title}/{image.filename}",
                info.headers if info.headers else {},
            )

    async def download(self, download_info: DownloadInfo) -> None:
        image_byte = await self.get(download_info.url, headers=download_info.headers)
        async with aiofiles.open(download_info.directory, mode="wb") as f:
            await f.write(image_byte)

    async def start_download(self, info: Info) -> None:
        download_info = self.directory_generator(info)
        await self.create_folder(info.title)
        async with Pool() as pool:
            async for _ in pool.map(self.download, download_info):
                pass

    async def start_multiple_download(self, info_list: list[Info]) -> None:
        async with Pool() as pool:
            async for _ in pool.map(self.start_download, info_list):
                pass
