from os import mkdir
from typing import TYPE_CHECKING
from asyncio.threads import to_thread

if TYPE_CHECKING:
    from _typeshed import StrOrBytesPath


async def async_mkdir(path: StrOrBytesPath) -> None:
    """
    Make a directory in a thread.

    :param path: The path to the directory.
    """
    await to_thread(mkdir, path)
