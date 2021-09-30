import logging

from common.selenium_basics import get_driver
from common.utils import get_execution_list_from_config
from config import MASTER_CONFIG
from navigation.activity_navigator import ActivityNavigator
from navigation.profile_navigator import ProfileNavigator


def scrap(driver=None):

    if not driver:
        driver = get_driver()

    jobs = get_execution_list_from_config(MASTER_CONFIG, "")
    for job in jobs:
        job_extract_config = MASTER_CONFIG[job]
        if job_extract_config["enabled"]:
            execution_list = get_execution_list_from_config(job_extract_config, "extract")
            if execution_list:
                if job == "from_activity":
                    activity_navigator = ActivityNavigator(driver)
                    activity_navigator.get_from_activity(execution_list)
                elif job == "from_profile":
                    profiles_navigator = ProfileNavigator(driver)
                    profiles_navigator.get_from_profile(execution_list)

    logging.info(f"SUCCESSFUL execution, all the scrapping jobs were done")


if __name__ == "__main__":
    scrap()
