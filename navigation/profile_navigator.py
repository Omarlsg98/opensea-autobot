import logging

import pandas as pd

import data
from common.selenium_context import SeleniumContext
from config import MASTER_CONFIG
from objects.user import User


class ProfileNavigator:

    def __init__(self, driver):
        self.driver = driver
        self.execute_from_profile = {
            'extract/socials': self.get_socials,
        }
        self.context = None
        self.profile_config = MASTER_CONFIG["from_profile"]["extract"]["socials"]
        self.current_profile = None

    def get_from_profile(self, execution_list: list):
        profiles = pd.read_csv(f"{data.users_temp_path}")
        total_profiles = len(profiles)
        logging.info(f"{total_profiles} profiles found for scrapping")

        for index, row in profiles.iterrows():
            profile = row
            logging.info(f"Seeing profile {index + 1} out of {total_profiles}: {profile['name']}")
            self.go_to_profile(profile, execution_list)
            # TODO: parallel execution tabs!

    def go_to_profile(self, profile_info, execution_list):
        profile_name = profile_info['name']
        url = profile_info['url']
        wait_xpath = "//div[@class='AccountHeader--title']"
        self.context = SeleniumContext(name=profile_name, url=url, wait_xpath=wait_xpath)
        self.context.go_there(self.driver)

        self.current_profile = profile_info
        for to_do in execution_list:
            logging.info(f"Doing: {to_do} from profile {profile_name}...")
            exec_func = self.execute_from_profile[to_do]
            exec_func()
            # TODO: SAVE PROGRESS

    def get_socials(self):
        socials = self.driver.find_elements_by_xpath("//a[contains(@class,'AccountHeader--social-container')]")

        if socials:
            logging.info(f"Some socials found for {self.current_profile['name']}")
            twitter = None
            instagram = None
            for social in socials:
                social_link = social.get_attribute("href")
                if "twitter" in social_link:
                    twitter = social_link
                elif "instagram" in social_link:
                    instagram = social_link

            new_user = User(name=self.current_profile["name"],
                            url=self.current_profile["url"],
                            twitter=twitter,
                            instagram=instagram)
            new_user.save()
