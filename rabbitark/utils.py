from re import sub
from rabbitark.abc import RabbitArkABC
from os.path import basename
from urllib.parse import urlparse
from http.cookiejar import MozillaCookieJar
from http.cookies import SimpleCookie

import importlib.util
import logging
from typing import Any, Optional, cast
from rabbitark.typing import CA
from functools import wraps

logger = logging.getLogger("rabbitark.utils.load_dynamic_module")


def import_dynamic_module(path: str):
    logger.debug("extractor path: %s", path)
    spec = importlib.util.spec_from_file_location("dynamic_module", path)
    importlib.util.module_from_spec(spec)
    logger.info("sucees import")


def split(url: str) -> str:
    a = urlparse(url)
    return basename(a.path)


def load_rawcookie(rawdata: str) -> dict[str, str]:
    cookie: SimpleCookie[str] = SimpleCookie(rawdata)
    return {key: morsel.value for key, morsel in cookie.items()}


def load_cookie_txt(filename: str) -> dict[str, Optional[str]]:
    cj = MozillaCookieJar(filename)
    return {each.name: each.value for each in cj}


def folder_name_checker(foldername: str) -> str:
    return sub(r"[\\/:*?\"<>\|]", "", foldername)


def close(f: CA) -> CA:
    @wraps(f)
    async def wrapper(self: RabbitArkABC, *args: Any, **kwargs: Any):
        try:
            result = await f(self, *args, **kwargs)
        finally:
            if self.session:
                await self.session.close()
        return result

    return cast(CA, wrapper)
