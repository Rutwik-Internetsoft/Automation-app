import pytest
from PAT import PAT
class TestPAT:
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        self.driver = appium_driver
        self.pat = PAT(self.driver)

    def test_login(self):
        assert self.pat.login_logic() is True
    def test_passcode(self):
        assert self.pat.passcode() is True
    def test_add_table(self):
        assert self.pat.add_table() is True
    def test_add_multiple_items(self):
        assert self.pat.add_multiple_items(1) is True