import logging
from http.cookiejar import MozillaCookieJar
from http.cookies import SimpleCookie
from importlib.util import module_from_spec, spec_from_file_location
from os.path import basename
from re import sub
from typing import Optional
from urllib.parse import urlparse

logger = logging.getLogger("rabbitark.utils.load_dynamic_module")


def import_dynamic_module(path: str):
    logger.debug("extractor path: %s", path)
    spec = spec_from_file_location("dynamic_module", path)
    module_from_spec(spec)
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
