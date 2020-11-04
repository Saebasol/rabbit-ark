import importlib.util


def import_dynamic_module(path: str):
    spec = importlib.util.spec_from_file_location("dynamic_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_extensions(path):
    module = import_dynamic_module(path)
    main_class = module.load()
    return main_class
