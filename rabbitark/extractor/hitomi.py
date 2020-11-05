import json
import re

from rabbitark.utils import Requester
from rabbitark.utils.default_class import Image
from rabbitark.utils.default_class import Info


class HitomiImageModel:
    def __init__(self, width: int, hash_: str, haswebp: int, name: str, height: int):
        self.width = int(width)
        self.hash_ = str(hash_)
        self.haswebp = bool(haswebp)
        self.name = str(name)
        self.height = int(height)


class HitomiGalleryInfoModel:
    def __init__(
        self,
        language_localname: str,
        language: str,
        date: str,
        files: list,
        tags: list,
        japanese_title: str,
        title: str,
        galleryid: int,
        type_: str,
    ):
        self.language_localname = language_localname
        self.language = language
        self.date = date
        self.files = files
        self.tags = tags
        self.japanese_title = japanese_title
        self.title = title
        self.galleryid = galleryid
        self.type_ = type_


class HitomiRequester(Requester):
    def __init__(self):
        super().__init__(
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                "referer": "https://hitomi.la",
            }
        )

    async def get_galleryinfo(self, index):
        response = await self.get(f"https://ltn.hitomi.la/galleries/{index}.js", "text")
        js_to_json = response.body.replace("var galleryinfo = ", "")
        return parse_galleryinfo(json.loads(js_to_json))

    async def images(self, index: int) -> tuple[list[Image], HitomiGalleryInfoModel]:
        galleryinfomodel = await self.get_galleryinfo(index)
        if not galleryinfomodel:
            return None
        images = [
            Image(image_url_from_image(index, img, True), img.name)
            for img in image_model_generator(galleryinfomodel.files)
        ]
        return images, galleryinfomodel


class Hitomi(HitomiRequester):
    def __init__(self) -> None:
        super().__init__()

    async def download_info(self, index) -> Info:
        images, model = await self.images(index)
        return Info(images, model.galleryid, self.headers)

    async def multiple_download_info(self, index_list: list):
        for index in index_list:
            yield self.download_info(index)


def subdomain_from_galleryid(g: int, number_of_frontends: int) -> str:
    o = g % number_of_frontends
    r = chr(97 + o)
    return r


def subdomain_from_url(url: str) -> str:
    retval = "b"

    number_of_frontends = 3
    b = 16

    r = re.compile(r"\/[0-9a-f]\/([0-9a-f]{2})\/")
    m = r.search(url)

    g = int(m[1], b)

    if g < 0x30:
        number_of_frontends = 2

    if g < 0x09:
        g = 1

    retval = subdomain_from_galleryid(g, number_of_frontends) + retval

    return retval


def url_from_url(url: str) -> str:
    r = re.compile(r"\/\/..?\.hitomi\.la\/")
    s = subdomain_from_url(url)
    return r.sub(f"//{s}.hitomi.la/", url)


def full_path_from_hash(hash_: str) -> str:
    if len(hash_) < 3:
        return hash_

    result = hash_[len(hash_) - 3 :]
    a = result[0:2]
    b = result[-1]
    return f"{b}/{a}/" + hash_


def url_from_hash(
    galleryid: int, image: HitomiImageModel, dir_: str = None, ext: str = None
) -> str:
    e = image.name.split(".")[-1]
    if ext:
        e = ext

    d = "images"

    if dir_:
        e = dir_
        d = dir_

    r = full_path_from_hash(image.hash_)

    return "https://a.hitomi.la/" + d + "/" + r + "." + e


def url_from_url_from_hash(
    galleryid: int, image: HitomiImageModel, dir_: str = None, ext: str = None
) -> str:
    a = url_from_hash(galleryid, image, dir_, ext)
    b = url_from_url(a)
    return b


def image_url_from_image(galleryid: int, image: HitomiImageModel, no_webp: bool) -> str:
    webp = None
    if image.hash_ and image.haswebp and not no_webp:
        webp = "webp"

    return url_from_url_from_hash(galleryid, image, webp)


def parse_galleryinfo(galleryinfo_json: dict) -> HitomiGalleryInfoModel:
    if not galleryinfo_json["tags"]:
        parsed_tags = []
    else:
        parsed_tags = []
        for tag in galleryinfo_json["tags"]:
            if not tag.get("male") and tag.get("female"):
                parsed_tags.append({"value": f"female:{tag['tag']}", "url": tag["url"]})
            elif tag.get("male") and not tag.get("female"):
                parsed_tags.append({"value": f"male:{tag['tag']}", "url": tag["url"]})
            elif not tag.get("male") and not tag.get("female"):
                parsed_tags.append({"value": f"tag:{tag['tag']}", "url": tag["url"]})
            elif tag.get("male") and tag.get("female"):
                raise Exception
            else:
                raise Exception

    return HitomiGalleryInfoModel(
        galleryinfo_json.get("language_localname"),
        galleryinfo_json.get("language"),
        galleryinfo_json.get("date"),
        galleryinfo_json.get("files"),
        parsed_tags,
        galleryinfo_json.get("japanese_title"),
        galleryinfo_json.get("title"),
        galleryinfo_json.get("id"),
        galleryinfo_json.get("type"),
    )


def image_model_generator(files: list):
    for file_ in files:
        yield HitomiImageModel(
            file_["width"],
            file_["hash"],
            file_["haswebp"],
            file_["name"],
            file_["height"],
        )
