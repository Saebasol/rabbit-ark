from typing import Any, Dict, List, Optional, Tuple

import aiohttp

from rabbitark.utils.default_class import Response


class Requester:
    def __init__(self, *args, **kwargs) -> None:
        self.args: Tuple = args
        self.kwargs: Dict[str, Any] = kwargs

    @property
    def headers(self) -> Optional[Dict[str, str]]:
        return self.kwargs.get("headers")

    async def request(
        self, url: str, method: str, response_method: str, *args, **kwargs
    ) -> Response:
        async with aiohttp.ClientSession(*self.args, **self.kwargs) as session:
            response = await self.fetch(
                session, url, method, response_method, *args, **kwargs
            )
            return response

    async def fetch(
        self,
        session: aiohttp.ClientSession,
        url: str,
        method: str,
        response_method: str,
        *args,
        **kwargs,
    ):
        async with session.request(method, url, *args, **kwargs) as response:
            dispatch: Dict[str, Any] = {
                "json": response.json,
                "read": response.read,
                "text": response.text,
            }
            if response_method not in dispatch:
                raise ValueError(f"Invalid response_method value: {response_method}")
            return Response(
                response.status, response.reason, await dispatch[response_method]()
            )

    async def get(
        self, url: str, response_method: str = "read", *args, **kwargs
    ) -> Response:
        """Perform HTTP GET request."""
        return await self.request(url, "GET", response_method, *args, **kwargs)

    async def post(self, url: str, response_method: str, *args, **kwargs) -> Response:
        """Perform HTTP POST request."""
        return await self.request(url, "POST", response_method, *args, **kwargs)
