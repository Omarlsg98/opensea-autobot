import logging
import os

import pandas as pd
from selenium.webdriver.common.keys import Keys

import data
from common.opensea_common import login
from common.selenium_basics import get_driver, wait_element_by_xpath, wait_for_popup, center_and_click, \
    wait_any_element_to_have_text
from common.utils import create_csv_headers, append_to_csv, float_to_str


def list_all(driver=None, logged=False):
    if not driver:
        driver = get_driver()

    if not logged:
        login(driver)

    to_post = pd.read_csv(data.to_post_path)
    number_of_posts = len(to_post)

    posted = pd.read_csv(data.posted_path)
    posted["key"] = posted["collection"] + "/" + posted["name"]
    to_post["key"] = to_post["collection"] + "/" + to_post["name"]
    to_post = pd.merge(to_post, posted[['key', 'url']], on='key', how='left')

    if os.path.isfile(data.listed_path):
        listed = pd.read_csv(data.listed_path)
        listed["key"] = listed["collection"] + "/" + listed["name"]
        to_post = pd.merge(to_post, listed[['key', 'status']], on='key', how='left')
        to_post = to_post[to_post["status"].isnull()]
        del to_post["key"]
        del to_post["status"]

    for index, post_ in to_post.iterrows():
        index = index + 1

        if post_["list_n"] != 0:
            list_n = post_["list_n"]
            if post_["list_n"] == -1:
                list_n = post_["supply"]

            logging.info(f"{index}/{number_of_posts} -- Listing {list_n} copies of {post_['name']}")

            driver.get(f'{post_["url"]}/sell')
            wait_any_element_to_have_text(driver, "//div[contains(@class,'AssetSellPreviewFooter--name')]", post_['name'])

            quantity_inp = driver.find_element_by_xpath("//input[@id='quantity']")
            quantity_inp.send_keys(Keys.CONTROL + "a")
            quantity_inp.send_keys(Keys.DELETE)
            quantity_inp.send_keys(list_n)

            driver.find_element_by_xpath("//input[@id='price']").send_keys(float_to_str(post_['price']))

            center_and_click(driver, "//button[text()='Complete listing']")
            
            wait_element_by_xpath(driver, "//button[text()='Sign']")
            handles_before = driver.window_handles
            center_and_click(driver, "//button[text()='Sign']")
            popup_handle = wait_for_popup(driver, handles_before)

            opensea_window = driver.current_window_handle
            driver.switch_to.window(popup_handle)
            wait_element_by_xpath(driver, "//button[text()='Sign']")
            driver.find_element_by_xpath("//button[text()='Sign']").click()
            driver.switch_to.window(opensea_window)
            wait_any_element_to_have_text(driver, "//h4", "Your NFT is listed!")

            create_csv_headers(data.listed_path, "collection,name,status,quantity")
            append_to_csv(data.listed_path,
                          f"{post_['collection']},{post_['name']},done,{list_n}")
            logging.info(f"{index}/{number_of_posts} -- Successfully listed  {post_['name']}")

        else:
            logging.info(f"{index}/{number_of_posts} -- Skipping listing of  {post_['name']}")

    logging.info(f"SUCCESSFUL execution, all the listing jobs were done")


if __name__ == "__main__":
    list_all()
