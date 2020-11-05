from typing import Any

from rabbitark.config import config
from rabbitark.error import NotFound
from rabbitark.utils.default_class import Image, Info
from rabbitark.utils.request import Requester
from rabbitark.utils.utils import folder_name_checker, get_urls, split


class PixivRequester(Requester):
    def __init__(self):
        super().__init__(
            headers={
                "accept-encoding": "gzip, deflate, br",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                "referer": "https://pixiv.net",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
            },
            cookies=config.COOKIES,
        )

    # async def get_postkey(self):
    #     r = await self.get("https://www.pixiv.net/", "text")
    #     return re.findall(r'.*pixiv.context.token = "([a-z0-9]{32})"?.*', r.body)[0]

    async def get_illust_info(self, illust_id):
        info = await self.get(
            f"https://www.pixiv.net/ajax/illust/{illust_id}",
            "json",
        )
        if info.status == 200:
            return info.body
        else:
            return

    async def get_illust_urls(self, illust_id):
        info = await self.get(
            f"https://www.pixiv.net/ajax/illust/{illust_id}/pages",
            "json",
        )
        return [page["urls"]["original"] for page in info.body["body"]]

    async def get_user_info(self, user_id):
        info = await self.get(
            f"https://www.pixiv.net/ajax/user/{user_id}?full=1", "json"
        )
        if info.status == 200:
            return info.body["body"]["name"]
        else:
            return None

    async def get_user_all_illust(self, user_id):
        info = await self.get(
            f"https://www.pixiv.net/ajax/user/{user_id}/profile/all",
            "json",
        )
        return info.body["body"]["illusts"].keys()

    async def user_images(self, user_id):
        user_all_illust = await self.get_user_all_illust(user_id)
        url_list = await get_urls(self.get_illust_urls, user_all_illust)
        return url_list

    async def checking_id(self, pixiv_id):
        illust = await self.get_illust_info(pixiv_id)
        if illust:
            return await self.single_images(pixiv_id)

        username = await self.get_user_info(pixiv_id)
        if username:
            return await self.user(pixiv_id)

        raise NotFound(pixiv_id)

    async def single_images(self, illust_id):
        info = await self.get_illust_info(illust_id)
        if not info:
            return
        urls = await self.get_illust_urls(illust_id)
        return Info(
            [Image(url) for url in urls],
            folder_name_checker(info["body"]["title"]),
            self.headers,
        )

    async def user(self, user_id):
        username = await self.get_user_info(user_id)
        if not username:
            return
        url_list = await self.user_images(user_id)
        return Info(
            [Image(url) for url in url_list],
            folder_name_checker(username),
            self.headers,
        )


class Pixiv(PixivRequester):
    def __init__(self):
        super().__init__()

    async def download_info(self, downloadable: Any) -> Info:
        if downloadable.isdigit():
            info = await self.checking_id(downloadable)
        else:
            if "artwork" in downloadable:
                info = await self.single_images(split(downloadable))
            elif "user" in downloadable:
                info = await self.user(split(downloadable))
            else:
                raise NotFound(downloadable)

        if not info:
            raise NotFound(downloadable)

        return info
