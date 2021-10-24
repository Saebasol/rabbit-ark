import logging

from importlib.util import module_from_spec, spec_from_file_location
from os.path import basename
from re import sub
from urllib.parse import urlparse

logger = logging.getLogger("rabbitark.utils")


def import_dynamic_module(path: str):
    logger.debug("extractor path: %s", path)
    spec = spec_from_file_location("dynamic_module", path)
    if spec:
        module_from_spec(spec)
        logger.info("Success import")
    raise RuntimeError("Failed import")


def split(url: str) -> str:
    parse_result = urlparse(url)
    return basename(parse_result.path)


def replace_folder_name(foldername: str) -> str:
    return sub(r"[\\/:*?\"<>\|]", "", foldername)
