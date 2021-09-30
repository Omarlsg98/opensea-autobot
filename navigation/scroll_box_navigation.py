import logging
import time
from datetime import datetime

import data
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from common.selenium_basics import scroll, wait_element_by_xpath
from common.utils import append_to_csv, sleep_random
from common.selenium_context import SeleniumContext
from config import SECS_TO_RE_CLICK, MAX_RETRIES
from objects.user import User


class ScrollBoxNavigator:

    def __init__(self, driver, to_collect, context: SeleniumContext, users_to_collect):
        self.driver = driver
        self.to_collect = to_collect
        self.context = context

        self.total_users = users_to_collect
        self.users_found = set()

    def get_users(self) -> set:
        """
        Best effort method to retrieve the users in a scroll box\n
        Use this to obtain followers list, following list and likes list

        :return: users set
        """

        prev_users_found = 0
        count = 0
        while count < 10 and prev_users_found < self.total_users:
            box_rows = self.driver.find_elements_by_xpath("//div[contains(@class,'EventHistory--row')]")

            for row in box_rows:
                users = row.find_elements_by_xpath(".//a[contains(@class,'AccountLink--ellipsis-overflow')]")
                if "To" in self.to_collect:
                    new_user = User(users[1].text, users[1].get_attribute("href"))
                    if new_user not in self.users_found:
                        new_user.save()
                        self.users_found.add(new_user)

            n_users_found = len(self.users_found)
            logging.info(f"{n_users_found} different users found out of {self.total_users} from {self.context.name}")

            if n_users_found == prev_users_found:
                count += 1
            else:
                count = 0

            self.context.click_click_xpath(self.driver)
            scroll(self.driver, down=True, intensity=1)
            prev_users_found = n_users_found
            sleep_random()

        logging.info(f"All users from {self.context.name} collected successfully")
        return self.users_found
