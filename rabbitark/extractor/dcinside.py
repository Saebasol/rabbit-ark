from rabbitark.error import NotFound
from rabbitark.utils.default_class import DownloadInfo
from rabbitark.utils import Request
from rabbitark.rabbitark import RabbitArk
from typing import Any

class DcinsideRequester(Request):
    def __init__(self) -> None:
        super().__init__(
            headers={
                "accept-encoding": "gzip, deflate, br",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                "referer": "https://images.dcinside.com",
            }
        )
    async def image(self, url: str):
            id = url.split("=")[1]
            no = url.split("=")[2]
            return f"https://images.dcinside.com/viewimagePop.php?id={id}&no={no}"
    
    async def images(self, url: str):
        pass

@RabbitArk.register("dcinside")
class Dcinside(DcinsideRequester):
    def __init__(self):
        super().__init__()
        
    async def extractor_download(self, downloadable: Any) -> DownloadInfo:
        if downloadable != None:
            await self.images(downloadable)
        raise NotFound(downloadable)
