import pytest
from logic.dependencies import Dependencies

class TestLoyalityProgram:
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        self.driver = appium_driver
        self.deps = Dependencies(self.driver)


    def test_adding_item(self):
        assert self.deps.get_calculations().add_multiple_items(3) is True
    
    def test_loyality(self):
        assert self.deps.get_loyality().using_loyality_points() is True
    
