from typing import Any, Optional
import aiohttp


class Requester:
    def __init__(
        self,
        user_agent: Optional[str] = None,
        range: Optional[str] = None,
        referer: Optional[str] = None,
        origin: Optional[str] = None,
    ):
        self.referer = referer
        self.user_agent = user_agent
        self.range = range
        self.origin = origin

    @property
    def headers(self):
        headers = {}
        if self.referer:
            headers.update({"referer": self.referer})
        if self.user_agent:
            headers.update({"User-Agent": self.user_agent})
        if self.range:
            headers.update({"Range": self.range})
        if self.origin:
            headers.update({"origin": self.range})
        return headers

    async def request(
        self, url: str, method: str, response_method: str, json: Any = None
    ) -> Any:
        async with aiohttp.ClientSession(headers=self.headers) as cs:
            async with cs.request(
                method,
                url,
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
                return await dispatch[response_method]()

    async def get(self, url: str, response_method: str = "read") -> Any:
        """Perform HTTP GET request."""
        return await self.request(url, "GET", response_method)

    async def post(self, url: str, response_method: str, json: Any = None) -> Any:
        """Perform HTTP POST request."""
        return await self.request(url, "POST", response_method, json)