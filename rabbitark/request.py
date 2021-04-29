from __future__ import annotations
from asyncio.tasks import wait

from typing import Any, Awaitable, Callable, Literal, Optional

from aiohttp import ClientSession
from math import ceil


class Request:
    def __init__(self) -> None:
        self.session: Optional[ClientSession] = None

    async def request(
        self,
        session: ClientSession,
        url: str,
        method: str,
        return_method: Literal["json", "text", "read"],
        **kwargs: Any,
    ):
        response = await session.request(method, url, **kwargs)
        return await getattr(response, return_method)()

    async def get(
        self,
        url: str,
        return_method: Literal["json", "text", "read"],
    ) -> Any:
        if not self.session:
            self.session = ClientSession()
        return await self.request(self.session, url, "GET", return_method)

    async def post(
        self,
        url: str,
        return_method: Literal["json", "text", "read"],
    ) -> Any:
        if not self.session:
            self.session = ClientSession()
            return await self.request(self.session, url, "POST", return_method)


class SessionPoolRequest(Request):
    def __init__(self) -> None:
        self._session_pool: list[ClientSession] = []

    @property
    def session_pool(self) -> list[ClientSession]:
        return self._session_pool

    async def request_using_session_pool(
        self,
        request_func: Callable[..., Awaitable[Any]],
        url: list[str],
        method: str,
        return_method: Optional[Literal["json", "text", "read"]] = None,
        division: int = 10,
        **kwargs: Any,
    ):
        try:
            pool_size = ceil(len(url) / division)

            division_url_list = [
                url[pos : pos + pool_size] for pos in range(0, len(url), pool_size)
            ]

            for _ in range(len(division_url_list)):
                self.session_pool.append(ClientSession())

            request_list = [
                request_func(session, url, method, return_method, **kwargs)
                for session, url_list in zip(self.session_pool, division_url_list)
                for url in url_list
            ]

            done, _ = await wait(request_list)
            return done

        finally:
            while self.session_pool:
                session = self.session_pool.pop(0)
                await session.close()

    async def multiple_get(
        self,
        url: list[str],
        return_method: Literal["json", "text", "read"],
        division: int = 10,
        **kwargs: Any,
    ):
        return await self.request_using_session_pool(
            self.request, url, "GET", return_method, division, **kwargs
        )

    async def multiple_post(
        self,
        url: list[str],
        return_method: Literal["json", "text", "read"],
        division: int = 10,
        **kwargs: Any,
    ):
        return await self.request_using_session_pool(
            self.request, url, "POST", return_method, division, **kwargs
        )
