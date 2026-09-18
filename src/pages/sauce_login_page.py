"""Login page object for Sauce Demo."""

from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage, Locator


class SauceLoginPage(BasePage):
    USERNAME: Locator = (By.ID, "user-name")
    PASSWORD: Locator = (By.ID, "password")
    LOGIN_BUTTON: Locator = (By.ID, "login-button")
    ERROR_MESSAGE: Locator = (By.CSS_SELECTOR, "[data-test='error']")

    def load(self, base_url: str) -> "SauceLoginPage":
        self.open(base_url)
        return self

    def login(self, username: str, password: str) -> None:
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    @property
    def error_message(self) -> str:
        return self.text_of(self.ERROR_MESSAGE)
