"""Shared Selenium interactions with explicit, readable waits."""

from __future__ import annotations

from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.ui import WebDriverWait

Locator = Tuple[str, str]


class BasePage:
    """Small foundation for page objects that avoids brittle fixed delays."""

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str) -> None:
        self.driver.get(url)

    def find_visible(self, locator: Locator) -> WebElement:
        return self.wait.until(conditions.visibility_of_element_located(locator))

    def click(self, locator: Locator) -> None:
        element = self.wait.until(conditions.element_to_be_clickable(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )
        element.click()

    def fill(self, locator: Locator, value: str) -> None:
        element = self.find_visible(locator)
        element.clear()
        element.send_keys(value)

    def text_of(self, locator: Locator) -> str:
        return self.find_visible(locator).text.strip()

    def is_visible(self, locator: Locator) -> bool:
        try:
            self.find_visible(locator)
        except Exception:
            return False
        return True

    def wait_for_url_to_contain(self, value: str) -> None:
        self.wait.until(conditions.url_contains(value))
