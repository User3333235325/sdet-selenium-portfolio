"""Secure-area page object for The Internet practice application."""

from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage, Locator


class SecureAreaPage(BasePage):
    HEADING: Locator = (By.CSS_SELECTOR, ".example h2")
    FLASH_MESSAGE: Locator = (By.ID, "flash")

    @property
    def heading(self) -> str:
        return self.text_of(self.HEADING)

    @property
    def notification(self) -> str:
        return self.text_of(self.FLASH_MESSAGE)
