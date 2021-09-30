import logging
import pandas as pd

import data
from common.selenium_basics import scroll
from common.selenium_context import SeleniumContext
from config import MASTER_CONFIG
from navigation.scroll_box_navigation import ScrollBoxNavigator


class ActivityNavigator:

    def __init__(self, driver):
        self.driver = driver
        self.execute_from_activity = {
            'extract/users': self.get_to_users,
        }
        self.context = None
        self.activity_config = MASTER_CONFIG["from_activity"]["extract"]["users"]

    def get_from_activity(self, execution_list: list):
        activities = pd.read_csv(f"{data.input_dir}/activities.csv")
        total_activities = len(activities)
        logging.info(f"{total_activities} activities found for scrapping")

        for index, row in activities.iterrows():
            activity = row
            logging.info(f"Seeing activity {index + 1} out of {total_activities}: {activity['name']}")
            self.go_to_activity(activity, execution_list)
            # TODO: parallel execution tabs!

    def go_to_activity(self, activity_info, execution_list):
        activity_name = activity_info['name']
        url = activity_info['url']
        wait_xpath = "//div[@class='Scrollbox--content']"
        click_xpath = "//div[@class='SearchFilter-expand-icon-container']"
        wait_xpath_disappear = "//div[contains(@class,'SearchFilter--isFilterSidebarOpen')]"
        self.context = SeleniumContext(name=activity_name, url=url, wait_xpath=wait_xpath)\
            .clone(click_xpath=click_xpath, wait_xpath_disappear=wait_xpath_disappear)
        self.context.go_there(self.driver)
        scroll(self.driver, down=True, intensity=2)

        for to_do in execution_list:
            logging.info(f"Doing: {to_do} from activity {activity_name}...")
            exec_func = self.execute_from_activity[to_do]
            exec_func()
            # TODO: SAVE PROGRESS

    def do_with_trading_history(self, action):
        dr = self.driver
        to_collect = self.activity_config["from/to"]
        total_users = self.activity_config["first_n_users"]

        box_context = self.context.clone(click_xpath=self.context.wait_xpath)
        scroll_box_navigator = ScrollBoxNavigator(dr, to_collect, box_context, total_users)
        if action == "extract":
            scroll_box_navigator.get_users()

    def get_to_users(self):
        self.do_with_trading_history("extract")
