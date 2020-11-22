import argparse
import asyncio
import logging
import multiprocessing
import platform
import sys

from rabbitark.config import config
from rabbitark.extractor import load
from rabbitark.rabbitark import RabbitArk
from rabbitark.utils.utils import load_cookie_txt

logger = logging.getLogger("rabbitark")
logger.setLevel(logging.DEBUG)

# formatter
formatter = logging.Formatter("%(asctime)s - (%(name)s) - [%(levelname)s]: %(message)s")

# console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)


if getattr(sys, "frozen", False):
    multiprocessing.freeze_support()
    logger.info("detect exe called freeze_support")

parser: argparse.ArgumentParser = argparse.ArgumentParser("rabbitark")

parser.add_argument("extractor", type=str, help="Specifies the extractor name")

parser.add_argument(
    "--downloadable",
    help="It takes a url or an available argument value.",
    default=None,
)

parser.add_argument("--base", type=str, help="Specifies the pre-created folder")

parser.add_argument("--folder", type=str, help="Specifies the folder name")

parser.add_argument("--cookies", type=str, help="load cookies.txt")

parser.add_argument("--page", type=int, help="Youtube page limit")

parser.add_argument("--custom_extractor", type=str, help="use custom extractor")

parser.add_argument(
    "--verbose", action="store_true", help="print debugging information"
)

parser.add_argument("--report", action="store_true", help="save debugging informaion")

args: argparse.Namespace = parser.parse_args()

if args.base:
    config.BASE_DIRECTORY = args.folder

if not args.folder:
    config.FOLDER = f"rabbitark_{args.extractor}"

if args.cookies:
    config.COOKIES = load_cookie_txt(args.cookies)

if args.page:
    config.YOUTUBE_PAGE_LIMIT = args.page

if args.custom_extractor:
    config.CUSTOM_EXTRACTOR = args.custom_extractor

if args.verbose:
    ch.setLevel(logging.DEBUG)

if args.report:
    fh = logging.FileHandler("rabbitark.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

logger.debug("system ver: %s %s", platform.python_implementation(), sys.version)
logger.debug("platform: %s", platform.platform())
logger.debug("args: %s", sys.argv[1:])

logger.info("start import extractor")
load()
logger.info("sucessfully import extractor")

logger.debug("start loop")
asyncio.run(RabbitArk(args.extractor).start(args.downloadable))
logger.debug("complete loop")
