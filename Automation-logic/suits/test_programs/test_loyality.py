import pytest
from logic.dependencies import Dependencies

class TestLoyalityProgram:
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        self.driver = appium_driver
        self.deps = Dependencies(self.driver)

    def test_login(appium_driver):
        """
        Perform login once before all tests and share the session.
        This runs before any test case in the session.
        """
        deps = Dependencies(appium_driver)
        testLogin = deps.get_login()
        assert testLogin.login() is True, "Login failed."
        
        assert testLogin.passcode() is True, "Passcode entry failed."

    # def test_loyality(self):
    #     self.deps.get_calculations().add_multiple_items(3)
    #     self.deps.get_loyality().using_loyality_points()
    #     assert self.deps.get_calculations().tear_down() == True
    
