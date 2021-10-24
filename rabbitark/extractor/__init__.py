import logging
import os
import re
import sys
import traceback
from importlib import import_module

logger = logging.getLogger(__name__)

if getattr(sys, "frozen", False):
    logger.info("detect exe extractor folder as a temporary folder")
    directory = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
else:
    directory = os.path.dirname(os.path.realpath(__file__))


def load():
    failed = []

    for extension in [
        re.sub(".py", "", file)
        for file in os.listdir(directory)
        if not "__" in file
        if os.path.splitext(file)[1] == ".py"
    ]:
        try:
            logger.debug("import %s", extension)
            import_module(
                extension
                if getattr(sys, "frozen", False)
                else f"rabbitark.extractor.{extension}"
            )
        except:
            traceback.print_exc()
            failed.append(extension)
