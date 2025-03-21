import pytest
import allure
from logic.dependencies import Dependencies

class TestDemo:
    
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        """Automatically inject the appium_driver fixture for every test."""
        self.driver = appium_driver
        self.deps = Dependencies(self.driver)
        self.calc = self.deps.get_calculations()
        
    # @allure.story("Device Connection")
    # @allure.title("Connect PAX Payment Terminal")
    # def test_pax_connection(self):
    #     with allure.step("Connecting to PAX Terminal"):
    #         assert self.calc.connect_PAX() == True
    #     allure.attach("PAX Connected Successfully", name="Connection Log")

    @allure.story("Order Management")
    @allure.title("Select Open Order")
    def test_openorder_btn(self):
        with allure.step("Selecting Open Order"):
            assert self.calc.order("Open Order") == True
            
    @allure.story("Order Management")
    @allure.title("Add multiple items to the cart")
    def test_adding_items(self):
        with allure.step("Adding multiple items"):
            assert self.calc.add_multiple_items(3) == True
 
    @allure.story("Manual Item Management")
    @allure.title("Add a Manual Item and Set Quantity")
    @allure.description("Tests if a manual item can be added with a specified quantity.")
    def test_manual_item_and_qty(self):
        with allure.step("Adding a manual item"):
            assert self.calc.manual_item() == True
    
    @allure.story("Item Quantity Update")
    @allure.title("Update Item Quantity")
    @allure.description("Ensures that the quantity of an existing item can be updated.")
    def test_updating_item(self):
        with allure.step("Updating item quantity"):
            assert self.calc.update_item_quantity() == True

    def test_remove_itm(self):
        assert self.calc.remove_item() is True
    
    def test_up(self):
        assert self.calc.save_order(process = "Update") == True
        
        
