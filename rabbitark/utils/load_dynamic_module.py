import importlib.util
from importlib.machinery import ModuleSpec
from typing import Any


def import_dynamic_module(path: str) -> Any:
    spec: ModuleSpec = importlib.util.spec_from_file_location("dynamic_module", path)
    module: Any = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    return module


def load_extensions(path):
    module: Any = import_dynamic_module(path)
    main_class: Any = module.load()
    return main_class
