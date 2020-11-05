from aiomultiprocess import Pool
from http.cookies import SimpleCookie
from http.cookiejar import MozillaCookieJar


def split(url: str):
    return url.rsplit("/", 1)[1]


async def get_urls(func, arg: list) -> None:
    result = []
    async with Pool() as pool:
        async for url in pool.map(func, arg):
            if isinstance(url, list):
                result.extend(url)
            else:
                result.append(url)

    return result


def load_rawcookie(rawdata):
    cookie = SimpleCookie()
    cookie.load(rawdata)
    return {key: morsel.value for key, morsel in cookie.items()}


def load_cookie_txt(filename):
    cj = MozillaCookieJar()
    cj.load(filename)
    return {each.name: each.value for each in cj}


def folder_name_changer(foldername):
    return re.sub(r"[\\/:*?\"<>\|]", "", foldername)
