import logging

from common.selenium_basics import get_driver, closing_routine
from scrapper.scrapper import scrap
from bot.poster import post
from bot.lister import list_all


if __name__ == "__main__":
    driver = get_driver()
    try:
        # scrap(driver)
        post(driver)
        list_all(driver, logged=True)
        logging.info(f"SUCCESSFUL execution, ALL jobs were done")
    finally:
        closing_routine(driver)
