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
        
