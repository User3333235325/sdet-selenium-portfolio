"""Secure-area page object for The Internet practice application."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage, Locator


class SecureAreaPage(BasePage):
    PATH_FRAGMENT = "/secure"
    HEADING: Locator = (By.CSS_SELECTOR, ".example h2")
    FLASH_MESSAGE: Locator = (By.ID, "flash")

    def wait_until_loaded(self) -> "SecureAreaPage":
        """Block until the browser is really on the secure-area document.

        The login page and the secure area share the same `.example h2`
        markup - only the text differs ("Login Page" vs "Secure Area"). Reading
        it right after the login click can grab the login page's own heading a
        moment before the post-login navigation lands, and that element goes
        stale the instant the browser catches up. Confirming the URL first
        removes the race, the same way CartPage confirms `cart.html` first.
        """
        self.wait_for_url_to_contain(self.PATH_FRAGMENT)
        return self

    @property
    def heading(self) -> str:
        self.wait_until_loaded()
        return self.text_of(self.HEADING)

    @property
    def notification(self) -> str:
        self.wait_until_loaded()
        return self.text_of(self.FLASH_MESSAGE)
