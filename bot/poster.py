import logging
from time import sleep

from selenium.webdriver.support.wait import WebDriverWait

from common.selenium_basics import get_driver, wait_element_by_xpath, wait_for_popup
from common.utils import get_execution_list_from_config
from config import MASTER_CONFIG, METAMASK_ID, TIMEOUT
from navigation.activity_navigator import ActivityNavigator
from navigation.metamask_navigator import MetamaskNavigator
from navigation.profile_navigator import ProfileNavigator
from secret_config import SECRET_RECOVERY_PHRASE, NEW_PASSWORD
from selenium.webdriver.support import expected_conditions as EC


def login(driver, main_page):
    handles_before = driver.window_handles
    driver.find_element_by_xpath('//button[text()="Sign In"]').click()
    driver.switch_to_window(wait_for_popup(driver, handles_before))
    wait_element_by_xpath(driver, '//button[text()="Next"]')
    driver.find_element_by_xpath('//button[text()="Next"]').click()
    driver.find_element_by_xpath('//button[text()="Connect"]').click()


def post(driver=None):
    if not driver:
        driver = get_driver()
    driver.get("https://opensea.io/login")
    opensea_window = driver.current_window_handle
    metamask = MetamaskNavigator(driver)
    driver.switch_to_window(opensea_window)
    login(driver, opensea_window)

    # "https://opensea.io/collection/test-moarload"
    driver.find_element_by_xpath("//button[contains(@class,'Buttonreact__StyledButton')]").click()
    logging.info(f"SUCCESSFUL execution, all the posting jobs were done")


if __name__ == "__main__":
    post()
