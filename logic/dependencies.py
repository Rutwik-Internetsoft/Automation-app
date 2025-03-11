from logic.takeout_logic import Calculations 
from logic.login_logic import Login
from logic.locators import Locators
from logic.dining_logic import Dining
from logic.split_logic import Split_cash
from logic.cash_log_logic import Cash_log
class Dependencies:

    def __init__(self, driver):
        self.driver = driver
        self.locators = Locators()
        self._calc = None
        self._phone = None
        self._login = None
        self._dining = None
        self._split  = None
        self._loyality = None
        self._cashlog = None
    
    def get_login(self):
        if self._login is None:
            self._login = Login(self.driver)
        return self._login

    def get_calculations(self):
        if self._calc is None:
            self._calc = Calculations(self.driver)
        return self._calc

    
    def get_dining_order(self):
        if self._dining is None:
            self._dining = Dining(self.driver)
        return self._dining
    
    def get_split_order(self):
        if self._split is None:
            self._split = Split_cash(self.driver)
        return self._split

    def get_loyality(self):  # Fix indentation
        if self._loyality is None:
            from logic.loyality_program_logic import Loyality  # Lazy import to avoid circular import
            self._loyality = Loyality(self.driver)
        return self._loyality
    
    def get_cash_log(self):
        if self._cashlog is None:
            self._cashlog = Cash_log(self.driver)
        return self._cashlog

