"""Page objects for the HTML form and its submission results."""

from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage, Locator


class HtmlFormPage(BasePage):
    USERNAME: Locator = (By.NAME, "username")
    PASSWORD: Locator = (By.NAME, "password")
    COMMENTS: Locator = (By.NAME, "comments")
    SUBMIT_BUTTON: Locator = (By.CSS_SELECTOR, "input[type='submit'][value='submit']")

    def load(self, form_url: str) -> "HtmlFormPage":
        self.open(form_url)
        return self

    def submit(self, username: str, password: str, comments: str) -> None:
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.fill(self.COMMENTS, comments)
        self.click(self.SUBMIT_BUTTON)


class HtmlFormResultsPage(BasePage):
    SUBMISSION_MESSAGE: Locator = (
        By.XPATH,
        "//*[contains(normalize-space(), 'You submitted the form.')]",
    )
    PAGE_BODY: Locator = (By.TAG_NAME, "body")

    @property
    def submission_message(self) -> str:
        return self.text_of(self.SUBMISSION_MESSAGE)

    @property
    def submitted_values(self) -> str:
        return self.text_of(self.PAGE_BODY)
