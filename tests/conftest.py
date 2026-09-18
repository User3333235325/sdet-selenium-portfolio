"""Pytest fixtures for browser lifecycle and useful failure artifacts."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from src.config.settings import settings

ARTIFACTS_DIRECTORY = Path("artifacts")

# Ad and analytics frames are the usual cause of ElementClickInterceptedException
# on public practice sites: they load late, push the form down after the test has
# already scrolled, and sometimes float a sticky banner over the submit button.
# Blocking them is a test-environment decision, not a workaround in the test code.
BLOCKED_THIRD_PARTY_URLS = [
    "*googlesyndication.com*",
    "*doubleclick.net*",
    "*googletagservices.com*",
    "*googletagmanager.com*",
    "*google-analytics.com*",
    "*adservice.google.*",
    "*adsystem.com*",
    "*carbonads.net*",
    "*ezoic.net*",
    "*ezodn.com*",
]


def _build_chrome_driver() -> WebDriver:
    if settings.browser != "chrome":
        raise pytest.UsageError(
            f"Unsupported browser: {settings.browser}. This project currently supports chrome."
        )

    options = Options()
    if settings.headless:
        options.add_argument("--headless=new")
    # A taller viewport keeps long forms in view and reduces scroll-then-click races.
    options.add_argument("--window-size=1440,1400")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(settings.timeout_seconds)
    driver.implicitly_wait(0)
    _block_third_party_requests(driver)
    return driver


def _block_third_party_requests(driver: WebDriver) -> None:
    """Drop ad and tracker requests so page layout stays stable during a run."""
    try:
        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd(
            "Network.setBlockedURLs", {"urls": BLOCKED_THIRD_PARTY_URLS}
        )
    except (WebDriverException, AttributeError):
        # Non-Chromium drivers have no CDP; the suite still runs without blocking.
        pass


@pytest.fixture
def driver(request: pytest.FixtureRequest) -> WebDriver:
    """Provide an isolated browser and save evidence whenever a test fails."""
    browser = _build_chrome_driver()
    yield browser

    report = getattr(request.node, "rep_call", None)
    if report and report.failed:
        _save_failure_artifacts(browser, request.node.name)
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    """Attach the call-phase result to the test so the fixture can inspect it."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        item.rep_call = report


def _save_failure_artifacts(browser: WebDriver, test_name: str) -> None:
    ARTIFACTS_DIRECTORY.mkdir(exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", test_name)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    artifact_base = ARTIFACTS_DIRECTORY / f"{safe_name}_{timestamp}"

    browser.save_screenshot(f"{artifact_base}.png")
    (artifact_base.with_suffix(".html")).write_text(
        browser.page_source, encoding="utf-8"
    )
