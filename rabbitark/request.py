from __future__ import annotations

from asyncio.tasks import wait
from functools import wraps
from math import ceil
from typing import Any, Awaitable, Callable, Optional, cast

from aiohttp import ClientSession

from rabbitark.abc import BaseExtractor, BaseRequest
from rabbitark.typing import CA, RETURN_METHOD


def close(f: CA) -> CA:
    @wraps(f)
    async def wrapper(self: BaseExtractor, *args: Any, **kwargs: Any):
        try:
            result = await f(self, *args, **kwargs)
        finally:
            if self.session:
                await self.session.close()
        return result

    return cast(CA, wrapper)


class Request(BaseRequest):
    def __init__(self) -> None:
        self.session: Optional[ClientSession] = None

    async def request(
        self,
        session: ClientSession,
        url: str,
        method: str,
        return_method: RETURN_METHOD,
        **kwargs: Any,
    ):
        response = await session.request(method, url, **kwargs)
        return await getattr(response, return_method)()

    async def get(
        self,
        url: str,
        return_method: RETURN_METHOD,
    ) -> Any:
        if not self.session:
            print("we make session")
            self.session = ClientSession()
        return await self.request(self.session, url, "GET", return_method)

    async def post(
        self,
        url: str,
        return_method: RETURN_METHOD,
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
        return_method: Optional[RETURN_METHOD] = None,
        request_per_session: int = 10,
        **kwargs: Any,
    ):
        try:
            pool_size = ceil(len(url) / request_per_session)

            request_per_session_url_list = [
                url[pos : pos + pool_size] for pos in range(0, len(url), pool_size)
            ]

            for _ in range(len(request_per_session_url_list)):
                self.session_pool.append(ClientSession())

            request_list = [
                request_func(session, url, method, return_method, **kwargs)
                for session, url_list in zip(
                    self.session_pool, request_per_session_url_list
                )
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
        return_method: RETURN_METHOD,
        request_per_session: int = 10,
        **kwargs: Any,
    ):
        return await self.request_using_session_pool(
            self.request, url, "GET", return_method, request_per_session, **kwargs
        )

    async def multiple_post(
        self,
        url: list[str],
        return_method: RETURN_METHOD,
        request_per_session: int = 10,
        **kwargs: Any,
    ):
        return await self.request_using_session_pool(
            self.request, url, "POST", return_method, request_per_session, **kwargs
        )
