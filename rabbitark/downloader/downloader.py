import os
from typing import Generator, List, Optional, Union
from functools import wraps

import aiofiles
import aiofiles.os as aioos  # type: ignore
from aiomultiprocess import Pool  # type: ignore

from rabbitark.config import config
from rabbitark.utils import Requester
from rabbitark.utils.default_class import RequestInfo, DownloadInfo, Response


class Downloader(Requester):
    def __init__(self) -> None:
        super().__init__()
        self.base_directory: str = config.BASE_DIRECTORY
        self.folder: Optional[str] = config.FOLDER

    async def create_folder(self, title=None) -> None:
        if not os.path.exists(f"{self.base_directory}/{self.folder}"):
            await aioos.mkdir(f"{self.base_directory}/{self.folder}")

        if title:
            if not os.path.exists(f"{self.base_directory}/{self.folder}/{title}"):
                await aioos.mkdir(f"{self.base_directory}/{self.folder}/{title}")

    def check_folder(self, title: Optional[str], filename: Optional[str]) -> str:
        if title:
            return f"{self.base_directory}/{self.folder}/{title}/{filename}"
        else:
            return f"{self.base_directory}/{self.folder}/{filename}"

    def download_info_generator(self, info: DownloadInfo) -> Generator:
        for image in info.image:
            yield RequestInfo(
                image.url,
                self.check_folder(info.title, image.filename),
                info.headers if info.headers else {},
            )

    def checking_image_object(
        self, info: DownloadInfo
    ) -> Union[Generator, List[RequestInfo]]:
        if isinstance(info.image, list):
            return self.download_info_generator(info)
        else:
            return [
                RequestInfo(
                    info.image.url,
                    self.check_folder(info.title, info.image.filename),
                    info.headers if info.headers else {},
                )
            ]

    async def download(self, download_info: RequestInfo) -> None:
        image_byte: Response = await self.get(
            download_info.url, headers=download_info.headers
        )
        async with aiofiles.open(download_info.directory, mode="wb") as f:  # type: ignore
            await f.write(image_byte.body)

    async def start_download(self, info: DownloadInfo) -> None:
        download_info: Union[Generator, List[RequestInfo]] = self.checking_image_object(
            info
        )
        await self.create_folder(info.title)
        async with Pool() as pool:
            async for _ in pool.map(self.download, download_info):
                pass

    async def start_multiple_download(self, info_list: List[DownloadInfo]) -> None:
        async with Pool() as pool:
            async for _ in pool.map(self.start_download, info_list):
                pass
