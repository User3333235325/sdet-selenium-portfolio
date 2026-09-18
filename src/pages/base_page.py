"""Shared Selenium interactions with explicit, readable waits."""

from __future__ import annotations

from typing import Callable, List, Optional, Tuple

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.ui import WebDriverWait

from src.config.settings import settings

Locator = Tuple[str, str]

TRANSIENT_CLICK_ERRORS = (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)


class BasePage:
    """Small foundation for page objects that avoids brittle fixed delays."""

    def __init__(self, driver: WebDriver, timeout: Optional[int] = None) -> None:
        self.driver = driver
        self.timeout = settings.timeout_seconds if timeout is None else timeout
        self.wait = WebDriverWait(driver, self.timeout)

    def open(self, url: str) -> None:
        self.driver.get(url)

    def find_visible(self, locator: Locator) -> WebElement:
        return self.wait.until(conditions.visibility_of_element_located(locator))

    def find_all(self, locator: Locator) -> List[WebElement]:
        return self.driver.find_elements(*locator)

    def click(self, locator: Locator) -> None:
        """Click an element, retrying while something transient covers it.

        Public practice pages shift layout while banners and ad frames load, so a
        single scroll-then-click can aim at coordinates that are already stale by
        the time the command reaches the browser. Retrying inside the existing
        wait budget keeps the test honest - it still clicks the real element with
        a real click, it just refuses to give up on the first interception.
        """
        self.wait.until(
            self._clicked(locator),
            f"{locator} was still covered by another element after {self.timeout}s",
        )

    @staticmethod
    def _clicked(locator: Locator) -> Callable[[WebDriver], bool]:
        clickable = conditions.element_to_be_clickable(locator)

        def attempt(driver: WebDriver) -> bool:
            element = clickable(driver)
            if not element:
                return False
            try:
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                    element,
                )
                element.click()
            except TRANSIENT_CLICK_ERRORS:
                return False
            return True

        return attempt

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
        self.wait.until(
            conditions.url_contains(value),
            f"URL never contained {value!r} within {self.timeout}s "
            f"(current: {self.driver.current_url})",
        )
