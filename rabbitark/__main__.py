from logging import DEBUG, INFO, Formatter, StreamHandler, getLogger
from platform import python_implementation, platform
from sys import version, argv
from rabbitark.client import RabbitArk

from rabbitark.extractor import load

logger = getLogger("rabbitark")
logger.setLevel(DEBUG)

# Formatter
formatter = Formatter("%(asctime)s - (%(name)s) - [%(levelname)s]: %(message)s")

# Stream handler
sh = StreamHandler()
sh.setLevel(INFO)
sh.setFormatter(formatter)
logger.addHandler(sh)

logger.debug("System ver: %s %s", python_implementation(), version)
logger.debug("Platform: %s", platform())
logger.debug("Args: %s", argv[1:])

logger.debug("Start import extractor")
load()

import asyncio

asyncio.get_event_loop().run_until_complete(RabbitArk().run())
