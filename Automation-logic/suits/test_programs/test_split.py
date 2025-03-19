import pytest
from logic.dependencies import Dependencies

class TestSplitProgram:
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        """Automatically inject the appium_driver fixture for every test."""
        self.driver = appium_driver
        self.deps = Dependencies(self.driver)
        self.calc = self.deps.get_calculations()
        self.split = self.deps.get_split_order()

    def test_split_cash(self):
        self.calc.add_multiple_items()
        assert self.split.price_checking_cash() == True
        assert self.split.splitting_cash() == True
        assert self.split.transaction_checking() == True
        
    def test_split_cash_with_tip(self):
        self.calc.add_multiple_items()
        assert self.split.price_checking_cash() == True
        assert self.split.splitting_cash() == True
        self.calc.transaction_tip(1)
        self.calc.transaction_tip(2)
    
    # def test_split_card(self):
    #     self.calc.connect_PAX()
    #     self.calc.add_multiple_items(3)
    #     assert self.split.price_checking_card() == True
    #     assert self.split.splitting_card() == True
    #     assert self.split.transaction_checking() == True

    # def test_split_gift_card(self):
    #     # self.split.add_multiple_items()
    #     self.split.gift_card_balance()
    #     assert self.split.price_checking_cash()==True
    #     assert self.split.splitting_gift_card() == True