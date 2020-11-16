import argparse
import asyncio
import multiprocessing
import sys

from rabbitark.config import config
from rabbitark.rabbitark import RabbitArk
from rabbitark.utils.utils import load_cookie_txt
from rabbitark.extractor import load

if getattr(sys, "frozen", False):
    multiprocessing.freeze_support()

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

load()
asyncio.run(RabbitArk(args.extractor).start(args.downloadable))
