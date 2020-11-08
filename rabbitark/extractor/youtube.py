"""
Youtube Playlist Extractor

https://github.com/kijk2869/discodo/blob/master/discodo/extractor/youtube/playlist.py

Used in function: extract_playlist

MIT License

Copyright (c) 2020 매리

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Youtube URL Regex

youtube_dl/extractor/youtube.py

Used in constant: VALID_URL, PLAYLIST_VAILD_URL

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
"""

import json
import re

from rabbitark.error import NotFound
from rabbitark.utils.default_class import Image, Info
from rabbitark.utils.request import Requester

VALID_URL = r"""(?x)^
                     (
                         (?:https?://|//)                                    # http(s):// or protocol-independent URL
                         (?:(?:(?:(?:\w+\.)?[yY][oO][uU][tT][uU][bB][eE](?:-nocookie|kids)?\.com/|
                            (?:www\.)?deturl\.com/www\.youtube\.com/|
                            (?:www\.)?pwnyoutube\.com/|
                            (?:www\.)?hooktube\.com/|
                            (?:www\.)?yourepeat\.com/|
                            tube\.majestyc\.net/|
                            # Invidious instances taken from https://github.com/omarroth/invidious/wiki/Invidious-Instances
                            (?:(?:www|dev)\.)?invidio\.us/|
                            (?:(?:www|no)\.)?invidiou\.sh/|
                            (?:(?:www|fi|de)\.)?invidious\.snopyta\.org/|
                            (?:www\.)?invidious\.kabi\.tk/|
                            (?:www\.)?invidious\.13ad\.de/|
                            (?:www\.)?invidious\.mastodon\.host/|
                            (?:www\.)?invidious\.nixnet\.xyz/|
                            (?:www\.)?invidious\.drycat\.fr/|
                            (?:www\.)?tube\.poal\.co/|
                            (?:www\.)?vid\.wxzm\.sx/|
                            (?:www\.)?yewtu\.be/|
                            (?:www\.)?yt\.elukerio\.org/|
                            (?:www\.)?yt\.lelux\.fi/|
                            (?:www\.)?invidious\.ggc-project\.de/|
                            (?:www\.)?yt\.maisputain\.ovh/|
                            (?:www\.)?invidious\.13ad\.de/|
                            (?:www\.)?invidious\.toot\.koeln/|
                            (?:www\.)?invidious\.fdn\.fr/|
                            (?:www\.)?watch\.nettohikari\.com/|
                            (?:www\.)?kgg2m7yk5aybusll\.onion/|
                            (?:www\.)?qklhadlycap4cnod\.onion/|
                            (?:www\.)?axqzx4s6s54s32yentfqojs3x5i7faxza6xo3ehd4bzzsg2ii4fv2iid\.onion/|
                            (?:www\.)?c7hqkpkpemu6e7emz5b4vyz7idjgdvgaaa3dyimmeojqbgpea3xqjoid\.onion/|
                            (?:www\.)?fz253lmuao3strwbfbmx46yu7acac2jz27iwtorgmbqlkurlclmancad\.onion/|
                            (?:www\.)?invidious\.l4qlywnpwqsluw65ts7md3khrivpirse744un3x7mlskqauz5pyuzgqd\.onion/|
                            (?:www\.)?owxfohz4kjyv25fvlqilyxast7inivgiktls3th44jhk3ej3i7ya\.b32\.i2p/|
                            (?:www\.)?4l2dgddgsrkf2ous66i6seeyi6etzfgrue332grh2n7madpwopotugyd\.onion/|
                            youtube\.googleapis\.com/)                        # the various hostnames, with wildcard subdomains
                         (?:.*?\#/)?                                          # handle anchor (#/) redirect urls
                         (?:                                                  # the various things that can precede the ID:
                             (?:(?:v|embed|e)/(?!videoseries))                # v/ or embed/ or e/
                             |(?:                                             # or the v= param in all its forms
                                 (?:(?:watch|movie)(?:_popup)?(?:\.php)?/?)?  # preceding watch(_popup|.php) or nothing (like /?v=xxxx)
                                 (?:\?|\#!?)                                  # the params delimiter ? or # or #!
                                 (?:.*?[&;])??                                # any other preceding param (like /?s=tuff&v=xxxx or ?s=tuff&amp;v=V36LpHqtcDY)
                                 v=
                             )
                         ))
                         |(?:
                            youtu\.be|                                        # just youtu.be/xxxx
                            vid\.plus|                                        # or vid.plus/xxxx
                            zwearz\.com/watch|                                # or zwearz.com/watch/xxxx
                         )/
                         |(?:www\.)?cleanvideosearch\.com/media/action/yt/watch\?videoId=
                         )
                     )?                                                       # all until now is optional -> you can pass the naked ID
                     ([0-9A-Za-z_-]{11})                                      # here is it! the YouTube video ID
                     (?!.*?\blist=
                        (?:
                            %(playlist_id)s|                                  # combined list/video URLs are handled by the playlist IE
                            WL                                                # WL are handled by the watch later IE
                        )
                     )
                     (?(1).+)?                                                # if we found the ID, everything can follow
                     $"""

