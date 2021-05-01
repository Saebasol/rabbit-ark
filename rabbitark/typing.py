from typing import Any, Awaitable, Callable, Literal, TypeVar

CA = TypeVar("CA", bound=Callable[..., Awaitable[Any]])

RETURN_METHOD = Literal["json", "text", "read"]
