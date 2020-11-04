from typing import Any


class Image:
    def __init__(self, url: str, filename: str = None):
        self.url = url
        self.filename = filename if filename else url.rsplit("/", 1)[1]


class Info:
    def __init__(self, image: list[Image], title: str = None, headers: Any = None):
        self.title = title
        self.image = image
        self.headers = headers


class DownloadInfo:
    def __init__(self, url: str, directory: str, headers: Any = None):
        self.url = url
        self.directory = directory
        self.headers = headers


class Response:
    def __init__(self, status: int, message: str, body: Any):
        self.status = status
        self.message = message
        self.body = body