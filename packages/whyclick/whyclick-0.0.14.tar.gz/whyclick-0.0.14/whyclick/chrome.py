# -*- coding: utf-8 -*-

import sys
import warnings
import time

from tqdm import tqdm
from bs4 import BeautifulSoup

import pyderman

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver import DesiredCapabilities


class ChromeBrowser:
    """Wrapper object to selenium WebDriver."""
    def __init__(self, headless=True, no_image=False, keep_log=True,
                 allow_non_w3c=True, version="latest"):
        self.headless = headless
        self.no_image = no_image
        self.keep_log = keep_log
        self.allow_non_w3c = allow_non_w3c
        self.version = version
        # Open the web-browser.
        self.driver = self.open_chrome(self.headless, self.no_image,
            self.keep_log, self.allow_non_w3c, self.version)

    def page_source(self):
        return self.driver.page_source

    def soupify(self, *args, **kwargs):
        return BeautifulSoup(self.driver.page_source, *args, **kwargs)

    @staticmethod
    def open_chrome(headless=True, no_image=False, keep_log=True,
                    allow_non_w3c=True, version="latest"):
        path = pyderman.install(browser=pyderman.chrome, version=version)
        options = Options()
        options.add_argument("--enable-javascript")
        options.headless = headless

        # Capabilities to keep logs.
        capabilities = DesiredCapabilities.CHROME

        if keep_log:
            capabilities["loggingPrefs"] = {"performance": "ALL"}  # newer: goog:loggingPrefs

        # Allow non W3C standard command, see https://stackoverflow.com/q/56111529/610569
        if allow_non_w3c:
            options.add_experimental_option('w3c', False)

        if no_image:
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(path, options=options,
            desired_capabilities=capabilities)

        # Sanity checks.
        driver.get("http://www.python.org")
        assert "Python" in driver.title

        return driver

    def scroll_height(self):
        return self.browser.driver.execute_script("return document.body.scrollHeight")

    def infinite_scroll(self, factor=1.2, pause=1):
        # Get scroll height
        last_height = self.scroll_height()

        while True:
            # Scroll down to bottom.
            self.browser.driver.execute_script(
                f"window.scrollTo(0, document.body.scrollHeight / {factor});"
                )
            # Pause to let content load.
            time.sleep(pause)
            # Check whether it's end of page.
            this_height = self.scroll_height()
            if last_height == this_height:
                break
            last_height = this_height


def open_chrome(*args, **kwargs):
    return Chromebrowser.open_chrome(*args, **kwargs)


def remove_popups(driver, url, pop_name):
    driver.get(url)
    # Remove all pop-up nonsense...
    element = driver.find_element_by_class_name(pop_name)
    driver.execute_script("""
    var element = arguments[0];
    element.parentNode.removeChild(element);
    """, element)
    driver.get(url)
    return driver
