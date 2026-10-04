"""Central test-run configuration, with environment variable overrides."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    """Settings that keep the test suite portable between local and CI runs."""

    browser: str = os.getenv("BROWSER", "chrome").lower()
    headless: bool = _as_bool(os.getenv("HEADLESS", "true"))
    # Empty means "serve the login flow locally", which is the default the suite
    # runs on - the-internet.herokuapp.com is free-tier infra with no uptime
    # guarantee. Set THE_INTERNET_URL to aim the same tests at the real site.
    the_internet_url: str = os.getenv("THE_INTERNET_URL", "")
    sauce_demo_url: str = os.getenv("SAUCE_DEMO_URL", "https://www.saucedemo.com")
    # Empty means "serve the form locally", which is the default the suite runs on.
    # Set FORM_TEST_URL to aim the same test at a hosted page.
    form_test_url: str = os.getenv("FORM_TEST_URL", "")
    timeout_seconds: int = int(os.getenv("UI_TIMEOUT_SECONDS", "10"))
    # Separate from timeout_seconds on purpose: the-internet.herokuapp.com runs on
    # a free-tier dyno that sleeps when idle, and the request that wakes it can
    # take well past 10s. This covers that cold start without slowing down every
    # explicit element wait in the suite.
    page_load_timeout_seconds: int = int(os.getenv("PAGE_LOAD_TIMEOUT_SECONDS", "30"))


settings = Settings()
