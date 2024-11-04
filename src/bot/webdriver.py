from pathlib import Path
from src.config.config import config
from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class StealthDriver:
    """ Stealth selenium webdriver """

    def __init__(self, headless=False):
        self.opts = Options()
        self.opts.add_argument("--disable-blink-features=AutomationControlled")
        if headless:
            self.opts.add_argument("--headless")  # Add this line for headless mode
        self.opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.opts.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(options=self.opts)



        self.stealth_driver()

    def stealth_driver(self):
        stealth(driver=self.driver,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                            Chrome/83.0.4103.53 Safari/537.36",
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                run_on_insecure_origins=False
                )

        return self.driver


class WebDriver:
    """ Regular selenium webdriver """

    def __init__(self):
        self.opts = webdriver.FirefoxOptions()
        self.opts.add_argument("--width=600")
        self.opts.add_argument("--height=600")
        self.opts.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Firefox(options=self.opts)
