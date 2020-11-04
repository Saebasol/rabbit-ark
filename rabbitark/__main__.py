import argparse
import asyncio

from rabbitark.rabbitark import RabbitArk
from rabbitark.config import config

parser = argparse.ArgumentParser("rabbitark")


parser.add_argument("extractor", type=str, help="Specifies the extractor to use")

parser.add_argument(
    "--downloadable",
    help="It takes a url or an available argument value.",
    default=None,
)

parser.add_argument("--base", type=str, help="Specifies the pre-created folder")

parser.add_argument("--folder", type=str, help="")

args = parser.parse_args()

if args.base:
    config.BASE_DIRECTORY = args.folder

if not args.folder:
    config.FOLDER = f"rabbitark_{args.extractor}"

if __name__ == "__main__":
    ark = RabbitArk(args.extractor)
    asyncio.run(ark.start(args.downloadable))
