class Image:
    def __init__(self, url: str, filename: str = None):
        self.url = url
        self.filename = filename if filename else url.rsplit("/", 1)[1]


class Info:
    def __init__(self, title: str, image: list[Image]):
        self.title = title
        self.image = image


class DownloadInfo:
    def __init__(self, url: str, directory: str):
        self.url = url
        self.directory = directory
