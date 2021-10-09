import time
import logging

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from config import chrome_arguments, TIMEOUT, PING, SECS_BEFORE_CLOSING, MAX_RETRIES, \
    SECS_TO_RE_CLICK, DRIVER_PATH, METAMASK_PATH

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s - #%(levelname)s - %(message)s')


def center_element_on_screen(dr, element):
    js_center_element = """
        var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
        var elementTop = arguments[0].getBoundingClientRect().top;
        window.scrollBy(0, elementTop-(viewPortHeight/2));
        """
    dr.execute_script(js_center_element, element)


def write_text(dr, element, text):
    js_add_text_to_input = """
      var element = arguments[0], txt = arguments[1];
      element.innerHTML = txt;
      element.dispatchEvent(new Event('change'));
      """
    text = text.replace("\\n", "\n")
    dr.execute_script(js_add_text_to_input, element, text)


def hover(dr, element_to_hover_over):
    hover_act = ActionChains(dr).move_to_element(element_to_hover_over)
    hover_act.perform()


def scroll(dr, down: bool, intensity: int):
    body = dr.find_element_by_xpath("/html/body")
    if intensity == 1:
        if down:
            body.send_keys(Keys.PAGE_DOWN)
        else:
            body.send_keys(Keys.PAGE_UP)
    elif intensity == 2:
        if down:
            body.send_keys(Keys.END)
        else:
            body.send_keys(Keys.HOME)
    else:
        raise Exception("Invalid intensity")


def click_with_retries(dr, xpath_click, xpath_confirmation):
    tries = 0
    while tries < MAX_RETRIES:
        element_to_click = dr.find_element_by_xpath(xpath_click)
        element_to_click.click()
        tries = tries + 1
        if wait_element_by_xpath(dr, xpath_confirmation, False, SECS_TO_RE_CLICK):
            return
        else:
            logging.info(f"Retrying click for xpath {xpath_click}. Try {tries} out of {MAX_RETRIES}")
    logging.error(f"Element with xpath {xpath_confirmation} not found after {tries} clicks to {xpath_click}")
    raise TimeoutError()


def wait_element_by_xpath(dr, xpath, error_on_timeout=True, wait_time=TIMEOUT, return_all=False):
    secs_passed = 0
    while secs_passed < wait_time:
        elements_found = dr.find_elements_by_xpath(xpath)
        if len(elements_found) > 0:
            logging.debug(f"########### element found {xpath}")
            if return_all:
                return elements_found
            else:
                return elements_found[0]
        time.sleep(PING)
        secs_passed += PING
    if error_on_timeout:
        logging.error(f"Element with xpath {xpath} not found after {wait_time} seconds")
        raise TimeoutError()
    else:
        return False


def wait_element_disappear_by_xpath(dr, xpath, error_on_timeout=True, wait_time=TIMEOUT):
    secs_passed = 0
    while secs_passed < wait_time:
        elements_found = dr.find_elements_by_xpath(xpath)
        if len(elements_found) == 0:
            logging.debug(f"########### element disappeared {xpath}")
            return True
        time.sleep(PING)
        secs_passed += PING
    if error_on_timeout:
        logging.error(f"Element with xpath {xpath} STILL found after {wait_time} seconds")
        raise TimeoutError()
    else:
        return False


def wait_any_element_to_have_text(dr, xpath, text):
    secs_passed = 0
    while secs_passed < TIMEOUT:
        elements_found = dr.find_elements_by_xpath(xpath)
        for element in elements_found:
            if element.text == text:
                return element
        time.sleep(PING)
        secs_passed += PING
    logging.error(f"Element with xpath {xpath} and text {text} not found after {TIMEOUT} seconds")
    raise TimeoutError()


def check_two_outputs(dr, xpath1, xpath2):
    """
    Check two possible outcomes given two xpaths
    :param dr: reference to the driver
    :param xpath1: global xpath identifier for path 1
    :param xpath2: global xpath identifier for path 2
    :return: A tuple (first_path, elements) where the first is a boolean indicating that the first path was found
    """
    secs_passed = 0
    while secs_passed < TIMEOUT:
        elements1_found = dr.find_elements_by_xpath(xpath1)
        elements2_found = dr.find_elements_by_xpath(xpath2)
        if len(elements1_found) > 0:
            return True, elements1_found
        if len(elements2_found) > 0:
            return False, elements2_found
        time.sleep(PING)
        secs_passed += PING
    logging.error(f"The element with xpath {xpath1} nor the {xpath2} were found after {TIMEOUT} seconds")
    raise TimeoutError()


def get_driver() -> webdriver:
    opts = webdriver.ChromeOptions()
    opts.add_extension(METAMASK_PATH)
    for argument in chrome_arguments:
        opts.add_argument(argument)
    driver_ = webdriver.Chrome(DRIVER_PATH,
                               chrome_options=opts)
    return driver_


def wait_for_popup(dr, handles_before, error_on_timeout=True, wait_time=TIMEOUT, xpath_no_popup=None):
    new_handles = handles_before
    count = 0
    while len(handles_before) == len(new_handles) and count < wait_time:
        new_handles = dr.window_handles
        if xpath_no_popup:
            if dr.find_elements_by_xpath(xpath_no_popup):
                # Xpath that confirms that there was not any popup
                return False
        time.sleep(PING)
        count += PING

    if count >= wait_time:
        if error_on_timeout:
            logging.error(f"The popup did not appear after {wait_time} seconds")
            raise TimeoutError()
        else:
            return False

    for handle in dr.window_handles:
        if handle not in handles_before:
            return handle


def closing_routine(dr):
    logging.info(f"Waiting {SECS_BEFORE_CLOSING} secs before closing...")
    time.sleep(SECS_BEFORE_CLOSING)
    dr.close()
    dr.quit()
    logging.info("Driver closed successfully")
