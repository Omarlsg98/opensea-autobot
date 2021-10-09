from common.selenium_basics import wait_for_popup, wait_element_by_xpath
from navigation.metamask_navigator import MetamaskNavigator


def login(driver):
    driver.get("https://opensea.io/login")
    opensea_window = driver.current_window_handle
    metamask = MetamaskNavigator(driver)
    driver.switch_to_window(opensea_window)
    handles_before = driver.window_handles
    driver.find_element_by_xpath('//button/div/span[text()="MetaMask"]').click()
    driver.switch_to_window(wait_for_popup(driver, handles_before))
    wait_element_by_xpath(driver, '//button[text()="Next"]')
    driver.find_element_by_xpath('//button[text()="Next"]').click()
    driver.find_element_by_xpath('//button[text()="Connect"]').click()
    driver.switch_to_window(opensea_window)
