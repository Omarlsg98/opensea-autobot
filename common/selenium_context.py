import logging

from common.selenium_basics import wait_element_by_xpath, wait_element_disappear_by_xpath
from config import SECS_TO_RE_CLICK, TIMEOUT


class SeleniumContext:
    def __init__(self, name, url, wait_xpath=None, parent=None, click_xpath=None, wait_xpath_disappear=None):
        if (not url and not click_xpath) or (not wait_xpath and not wait_xpath_disappear):
            raise Exception(f"Incorrect instantiation of an InstagramContext")
        self.name = name
        self.url = url
        self.click_xpath = click_xpath
        self.wait_xpath = wait_xpath
        self.wait_xpath_disappear = wait_xpath_disappear
        self.parent = parent

    def clone(self, name=None, url=None, wait_xpath=None, parent=None, click_xpath=None, wait_xpath_disappear=None):
        return SeleniumContext(
            name=name if name else self.name,
            url=url if url else self.url,
            click_xpath=click_xpath if click_xpath else self.click_xpath,
            wait_xpath=wait_xpath if wait_xpath else self.wait_xpath,
            parent=parent if parent else self,
            wait_xpath_disappear=wait_xpath_disappear if wait_xpath_disappear else self.wait_xpath_disappear,
        )

    def click_click_xpath(self, driver):
        driver.find_element_by_xpath(self.click_xpath).click()

    def go_there(self, driver):
        context_chain = self.get_context_chain()
        for node in context_chain:
            if node.click_xpath:
                driver.find_element_by_xpath(node.click_xpath).click()
                if node.wait_xpath:
                    wait_element_by_xpath(driver, node.wait_xpath, False, SECS_TO_RE_CLICK)
                if node.wait_xpath_disappear:
                    wait_element_disappear_by_xpath(driver, node.wait_xpath_disappear, False, SECS_TO_RE_CLICK)
            else:
                driver.get(node.url)
                if node.wait_xpath:
                    wait_element_by_xpath(driver, node.wait_xpath)
                if node.wait_xpath_disappear:
                    wait_element_disappear_by_xpath(driver, node.wait_xpath_disappear)

    def get_context_chain(self):
        """
        Get context chain of actual node
        :return: context_chain organized from upmost parent to actual node
        """
        context_chain = [self]
        actual_node = self
        while actual_node.parent:
            actual_node = actual_node.parent
            context_chain.insert(0, actual_node)
            logging.info(actual_node)
        return context_chain

    def __str__(self):
        context_str = f"SeleniumContext(url={self.url}, name={self.name}, click_xpath:{self.click_xpath}, " + \
                      f"wait_xpath={self.wait_xpath}, wait_xpath_disappear={self.wait_xpath_disappear}"
        if self.parent:
            return context_str + f", parent:{self.parent.name})"
        return context_str + f", parent:NUll)"
