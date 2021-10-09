import logging
import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import data
from common.opensea_common import login
from common.selenium_basics import get_driver, wait_element_by_xpath, wait_for_popup, write_text,\
    center_element_on_screen
import pandas as pd

from common.utils import format_properties, create_csv_headers, append_to_csv


def post(driver=None, logged=False):
    if not driver:
        driver = get_driver()

    if not logged:
        login(driver)

    wait_element_by_xpath(driver, "//div[@class='AccountHeader--title']")

    to_post = pd.read_csv(data.to_post_path)
    number_of_posts = len(to_post)
    if os.path.isfile(data.posted_path):
        posted = pd.read_csv(data.posted_path)
        posted["key"] = posted["collection"] + "/" + posted["name"]
        to_post["key"] = to_post["collection"] + "/" + to_post["name"]
        to_post = pd.merge(to_post, posted[['key', 'url']],
                           on='key',
                           how='left')
        to_post = to_post[to_post["url"].isnull()]
        del to_post["key"]
        del to_post["url"]
    for index, post_ in to_post.iterrows():
        index = index+1
        logging.info(f"{index}/{number_of_posts} -- Posting {post_['name']}")
        handles_before = driver.window_handles
        driver.find_element_by_xpath("//a[contains(@href,'asset/create')]").click()

        popup_handle = wait_for_popup(driver, handles_before,
                                      xpath_no_popup="//header[@class='CollectionManager--header-container']")
        if popup_handle:
            opensea_window = driver.current_window_handle
            driver.switch_to.window(popup_handle)
            wait_element_by_xpath(driver, "//button[text()='Sign']")
            driver.find_element_by_xpath("//button[text()='Sign']").click()
            driver.switch_to.window(opensea_window)

        inp_media = wait_element_by_xpath(driver, "//input[@id='media']")
        driver.execute_script("arguments[0].style.display = 'block';", inp_media)
        inp_media.send_keys(post_['media'])

        driver.find_element_by_xpath("//input[@id='name']").send_keys(post_['name'])

        if type(post_['external_link']) == str:
            driver.find_element_by_xpath("//input[@id='external_link']").send_keys(post_['external_link'])

        description_txt_area = driver.find_element_by_xpath("//textarea[@id='description']")
        write_text(driver, description_txt_area, post_['description'])
        description_txt_area.send_keys(" ")

        collection_inp = driver.find_element_by_xpath("//input[@placeholder = 'Select collection']")
        center_element_on_screen(driver, collection_inp)
        collection_inp.click()
        check = False
        for collection_btn in wait_element_by_xpath(driver, "//div[@data-tippy-root]//li/button", return_all=True):
            if collection_btn.text == post_["collection"]:
                collection_btn.click()
                check = True
                break
        if not check:
            raise Exception(f"Collection {post_['collection']} not found")

        if post_["properties"]:
            properties = format_properties(post_["properties"])
            driver.find_element_by_xpath("//div[@class='AssetFormTraitSection--item']//i[@value='add']").click()
            add_btn = wait_element_by_xpath(driver, "//button[text()='Add more']")
            for i in range(len(properties[0])):
                add_btn.click()
            type_inpts = driver.find_elements_by_xpath("//input[@placeholder='Character']")
            name_inpts = driver.find_elements_by_xpath("//input[@placeholder='Male']")
            for i in range(len(properties[0])):
                type_inpts[i].send_keys(properties[0][i])
                name_inpts[i].send_keys(properties[1][i])

            driver.find_element_by_xpath("//button[text()='Save']").click()

        chain_inp = driver.find_element_by_xpath("//input[@id='chain']")
        center_element_on_screen(driver, chain_inp)
        chain_inp.click()
        time.sleep(0.1)
        for chain_btn in wait_element_by_xpath(driver, "//div[@data-tippy-root]//li/button", return_all=True):
            if post_["chain"] in chain_btn.text:
                chain_btn.click()
                break

        time.sleep(0.1)
        chain_selected = chain_inp.get_attribute("value")
        if post_["chain"] != chain_selected:
            raise Exception(
                f"Error: {post_['chain']} chain could not be selected instead {chain_selected} was selected"
            )

        if chain_selected == "Polygon":
            supply_inp = driver.find_element_by_xpath("//input[@id='supply']")
            supply_inp.send_keys(Keys.CONTROL + "a")
            supply_inp.send_keys(Keys.DELETE)
            supply_inp.send_keys(post_['supply'])

        create_btn = driver.find_element_by_xpath("//button[text()='Create']")
        center_element_on_screen(driver, create_btn)
        create_btn.click()

        wait_element_by_xpath(driver, "//h4[contains(text(),'You created')]")

        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        post_url = driver.current_url
        create_csv_headers(data.posted_path, "collection,name,url")
        append_to_csv(data.posted_path,
                      f"{post_['collection']},{post_['name']},{post_url}")

        logging.info(f"{index}/{number_of_posts} -- Successfully posted  {post_['name']}")

    logging.info(f"SUCCESSFUL execution, all the posting jobs were done")


if __name__ == "__main__":
    post()
