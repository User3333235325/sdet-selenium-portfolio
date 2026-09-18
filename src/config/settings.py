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
    the_internet_url: str = os.getenv(
        "THE_INTERNET_URL", "https://the-internet.herokuapp.com"
    )
    sauce_demo_url: str = os.getenv("SAUCE_DEMO_URL", "https://www.saucedemo.com")
    # Empty means "serve the form locally", which is the default the suite runs on.
    # Set FORM_TEST_URL to aim the same test at a hosted page.
    form_test_url: str = os.getenv("FORM_TEST_URL", "")
    timeout_seconds: int = int(os.getenv("UI_TIMEOUT_SECONDS", "10"))


settings = Settings()
