from typing import Any, Optional
from rabbitark.utils.default_class import Response
import aiohttp


class Requester:
    def __init__(
        self,
        user_agent: Optional[str] = None,
        referer: Optional[str] = None,
    ):
        self.referer = referer
        self.user_agent = user_agent

    @property
    def headers(self):
        headers = {}
        if self.referer:
            headers.update({"referer": self.referer})
        if self.user_agent:
            headers.update({"User-Agent": self.user_agent})
        return headers

    async def request(
        self,
        url: str,
        method: str,
        response_method: str,
        headers: Any = None,
        json: Any = None,
    ) -> Response:
        async with aiohttp.ClientSession(headers=self.headers) as cs:
            async with cs.request(
                method,
                url,
                headers=headers,
                json=json,
            ) as response:
                dispatch = {
                    "json": response.json,
                    "read": response.read,
                    "text": response.text,
                }
                if response_method not in dispatch:
                    raise ValueError(
                        f"Invalid response_method value: {response_method}"
                    )
                return Response(
                    response.status, response.reason, await dispatch[response_method]()
                )

    async def get(
        self, url: str, response_method: str = "read", headers: Any = None
    ) -> Response:
        """Perform HTTP GET request."""
        return await self.request(url, "GET", response_method, headers)

    async def post(
        self, url: str, response_method: str, json: Any = None, headers: Any = None
    ) -> Response:
        """Perform HTTP POST request."""
        return await self.request(url, "POST", response_method, json, headers)