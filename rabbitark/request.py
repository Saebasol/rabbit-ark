from typing import Any, Optional
from aiohttp import ClientSession
from rabbitark.types import Response

from rabbitark.typing import Method, ReturnMethod


class Request:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    }

    def __init__(self, session: Optional[ClientSession] = None, **options: Any):
        self.session = session
        self.options = options


    async def request(
        self,
        method: Method,
        url: str,
        return_method: ReturnMethod = "read",
        **kwargs: Any
    ) -> Response:
        if self.session is None:
            self.session = ClientSession(**self.options)

        async with self.session.request(method, url, **kwargs) as response:
            return Response(
                response.status,
                await getattr(response, return_method)(),
                response.url,
                response.headers,
            )

    async def get(
        self, url: str, return_method: ReturnMethod = "read", **kwargs: Any
    ) -> Response:
        return await self.request("GET", url, return_method, **kwargs)

    async def post(
        self, url: str, return_method: ReturnMethod = "read", **kwargs: Any
    ) -> Response:
        return await self.request("POST", url, return_method, **kwargs)
