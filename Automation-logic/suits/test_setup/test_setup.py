import pytest
import allure
from logic.dependencies import Dependencies

total = None
tolerance = None
surcharge = None

@allure.feature("Setup Testflow")
class TestSetUpFlow:
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        self.driver = appium_driver
        self.deps = Dependencies(self.driver)
        self.setup = self.deps.get_setup()
        self.calc = self.deps.get_calculations()
        
    #======================= Setting up Environment =========================
    
    def test_setup(self):
        assert self.setup.setting_up() is True
        
    #======================= Editing Tax, Discount, Order Note =====================
        
    def test_tax(self):
        assert self.setup.tax_editing() is True
        
    def test_tip(self):
        assert self.setup.tip_editing() is True
        
    def test_discount(self):
        assert self.setup.discount_editing() is True
        
    def test_ordernote(self):
        assert self.setup.order_note_editing() is True
        
    #======================== Adding items ============================
        
    def test_setupcheck(self):
        assert self.setup.setup_check() is True
    
    #========================= Checking if Tax, Discount, Order Note has added successfully============================
    
    def test_discount_check(self):
        assert self.setup.check_discount() is True
        
    def test_order_note_check(self):
        assert self.setup.check_note() is True
        
    def test_check_tax_added(self):
        assert self.setup.check_tax() is True
        
    def test_cart_calculations(self):
        total = self.calc.total_calculation()
        endpay = self.calc.pay()
        assert abs(total - endpay) <= 0.3, f"Total ({total}) and Pay ({endpay}) difference exceeded limit!"
    
    def test_final_tax_check(self):
        assert self.setup.check_tax() is True
    
    def test_tip_check(self):
        assert self.setup.check_tip() is True
        
    def test_cash_pay(self):
        assert self.calc.cash_pay() is True
        
    def test_delete_tip(self):
        assert self.setup.remove_tip() is True
        
    def test_delete_ordernote(self):
        assert self.setup.remove_ordernote() is True
        
    def test_delete_discount(self):
        assert self.setup.remove_discount() is True
    
    def test_delete_taxes(self):
        assert self.setup.remove_tax() is True
        
    def test_removed_setup(self):
        assert self.setup.setup_check() is True
            
    def test_removed_discount_check(self):
        assert self.setup.check_discount(1) is True
    
    def test_removed_tax_check(self):
        assert self.setup.check_tax(1) is True
        
    def test_calculations(self):
        total = self.calc.total_calculation()
        endpay = self.calc.pay()
        assert abs(total - endpay) <= 0.3, f"Total ({total}) and Pay ({endpay}) difference exceeded limit!"
    
    def test_removed_tax_check(self):
        assert self.setup.check_tax(1) is True
    
    def test_removed_tip_check(self):
        assert self.setup.check_tip(1) is True
        
    def test_final_cashpay(self):
        assert self.calc.cash_pay() is True
        
        
    
        
        