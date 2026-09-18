"""Login page object for The Internet practice application."""

from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage, Locator


class TheInternetLoginPage(BasePage):
    PATH = "/login"
    USERNAME: Locator = (By.ID, "username")
    PASSWORD: Locator = (By.ID, "password")
    LOGIN_BUTTON: Locator = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH_MESSAGE: Locator = (By.ID, "flash")

    def load(self, base_url: str) -> "TheInternetLoginPage":
        self.open(f"{base_url}{self.PATH}")
        return self

    def login(self, username: str, password: str) -> None:
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    @property
    def notification(self) -> str:
        return self.text_of(self.FLASH_MESSAGE)
