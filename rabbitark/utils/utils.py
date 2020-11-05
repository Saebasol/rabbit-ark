from http.cookies import SimpleCookie

from aiomultiprocess import Pool


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


def load_cookie(rawdata):
    cookie = SimpleCookie()
    cookie.load(rawdata)
    return {key: morsel.value for key, morsel in cookie.items()}
