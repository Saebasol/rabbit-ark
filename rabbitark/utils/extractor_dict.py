from typing import Any, Dict

from rabbitark.extractor import Hitomi, Pixiv, Youtube

extractor: Dict[str, Any] = {"hitomi": Hitomi, "pixiv": Pixiv, "youtube": Youtube}
