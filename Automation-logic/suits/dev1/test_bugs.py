import pytest
import allure
from logic.dependencies import Dependencies

total = None
tolerance = None
surcharge = None

@allure.feature("Developer 1 Report")
class TestTakeOutFlow:
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        """Automatically inject the appium_driver fixture for every test."""
        self.driver = appium_driver
        self.deps = Dependencies(self.driver)
        self.calc = self.deps.get_calculations()
        

    @allure.story("Device Connection")
    @allure.title("Connect PAX Payment Terminal")
    def test_BUG101(self):
        assert self.calc.connect_PAX() == True
        print("PAX Connected Successfully")
        
    @allure.story("Order Management")
    @allure.title("Select Takeout Order")
    def test_BUG102(self):
        assert self.calc.order("Take Out") == True
        print("Take out button clicked")

    @allure.story("Order Management")
    @allure.title("Add multiple items to the cart")
    def test_BUG103(self):
        assert self.calc.add_multiple_items(3) == True
        print("Added Items Successfully")
