from typing import Any

import aiohttp
from aiohttp.client_reqrep import ClientResponse

from rabbitark.utils.default_class import Response


class Request:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.session = None

    @property
    def headers(self):
        return self.kwargs.get("headers")

    async def fetch(
        self,
        session: aiohttp.ClientSession,
        url: str,
        method: str,
        response_method: str,
        *args,
        **kwargs,
    ) -> ClientResponse:
        async with session.request(method, url, *args, **kwargs) as response:
            dispatch: dict[str, Any] = {
                "json": response.json,
                "read": response.read,
                "text": response.text,
            }
            if response_method not in dispatch:
                raise ValueError(f"Invalid response_method value: {response_method}")
            return Response(
                response.status, response.reason, await dispatch[response_method]()
            )

    async def request(
        self, url: str, method: str, response_method: str, *args, **kwargs
    ) -> Response:
        async with aiohttp.ClientSession(*self.args, **self.kwargs) as session:
            response = await self.fetch(
                session, url, method, response_method, *args, **kwargs
            )
            return response

    async def get(
        self, url: str, response_method: str = "read", *args, **kwargs
    ) -> Response:
        """Perform HTTP GET request."""
        return await self.request(url, "GET", response_method, *args, **kwargs)

    async def post(self, url: str, response_method: str, *args, **kwargs) -> Response:
        """Perform HTTP POST request."""
        return await self.request(url, "POST", response_method, *args, **kwargs)

    async def session_request(
        self, url: str, method: str, response_method: str, *args, **kwargs
    ) -> Response:
        if not self.session:
            raise Exception
        response = await self.fetch(
            self.session, url, method, response_method, *args, **kwargs
        )
        return response

    async def session_get(
        self, url: str, response_method: str = "read", *args, **kwargs
    ) -> Response:
        return await self.session_request(url, "GET", response_method, *args, **kwargs)

    async def session_post(
        self, url: str, response_method: str, *args, **kwargs
    ) -> Response:
        return await self.session_request(url, "POST", response_method, *args, **kwargs)
