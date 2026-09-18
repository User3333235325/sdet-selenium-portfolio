"""Cart page object for Sauce Demo."""

from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage, Locator


class CartPage(BasePage):
    CART_ITEM_NAMES: Locator = (By.CSS_SELECTOR, ".inventory_item_name")

    @property
    def item_names(self) -> list[str]:
        return [item.text.strip() for item in self.driver.find_elements(*self.CART_ITEM_NAMES)]
