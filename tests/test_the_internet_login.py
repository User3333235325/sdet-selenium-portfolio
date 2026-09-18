"""Authentication coverage for The Internet practice site."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from src.config.settings import settings
from src.pages.secure_area_page import SecureAreaPage
from src.pages.the_internet_login_page import TheInternetLoginPage


@pytest.mark.smoke
@pytest.mark.regression
def test_registered_user_can_log_in(driver: WebDriver) -> None:
    login_page = TheInternetLoginPage(driver)
    login_page.load(settings.the_internet_url)

    login_page.login(username="tomsmith", password="SuperSecretPassword!")
    secure_area = SecureAreaPage(driver)

    assert secure_area.heading == "Secure Area"
    assert "You logged into a secure area!" in secure_area.notification


@pytest.mark.regression
def test_invalid_credentials_show_a_helpful_message(driver: WebDriver) -> None:
    login_page = TheInternetLoginPage(driver)
    login_page.load(settings.the_internet_url)

    login_page.login(username="not-a-real-user", password="incorrect-password")

    assert "Your username is invalid!" in login_page.notification