PLAYLIST_VALID_URL = r"""(?x)(?:
                    (?:https?://)?
                    (?:\w+\.)?
                    (?:
                        (?:
                            youtube(?:kids)?\.com|
                            invidio\.us
                        )
                        /
                        (?:
                            (?:course|view_play_list|my_playlists|artist|playlist|watch|embed/(?:videoseries|[0-9A-Za-z_-]{11}))
                            \? (?:.*?[&;])*? (?:p|a|list)=
                        |  p/
                        )|
                        youtu\.be/[0-9A-Za-z_-]{11}\?.*?\blist=
                    )
                    (
                        (?:PL|LL|EC|UU|FL|RD|UL|TL|PU|OLAK5uy_)?[0-9A-Za-z-_]{10,}
                        # Top tracks, they can also include dots
                        |(?:MC)[\w\.]*
                    )
                    .*
                    |
                    (%(playlist_id)s)
                    )"""


DATA_JSON = re.compile(
    r"(?:window\[\"ytInitialData\"\]|var ytInitialData)\s*=\s*(\{.*\})"
)

PLAYLIST_PREFIX_LIST = [
    "PL",
    "LL",
    "EC",
    "UU",
    "FL",
    "RD",
    "UL",
    "TL",
    "PU",
    "OLAK5uy_",
]


class YoutubeRequester(Requester):
    def __init__(self) -> None:
        super().__init__(
            headers={
                "x-youtube-client-name": "1",
                "x-youtube-client-version": "2.20201030.01.00",
            }
        )

    async def extract_playlist(self, playlist_id: str) -> dict:
        if playlist_id.startswith(("RD", "UL", "PU")):
            raise TypeError("playlistId is Youtube Mix id")

        body = await self.get(
            f"https://www.youtube.com/playlist",
            "text",
            params={"list": playlist_id, "hl": "en"},
        )

        search = DATA_JSON.search(body.body)

        if not search:
            raise ValueError

        Data: dict = json.loads(search.group(1))

        if Data.get("alerts"):
            raise Exception(Data["alerts"][0]["alertRenderer"]["text"]["simpleText"])

        firstPlaylistData: list = Data["contents"]["twoColumnBrowseResultsRenderer"][
            "tabs"
        ][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0][
            "itemSectionRenderer"
        ][
            "contents"
        ][
            0
        ][
            "playlistVideoListRenderer"
        ]

        Sources: list = []

        def extract_playlist(playlistData: dict, name: str = "contents") -> str:
            trackList: list = playlistData.get(name)
            if not trackList:
                return

            continuationsTokens: list = []

            def extract(Track: dict) -> dict:
                if "playlistVideoRenderer" in Track:
                    renderer: dict = Track.get("playlistVideoRenderer", {})
                    shortBylineText: dict = renderer.get("shortBylineText")

                    if not renderer.get("isPlayable") or not shortBylineText:
                        return

                    return {
                        "id": renderer["videoId"],
                        "title": renderer["title"].get("simpleText")
                        or renderer["title"]["runs"][0]["text"],
                        "webpage_url": "https://youtube.com/watch?v="
                        + renderer["videoId"],
                        "uploader": shortBylineText["runs"][0]["text"],
                        "duration": renderer["lengthSeconds"],
                    }
                elif "continuationItemRenderer" in Track:
                    continuationsTokens.append(
                        Track["continuationItemRenderer"]["continuationEndpoint"][
                            "continuationCommand"
                        ]["token"]
                    )

                    return
                else:
                    return

            Sources.extend(map(extract, trackList))

            if not continuationsTokens:
                return

            return (
                "https://www.youtube.com/browse_ajax?continuation="
                + continuationsTokens[0]
                + "&ctoken="
                + continuationsTokens[0]
                + "&hl=en"
            )

        continuations_url: str = extract_playlist(firstPlaylistData)
        for _ in range(6):
            if not continuations_url:
                break

            body = await self.get(continuations_url, "json")

            nextPlaylistData: dict = body[1]["response"]["onResponseReceivedActions"][
                0
            ]["appendContinuationItemsAction"]

            continuations_url: str = extract_playlist(
                nextPlaylistData, name="continuationItems"
            )

        return list(filter(None, Sources))

    async def checking_url(self, url):
        single_video = re.findall(VALID_URL, url)
        if single_video:
            return self.make_info_video(single_video[0][1])

        playlist = re.findall(PLAYLIST_VALID_URL, url)
        if playlist:
            return await self.make_info_playlist(playlist[0][0])

        return

    async def checking_id(self, yt_id: str):
        response = await self.get(
            f"https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={yt_id}"
        )
        if response.status != 200:
            for prefix in PLAYLIST_PREFIX_LIST:
                if yt_id.startswith(prefix):
                    return await self.make_info_playlist(yt_id)

            return

        return self.make_info_video(yt_id)

    def get_thumbnail(self, video_id):
        return Image(
            f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            f"{video_id}.jpg",
        )

    def make_info_video(self, video_id):
        return Info(self.get_thumbnail(video_id), video_id)

    async def make_info_playlist(self, playlist_id):
        video_infos = await self.extract_playlist(playlist_id)
        return Info(
            [self.get_thumbnail(info["id"]) for info in video_infos],
            playlist_id,
        )


class Youtube(YoutubeRequester):
    def __init__(self):
        super().__init__()

    async def download_info(self, downloadable) -> Info:
        first_check = await self.checking_url(downloadable)
        if first_check:
            return first_check

        second_check = await self.checking_id(downloadable)
        if second_check:
            return second_check

        raise NotFound(downloadable)
