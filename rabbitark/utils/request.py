import aiohttp

from ..utils.default_class import Response


class Requester:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @property
    def headers(self):
        return self.kwargs.get("headers")

    async def request(
        self, url: str, method: str, response_method: str, *args, **kwargs
    ) -> Response:
        async with aiohttp.ClientSession(*self.args, **self.kwargs) as cs:
            async with cs.request(method, url, *args, **kwargs) as response:
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
        self, url: str, response_method: str = "read", *args, **kwargs
    ) -> Response:
        """Perform HTTP GET request."""
        return await self.request(url, "GET", response_method, *args, **kwargs)

    async def post(self, url: str, response_method: str, *args, **kwargs) -> Response:
        """Perform HTTP POST request."""
        return await self.request(url, "POST", response_method, *args, **kwargs)
