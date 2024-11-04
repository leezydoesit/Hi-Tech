import sys

from selenium.common import ElementClickInterceptedException

from src.bot.functions import *
from src.config.config import Config
from src.config.logger import logger
from src.bot.utils import slow_type, wait_a_bit_sir
from src.bot.webdriver import StealthDriver
from src.data import account_manager
from src.data.data_models import Account
from src.ui.viewer import ask_for_2fa, show_popup


class IgBot:
    def __init__(self, auto_data):
        self.config = Config()
        self.username = auto_data.credentials.username
        self.password = auto_data.credentials.password
        self.session = auto_data.credentials.session # cookies
        self.message_obj = auto_data.message_obj # {name}, long time no see!
        self.check_for_prior = auto_data.check_messaged_before # boolean flag
        self.headless = auto_data.headless
        self.browser = StealthDriver(self.headless)
        self.broken_addressees = []
        self.messaged_before = []
        self.messaged_users = []
        logger.debug("IgBot init")

    ###################################### Credential Functions ######################################
    def get_credentials(self):
        """
        Get the credentials for the Instagram account.
            Returns:
                dict: A dictionary containing the username, password, and session.
        """
        logger.debug("Getting credentials")
        return {
            'username': self.username,
            'password': self.password,
            'session': self.session
        }

    def save_credentials(self):
        """
            Save the credentials to a JSON file.
        """
        logger.debug("Saving credentials")
        try:
            account_manager.save_or_update_account(Account(**self.get_credentials()))
        except Exception as e:
            logger.error(f"can't save credentials: {e}")
    
    def save_cookies(self):
        logger.debug("Saving credentials")
        try:
            if self.session is None:
                self.session = self.browser.driver.get_cookies()
        except Exception as e:
            logger.error(f"can't save cookies: {e}")

    ###################################### Browser/Cookie Functions ######################################

    def get(self, url):
        """
        Open the specified URL in the browser.
        :arg: url (str): The URL to open.
        """
        logger.debug(f"Opening {url}")
        self.browser.driver.get(url)

    def close_browser(self):
        """
        Close the browser and save the credentials.
        """
        logger.debug("Closing browser")
        self.browser.driver.quit()
        sys.exit()

    def load_cookies(self):
        """
        Load the cookies into the browser.
        """
        logger.debug("Loading cookies")
        try:
            for cookie in self.session:
                print(cookie)
                try:
                    self.browser.driver.add_cookie(cookie)
                except Exception as e:
                    logger.error(f"can't load cookies: {e}")
        except TypeError:
            return False

    def check_cookie_presence(self):
        """
        Check if there are any cookies present in the browser.
            :return: bool: True if cookies are present, False otherwise.
            :arg: self
        """
        cookies = self.browser.driver.get_cookies()
        return bool(cookies)

    ###################################### Popup Dismissal Functions ######################################
    def dismiss_cookie_notice(self):
        """
        Dismiss the cookie notice by clicking the corresponding button.
        """
        logger.debug("Dismissing cookie notice")
        dismiss_cookies = by_xpath(self.browser.driver,
                                   "//button[contains(text(), 'Only allow essential cookies') or contains(text(), "
                                   "'Decline')]",
                                   "decline cookies")
        if dismiss_cookies:
            dismiss_cookies.click()

    def two_fa_pass(self):
        """
        Handle the 2FA (Two-Factor Authentication) process if required.
        """
        logger.debug("Trying to enter 2FA")
        logger.info(get_page_title(self.browser.driver))
        
        two_fa_needed = wait_for_partial_page_url(self.browser.driver,
                                                  'two_factor?next=%2F')
        
        if two_fa_needed:
            two_fa_field = by_css(self.browser.driver, "input[name='verificationCode']")
            if two_fa_field:
                logger.debug("Asking user for 2FA")
                two_fa_code = ask_for_2fa()
                if two_fa_code:
                    slow_type(two_fa_code, two_fa_field)
                    by_xpath(self.browser.driver, "//button[@type='button']").click()
        else:
            logger.debug("no 2fa needed")

    def enable_save_login(self):
        """
        Enable the option to save login information if prompted.
        """
        logger.debug("Enabling Save Login")
        wait_a_bit_sir()
        save_login_present = wait_for_partial_page_url(self.browser.driver, '/accounts/onetap/?next=%2F')
        
        if save_login_present:
            by_xpath(self.browser.driver, '//button[normalize-space()="Save Info"]').click()
            self.save_cookies()
        else:
            logger.info("No 'Save login' prompt, moving on")

    def disable_notifications(self):
        """
        Disable notifications if prompted.
        """
        logger.debug("Disabling Notifications")
        wait_a_bit_sir()
        # there might be a prompt to enable notifications, click on "not now"
        not_now_button = by_xpath(self.browser.driver, '//button[normalize-space()="Not Now"]')

        if not_now_button:
            not_now_button.click()
        else:
            logger.info("No notification dialog shown, moving on")

    ###################################### Navigation Functions ######################################
    def enter_credentials(self):
        """
        Enter the username and password in the login form.
        """
        logger.debug(f'Logging in as {self.username}, password: {self.password}')
        try:
            username_f = by_css(self.browser.driver, "input[name='username']")
            slow_type(self.username, username_f)
            logger.debug("Typed in Username")
        except NoSuchElementException as e:
            logger.error("Error finding Username Input: %s", e, exc_info=True)

        try:
            password_f = by_css(self.browser.driver, "input[name='password']")
            slow_type(self.password, password_f)
            logger.debug("Typed in Password")
        except NoSuchElementException as e:
            logger.error("Error finding Password Input: %s", e, exc_info=True)
    
    def submit_login_form(self):
        """
        Submit the login form.
        """
        try:
            submitBtn = by_xpath(self.browser.driver, "//button[@type='submit']").click()
            print(f"submitBtn: {submitBtn}")  # Add this line to print the value of submitBtn
            if submitBtn:
                logger.debug("LoginBtn Found")
                # Remove this line, as the button is already clicked in the by_xpath function
                # submitBtn.click()
            else:
                logger.error("Submit button not found.")
        except AttributeError as e:
            logger.error("Error clicking Submit Button: %s", e, exc_info=True)
        except Exception as e:
            logger.error("Unknown error occurred while submitting the login form: %s", e, exc_info=True)
    
    def goto_send(self):
        """
        Go to the send message page.
        """
        self.browser.driver.get('https://www.instagram.com/direct/inbox/')
    
    
    def select_addressee(self, addressee):
        logger.info(get_page_title(self.browser.driver))
        by_css(self.browser.driver, 'svg[aria-label="New message"]').click()
        
        placeholder_value = "Search..."
        user_search_f = by_css(self.browser.driver, 'input[placeholder="{}"]'.format(placeholder_value))
        logger.info("user search field")
        slow_type(addressee, user_search_f)
        try:
            try:
                logger.debug("Trying to click on span with addressee's account name")
                addressee_found = by_xpath(self.browser.driver, f'//span[text()="{addressee}"]')
                
                if addressee_found:
                    addressee_found.click()
                else:
                    raise NoSuchElementException
            
            except ElementClickInterceptedException:
                try:
                    logger.debug("Couldn't click on the span with the account name, trying a CSS selector")
                    css_container = by_css(self.browser.driver, 'div.x1i10hfl')
                    
                    if css_container:
                        css_container.click()
                    else:
                        raise NoSuchElementException
                except (ElementClickInterceptedException, NoSuchElementException):
                    logger.debug("Couldn't select the addressee, returning an error,")
                    raise NoSuchElementException
            logger.info("clicked user")
            by_xpath(self.browser.driver, '//div[text()="Chat"]').click()
            wait_for_partial_page_url(self.browser.driver, 'https://www.instagram.com/direct/t/')
            logger.info("clicked next")
        
        except (NoSuchElementException, TimeoutException):
            self.handle_addressee_error(addressee)

    def handle_addressee_error(self, addressee):
        placeholder_value = "Search..."
        user_search_f = by_css(self.browser.driver, 'input[placeholder="{}"]'.format(placeholder_value))
        user_search_f.send_keys(Keys.ESCAPE)
        logger.error(f"Error selecting addressee: {addressee}", exc_info=True)
        self.broken_addressees.append(addressee)
        logger.debug(f"Added {addressee} to Broken addressees")
    
    def any_prior_messages(self, addressee):
        logger.debug("Checking for prior messages")
        wait_a_bit_sir()
        prior_message = by_xpath(self.browser.driver,
                                 '//div[@class="x6prxxf x1fc57z9 x1yc453h x126k92a x14ctfv" and @dir="auto" and @role="none"]')
        
        if not prior_message:
            logger.info(f'no messages have been sent to {addressee} before')
            return False
        else:
            logger.info(f'{addressee} has been messaged before')
            self.messaged_before.append(addressee)
            return True

    def send_message(self, message):
        """
        Slow Type and Send Message to Addressee
        """
        logger.debug("Sending message")
        message_input = by_xpath(self.browser.driver,
                                 '//div[@class="x1n2onr6"]//div[@aria-label="Message" and @role="textbox" and @contenteditable="true"]')
        
        if message_input:
            slow_type(message, message_input)
            message_input.send_keys(Keys.ENTER)
            logger.info("Message Sent")
        else:
            logger.info("Message element not found")
    
    ###################################### Error Check Functions ######################################
    def error_check(self):
        login_err = by_id(self.browser.driver, "slfErrorAlert", "login error div")
        if login_err:
            self.login_error_search()

    def login_error_search(self):
        if by_xpath(self.browser.driver, "//*[contains(text(), 'Sorry, your password was incorrect.')]"):
            logger.error("Login Password Incorrect, please fix credentials and run again.")
            self.close_browser()
        elif by_xpath(self.browser.driver,
                      "//*[contains(text(), 'There was a problem logging you into Instagram.')]"):
            logger.error("Login Account Incorrect, please fix credentials and run again.")
            self.close_browser()
        elif by_xpath(self.browser.driver, "//*[contains(text(), 'feedback_required')]"):
            logger.critical("Account Blocked... Try Again Later.")

    def check_ban(self):
        if by_xpath(self.browser.driver, "//*[contains(text(), 'We suspended your account')]"):
            logger.critical("Account Suspended... Disagree with Decision is Recommended.")
            self.close_browser()

    ###################################### Flow Functions ######################################
    def start_session(self):
        """
        Start the session by loading cookies or performing login.
        """
        logger.debug("Starting session")
        self.get('https://instagram.com')
        self.load_cookies()
        self.get('https://instagram.com')

        if not self.check_cookie_presence():
            self.login()
        else:
            self.disable_notifications()
            logger.info("No cookies found - Resuming Session")

    def login(self):
        """
        Starts Login Process
        """
        logger.debug("Log in process beginning")
        self.dismiss_cookie_notice()
        self.enter_credentials()
        self.submit_login_form() # intermittent error
        self.error_check() # checks for error popups
        self.check_ban()
        self.two_fa_pass()
        if self.session is None:
            self.save_cookies()
            self.save_credentials()
        self.enable_save_login()
        self.disable_notifications()

    def run(self):
        """
        Run the automated outreach process.
        """
        self.start_session()  # Do we need to log in or not?
        wait_a_bit_sir()  # starts here
        self.goto_send()

        message_limit = 200
        message_count = 0

        for obj in self.message_obj:
            if message_count >= message_limit:
                logger.info(f"Message limit reached: {message_limit}")
                break

            recipient = obj.addressee
            msg = obj.text
            self.select_addressee(recipient)

            if recipient in self.broken_addressees:
                continue

            if self.check_for_prior and not self.any_prior_messages(recipient):
                self.messaged_users.append(recipient)
                self.send_message(msg)
                message_count += 1

            elif not self.check_for_prior:
                self.messaged_users.append(recipient)
                self.send_message(msg)
                message_count += 1

        # Display popup when message limit is reached or loop completes
        show_popup(self.broken_addressees, self.messaged_users, self.messaged_before)

