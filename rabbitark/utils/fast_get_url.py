from aiomultiprocess import Pool


async def get_urls(func, arg: list) -> None:
    result = []
    async with Pool() as pool:
        async for url in pool.map(func, arg):
            if isinstance(url, list):
                result.extend(url)
            else:
                result.append(url)

    return result
