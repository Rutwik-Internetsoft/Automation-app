from logic.dependencies import Dependencies
import allure
import pytest

@allure.feature("Sanity Sheet")
class TestPhoneOrderCard:
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        """Automatically inject the appium_driver fixture for every test."""
        self.driver = appium_driver
        self.deps = Dependencies(self.driver)
        self.phone = self.deps.get_calculations()
    
    @allure.story("Phone Order Payment ")
    @allure.title("Process a phone order with cash payment and refund")
    def test_phoneorder_card_payment(self):
        
        assert self.phone.order("Phone Order") == True
        assert self.phone.phone_order() == True
        assert self.phone.add_multiple_items(2) is True
        assert self.phone.card_payment() == True
        self.phone.transaction()
        assert self.phone.card_refund() == True
        
    
    @allure.story("Phone Order Save and Pay")
    @allure.title("Process a phone order with Save and then Pay")
    def test_phoneorder_save_pay(self):
        
        assert self.phone.order("Phone Order") == True
        assert self.phone.phone_order() == True
        assert self.phone.add_multiple_items(3)
        assert self.phone.add_discount()
        self.trn_pay = self.phone.pay(amount = "yes")
        print(self.trn_pay)
        self.pend_pay =  self.phone.save_order("Pay")
        print(self.pend_pay)
        surcharge = self.phone.surcharge_actual()
        self.endpay = self.phone.card_amount()
        print(self.endpay)
        assert self.endpay == (self.pend_pay+surcharge) == (self.trn_pay+surcharge)
        assert self.phone.card_pay()==True

    @allure.story("Phone Order Save and Update and Pay By card")
    @allure.title("Process a phone order with Save and then Pay")
    def test_phoneorder_update_pay(self):
        
        assert self.phone.order("Phone Order") == True
        assert self.phone.phone_order() == True
        assert self.phone.add_multiple_items(3)
        assert self.phone.save_order(process = "Update") == True
        self.trn_pay = self.phone.pay(amount = "yes")
        print(self.trn_pay)
        self.pend_pay =  self.phone.save_order("Pay")
        print(self.pend_pay)
        surcharge = self.phone.surcharge_actual()
        self.endpay = self.phone.card_amount()
        print(self.endpay)
        assert self.endpay == (self.pend_pay+surcharge) == (self.trn_pay+surcharge)
        assert self.phone.card_pay()==True


    @allure.story("Phone Order Save and Cancel")
    @allure.title("Process a phone order and Cancel it")
    def test_phoneorder_cancel_order(self):
        
        assert self.phone.order("Phone Order") == True
        assert self.phone.phone_order() == True
        assert self.phone.add_multiple_items(3)
        assert self.phone.save_order("Cancel") == True
        
        
        
    
        
        
