"""Form-submission coverage using a dedicated public practice page."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from src.config.settings import settings
from src.pages.html_form_page import HtmlFormPage, HtmlFormResultsPage


@pytest.mark.smoke
@pytest.mark.regression
def test_user_can_submit_a_completed_html_form(driver: WebDriver) -> None:
    username = "portfolio-tester"
    comment = "Automated form submission"
    form_page = HtmlFormPage(driver)
    form_page.load(settings.form_test_url)

    form_page.submit(
        username=username,
        password="not-a-secret",
        comments=comment,
    )

    results_page = HtmlFormResultsPage(driver)
    assert "You submitted the form." in results_page.submission_message
    assert username in results_page.submitted_values
    assert comment in results_page.submitted_values
