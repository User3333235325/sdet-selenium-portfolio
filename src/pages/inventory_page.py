"""Inventory page object for adding Sauce Demo products to a cart."""

from __future__ import annotations

from typing import Optional

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage, Locator
from src.pages.cart_page import CartPage


class InventoryPage(BasePage):
    TITLE: Locator = (By.CSS_SELECTOR, "[data-test='title']")
    CART_LINK: Locator = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CART_BADGE: Locator = (By.CSS_SELECTOR, ".shopping_cart_badge")
    OPEN_CART_ATTEMPTS = 3

    @property
    def title(self) -> str:
        return self.text_of(self.TITLE)

    def add_item_named(self, item_name: str) -> None:
        item_button: Locator = (
            By.XPATH,
            "//div[contains(@class, 'inventory_item')][.//div[normalize-space()="
            f"'{item_name}'" "]]//button",
        )
        self.click(item_button)
        # The badge is the app confirming the add, so the next step cannot race it.
        self.find_visible(self.CART_BADGE)

    def open_cart(self) -> CartPage:
        """Open the cart, re-clicking if the router hasn't caught up yet.

        A successful click here doesn't guarantee the app's router has
        committed to `cart.html` before our wait budget runs out - on a
        loaded CI runner the click can register while the app is still
        mid-transition. Re-clicking is safe: it only happens while the URL
        still shows the inventory page, never once the cart has actually
        loaded, so it can't fire a second, unwanted navigation.
        """
        per_attempt_timeout = max(2, self.timeout // self.OPEN_CART_ATTEMPTS)
        last_error: Optional[TimeoutException] = None
        for _ in range(self.OPEN_CART_ATTEMPTS):
            if CartPage.PATH_FRAGMENT not in self.driver.current_url:
                self.click(self.CART_LINK)
            try:
                self.wait_for_url_to_contain(
                    CartPage.PATH_FRAGMENT, timeout=per_attempt_timeout
                )
                last_error = None
                break
            except TimeoutException as exc:
                last_error = exc
        if last_error is not None:
            raise last_error
        return CartPage(self.driver).wait_until_loaded()
