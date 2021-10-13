import logging
import time

from common.selenium_basics import wait_for_popup, wait_element_by_xpath
from navigation.metamask_navigator import MetamaskNavigator
from config import LOGIN_TIMEOUT


def login(driver):
    driver.get("https://opensea.io/login")
    opensea_window = driver.current_window_handle
    MetamaskNavigator(driver)
    driver.switch_to.window(opensea_window)

    handles_before = driver.window_handles
    wait_element_by_xpath(driver, '//button/div/span[text()="MetaMask"]', wait_time=LOGIN_TIMEOUT).click()
    driver.switch_to.window(wait_for_popup(driver, handles_before))
    wait_element_by_xpath(driver, '//button[text()="Next"]')
    driver.find_element_by_xpath('//button[text()="Next"]').click()
    driver.find_element_by_xpath('//button[text()="Connect"]').click()
    driver.switch_to.window(opensea_window)

    wait_element_by_xpath(driver, "//div[@class='AccountHeader--title']")
    logging.info("Successfully logged on opensea ")