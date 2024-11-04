from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.config.logger import logger

TIMEOUT = 15
PF = 1

def is_element_visible(driver, by, locator):
    try:
        element = driver.find_element(by, locator)
        return element.is_displayed()
    except NoSuchElementException:
        return False


def wait_for_element(driver, by, locator, timeout=TIMEOUT):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )
        return element
    except (NoSuchElementException, TimeoutException):
        logger.info(f"Element not found: {locator}")
        return None

def get_element_text(driver, by, locator, timeout=TIMEOUT):
    element = wait_for_element(driver, by, locator, timeout)
    if element:
        return element.text
    return None

def wait_for_element_to_disappear(driver, by, locator, timeout=TIMEOUT):
    try:
        WebDriverWait(driver, timeout).until_not(
                EC.visibility_of_element_located((by, locator))
        )
    except TimeoutException:
        logger.info(f"Element still visible: {locator}")

def wait_for_dialog(driver, timeout=TIMEOUT):
    try:
        WebDriverWait(driver, timeout, poll_frequency=PF).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]'))
        )
    except TimeoutException:
        logger.info("Dialog element with role 'dialog' not found within the given timeout")


def wait_for_partial_page_url(driver, partial_url, timeout=TIMEOUT):
    try:
        WebDriverWait(driver, timeout, poll_frequency=PF).until(
            EC.url_contains(partial_url)
        )
        return True
    except TimeoutException:
        logger.info(f"Partial page URL '{partial_url}' not found within the given timeout")
        return False

def wait_for_page_title(driver, title, timeout=TIMEOUT):
    try:
        WebDriverWait(driver, timeout, poll_frequency=PF).until(
            EC.title_is(title)
        )
    except TimeoutException:
        logger.info(f"Page title '{title}' not found within the given timeout")
        
def get_page_title(driver):
    # Usage:
    #     when you first log in to instagram: page title is: Instagram: Instagram.com
    #     navigate to inbox: Inbox · Direct
    #     click user: Instagram · Direct
    return driver.title

def get_element_attribute(driver, by, locator, attribute, description=None, timeout=TIMEOUT):
    element = find(driver, by, locator, description, timeout)
    if element:
        return element.get_attribute(attribute)
    return None

def find(driver, by, locator, description=None, timeout=TIMEOUT):
    try:
        element = WebDriverWait(driver, timeout, poll_frequency=PF).until(
            EC.element_to_be_clickable((by, locator))
        )
        return element
    except (NoSuchElementException, TimeoutException):
        if description is not None:
            error_message = f"Error finding: {description}"
        else:
            error_message = f"Error finding: {locator}"
        logger.info(error_message, exc_info=True)
        return None


def by_xpath(driver, locator, description=None, timeout=TIMEOUT):
    return find(driver, By.XPATH, locator, description, timeout)


def by_id(driver, locator, description=None, timeout=TIMEOUT):
    return find(driver, By.ID, locator, description, timeout)


def by_class(driver, locator, description=None, timeout=TIMEOUT):
    return find(driver, By.CLASS_NAME, locator, description, timeout)


def by_tag(driver, locator, description=None, timeout=TIMEOUT):
    return find(driver, By.TAG_NAME, locator, description, timeout)


def by_text(driver, locator, description=None, timeout=TIMEOUT):
    return find(driver, By.LINK_TEXT, locator, description, timeout)


def by_css(driver, locator, description=None, timeout=TIMEOUT):
    return find(driver, By.CSS_SELECTOR, locator, description, timeout)

def automate_click_and_enter(driver, path):
    # Locate the element you want to click and send "Enter" key to
    target_element = by_xpath(driver, path)

    # Create an ActionChains object
    actions = ActionChains(driver)

    # Click the target element
    actions.click(target_element)

    # Press the "Enter" key
    actions.send_keys(Keys.ENTER)

    # Perform the actions
    actions.perform()