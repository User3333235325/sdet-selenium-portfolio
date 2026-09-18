"""Inventory page object for adding Sauce Demo products to a cart."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage, Locator
from src.pages.cart_page import CartPage


class InventoryPage(BasePage):
    TITLE: Locator = (By.CSS_SELECTOR, "[data-test='title']")
    CART_LINK: Locator = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CART_BADGE: Locator = (By.CSS_SELECTOR, ".shopping_cart_badge")

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
        self.click(self.CART_LINK)
        return CartPage(self.driver).wait_until_loaded()
