import importlib.util
import logging
from importlib.machinery import ModuleSpec
from typing import Any

logger = logging.getLogger("rabbitark.utils.load_dynamic_module")


def import_dynamic_module(path: str) -> Any:
    logger.debug("extractor path: %s", path)
    spec: ModuleSpec = importlib.util.spec_from_file_location("dynamic_module", path)
    a = importlib.util.module_from_spec(spec)
    logger.info("sucees import")
