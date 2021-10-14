import logging

from common.selenium_basics import get_driver, closing_routine
from scrapper.scrapper import scrap
from bot.poster import post
from bot.lister import list_all

from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument("-m", "--modes", nargs='+', default=[],
                        help="List of the actions that have to be done by the script: post list scrap")
    parser.add_argument("-b", "--batch_size", default=-1, type=int,
                        help="Amount of NFTs to post in this run")
    args = parser.parse_args()
    driver = get_driver()
    try:
        logged = False
        logging.info(f"Running with params --modes f{args.modes}")
        if "scrap" in args.modes:
            scrap(driver)
        if "post" in args.modes:
            post(driver, batch_size=args.batch_size)
            logged = True
        if "list" in args.modes:
            list_all(driver, logged=logged)
        logging.info(f"SUCCESSFUL execution, ALL jobs were done")
    finally:
        closing_routine(driver)


if __name__ == "__main__":
    main()
