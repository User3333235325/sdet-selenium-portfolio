"""Cart page object for Sauce Demo."""

from __future__ import annotations

from typing import List

from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage, Locator


class CartPage(BasePage):
    PATH_FRAGMENT = "cart.html"
    CART_LIST: Locator = (By.CSS_SELECTOR, ".cart_list")
    CART_ITEM_NAMES: Locator = (By.CSS_SELECTOR, ".cart_list .inventory_item_name")

    def wait_until_loaded(self) -> "CartPage":
        """Block until the browser is really on the cart document.

        The inventory page uses the same .inventory_item_name nodes for all six
        products. Reading them before the cart navigation commits returns the
        whole catalogue instead of the cart contents, which is exactly the
        six-item list the assertion reported.
        """
        self.wait_for_url_to_contain(self.PATH_FRAGMENT)
        self.find_visible(self.CART_LIST)
        return self

    @property
    def item_names(self) -> List[str]:
        self.wait_until_loaded()
        return [item.text.strip() for item in self.find_all(self.CART_ITEM_NAMES)]
