import logging

from common.selenium_context import SeleniumContext
from config import METAMASK_ID
from secret_config import SECRET_RECOVERY_PHRASE, NEW_PASSWORD


class MetamaskNavigator:

    def __init__(self, driver):
        self.driver = driver
        self.metamask_window_handle = None
        self.context = None
        self.setup()

    def setup(self):
        driver = self.driver
        self.switch_to_metamask()
        driver.find_element_by_xpath('//button[text()="Get Started"]').click()
        driver.find_element_by_xpath('//button[text()="Import wallet"]').click()

        self.context = SeleniumContext(click_xpath="//button[text()='No Thanks']",
                                       wait_xpath="//div[@class='first-time-flow__checkbox']",
                                       name="MetaMask",
                                       url=f"chrome-extension://{METAMASK_ID}/home.html")
        self.context.go_there(driver)

        inputs = driver.find_elements_by_xpath('//input')
        inputs[0].send_keys(SECRET_RECOVERY_PHRASE)
        inputs[1].send_keys(NEW_PASSWORD)
        inputs[2].send_keys(NEW_PASSWORD)
        driver.find_element_by_css_selector('.first-time-flow__terms').click()
        driver.find_element_by_xpath('//button[text()="Import"]').click()
        logging.info("Successfully Metamask registration")

        self.context = SeleniumContext(wait_xpath="//button/span[text()='Unlock']",
                                       name="MetaMask",
                                       url=f"chrome-extension://{METAMASK_ID}/home.html")
        self.context.go_there(driver)

        inputs = driver.find_elements_by_xpath('//input')
        inputs[0].send_keys(NEW_PASSWORD)

        SeleniumContext(wait_xpath="//video", click_xpath="//button/span[text()='Unlock']").go_there(driver)
        driver.find_element_by_xpath('//button').click()
        SeleniumContext(wait_xpath="//section[contains(@class,'popover-wrap')]",
                        click_xpath='//button[text()="Remind me later"]').go_there(driver)
        driver.find_element_by_xpath('//button[@title="Close"]').click()
        logging.info("Successfully Metamask logging")

    def switch_to_metamask(self):
        if len(self.driver.window_handles) > 1:
            for window in self.driver.window_handles:
                if self.driver.title != "MetaMask":
                    self.driver.switch_to.window(window)
                else:
                    self.metamask_window_handle = self.driver.current_window_handle
                    break
        else:
            self.driver.get(f"chrome-extension://{METAMASK_ID}/home.html")
