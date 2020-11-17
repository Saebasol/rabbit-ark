import importlib.util
from importlib.machinery import ModuleSpec
from typing import Any


def import_dynamic_module(path: str) -> Any:
    spec: ModuleSpec = importlib.util.spec_from_file_location("dynamic_module", path)
    importlib.util.module_from_spec(spec)
