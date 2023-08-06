"""
    gpd.py
    ------------------

    Runs the project.

    :copyright: 2019 MislavJaksic
    :license: MIT License
"""
import argparse
import pickle
import socket
import sys
import time
from typing import Dict, Any, List

import requests
from loguru import logger
from tqdm import tqdm

from gpd.dependent_cache import DependentCache
from gpd.dependents_stats import DependentsStats
from gpd.models.dependent import Dependent
from gpd.parsers.table_page_parser import TablePageParser


def main() -> int:
    """main() will be run if you run this script directly"""
    args = get_cli_arguments()

    setup_loguru()

    cache = DependentCache(args["owner"], args["name"], args["max_page"])
    dependents = cache.dependents_from_file()
    if not dependents:
        dependents = get_dependents(args["owner"], args["name"], args["max_page"])
        cache.dependents_to_file(dependents)

    stats = DependentsStats(dependents)
    print(stats.get_top_stars())

    return 0


def get_dependents(owner: str, project: str, max_page: int) -> List[Dependent]:
    page_number: int = 0
    next_url: str = 'https://github.com/{}/{}/network/dependents'.format(owner, project)
    request = None
    dependents: List[Dependent] = []
    estimated_pages = get_estimate_of_dependent_pages(next_url)
    try:
        logger.info("start_url={start_url}, max_page={max_page}, estimated_pages={estimated_pages}", start_url=next_url, max_page=max_page, estimated_pages=estimated_pages)
        for page_number in tqdm(range(min(estimated_pages, max_page))):
            request = requests.get(next_url)
            parser = TablePageParser(request.text)

            dependents += parser.get_dependents()
            next_url = parser.get_next_page_url()

            time.sleep(1.5)
            if not next_url:
                break
    except:
        logger.exception("start_url={start_url}, next_url={next_url}, page_number={page_number}, request={request}", start_url='https://github.com/{}/{}/network/dependents'.format(owner, project), next_url=next_url, page_number=page_number, request=request)
        if request:
            with open("latest-error.html", 'wb') as f:
                f.write(request.content)
    return dependents

def get_estimate_of_dependent_pages(url: str):
    request = requests.get(url)
    parser = TablePageParser(request.text)
    dependents_estimate = parser.get_dependents_estimate()
    return int(dependents_estimate * 1.2 / 30)

def get_cli_arguments() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(description="",
                                     epilog="")

    parser.add_argument("-o", "--owner", required=True, help="Project owner. For example 'github' in 'https://github.com/github/advisory-database'.")
    parser.add_argument("-n", "--name", required=True, help="Project name. For example 'advisory-database' in 'https://github.com/github/advisory-database'.")
    parser.add_argument("-m", "--max_page", type=int, nargs='?', const=sys.maxsize, default=sys.maxsize, help="How many pages of dependents do you want to parse before finishing. Default is sys.maxsize, infinity.")

    return vars(parser.parse_args())


def setup_loguru() -> None:
    host = socket.gethostname()
    ip = socket.gethostbyname(host)

    config = {
        "handlers": [
            {"sink": sys.stderr, "diagnose": False,
             "format": '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{extra[host]}</cyan>:<cyan>{extra[ip]}</cyan> | <cyan>{process}</cyan>:<cyan>{thread}</cyan> | <cyan>{module}</cyan>:<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>'},
            {"sink": "file.log", "retention": "7 days", "serialize": True},
        ],
        "extra": {"host": host, "ip": ip},
    }
    logger.configure(**config)  # type: ignore


def run() -> None:
    """Entry point for the runnable script."""
    sys.exit(main())


if __name__ == "__main__":
    """main calls run()."""
    run()
