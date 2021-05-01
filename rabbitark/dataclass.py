from typing import Any

from rabbitark.utils import Optional, split


class Image:
    def __init__(self, url: str, filename: Optional[str] = None) -> None:
        self.url: str = url
        self.filename: str = filename or split(url)


class DownloadInfo:
    def __init__(
        self, image: list[Image], title: Optional[str] = None, **kwargs: Any
    ) -> None:
        self.title = title
        self.image = image
        self.kwargs = kwargs

    def to_download(self, path: str):
        return {image.url: path + image.filename for image in self.image}


class Response:
    def __init__(self, status: int, message: Optional[Any], body: Any) -> None:
        self.status = status
        self.message = message
        self.body = body
