from typing import Any, Awaitable, Callable, TypeVar

CA = TypeVar("CA", bound=Callable[..., Awaitable[Any]])
