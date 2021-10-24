from types import SimpleNamespace
from typing import Any, Optional
from json import load as json_load


class Config(SimpleNamespace):
    def __getattr__(self, item: Any) -> Optional[Any]:
        return getattr(self, item)

    @classmethod
    def load(cls, path: str, extractor_names: list[str]):
        with open(path, "rb") as f:
            json_load(f)
