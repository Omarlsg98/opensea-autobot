import logging

from common.selenium_basics import get_driver, closing_routine
from scrapper.scrapper import scrap


if __name__ == "__main__":
    driver = get_driver()
    try:
        scrap(driver)
        logging.info(f"SUCCESSFUL execution, ALL jobs were done")
    finally:
        closing_routine(driver)
