import re
from http.cookiejar import MozillaCookieJar
from http.cookies import SimpleCookie
from typing import Callable, Dict, List, Optional

from aiomultiprocess import Pool  # type: ignore


def split(url: str) -> str:
    return url.rsplit("/", 1)[1]


async def get_urls(func: Callable, arg: list) -> List:
    result: List = []
    async with Pool() as pool:
        async for url in pool.map(func, arg):
            if isinstance(url, list):
                result.extend(url)
            else:
                result.append(url)

    return result


def load_rawcookie(rawdata: str) -> Dict[str, str]:
    cookie: SimpleCookie = SimpleCookie()
    cookie.load(rawdata)
    return {key: morsel.value for key, morsel in cookie.items()}


def load_cookie_txt(filename: str) -> Dict[str, Optional[str]]:
    cj: MozillaCookieJar = MozillaCookieJar()
    cj.load(filename)
    return {each.name: each.value for each in cj}


def folder_name_checker(foldername: str) -> str:
    return re.sub(r"[\\/:*?\"<>\|]", "", foldername)
