"""Shopping-cart coverage for Sauce Demo."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from src.config.settings import settings
from src.pages.cart_page import CartPage
from src.pages.inventory_page import InventoryPage
from src.pages.sauce_login_page import SauceLoginPage


@pytest.mark.smoke
@pytest.mark.regression
def test_shopper_can_add_a_product_to_the_cart(driver: WebDriver) -> None:
    product_name = "Sauce Labs Backpack"
    login_page = SauceLoginPage(driver)
    login_page.load(settings.sauce_demo_url)
    login_page.login(username="standard_user", password="secret_sauce")

    inventory = InventoryPage(driver)
    assert inventory.title == "Products"
    inventory.add_item_named(product_name)
    inventory.open_cart()

    cart = CartPage(driver)
    assert cart.item_names == [product_name]
