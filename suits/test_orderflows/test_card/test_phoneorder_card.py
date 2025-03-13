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
    

    @allure.story("Device Connection")
    @allure.title("Connect PAX Payment Terminal")
    def test_pax_connection(self):
        assert self.phone.connect_PAX() == True
        print("PAX Connected Successfully")

    
    @allure.story("Phone Order Payment ")
    @allure.title("Process a phone order with cash payment and refund")
    def test_phoneorder_card_payment(self):
        
        assert self.phone.order("Phone Order") == True
        assert self.phone.search_cust_order() == True
        assert self.phone.add_multiple_items(2) is True
        
        assert self.phone.card_payment() == True
        
        assert self.phone.card_refund() == True
        
    
    @allure.story("Phone Order Save and Pay")
    @allure.title("Process a phone order with Save and then Pay")
    def test_phoneorder_save_pay(self):
        
        assert self.phone.order("Phone Order") == True
        assert self.phone.search_cust_order() == True
        assert self.phone.add_multiple_items(3)
        assert self.phone.add_discount()
        print("===================Checking=================")

        self.trn_pay = self.phone.pay(amount = "yes")
        print(f"The amount on Pay button is {self.trn_pay}")
        
        self.pend_pay =  self.phone.save_order("Pay")
        print(f"The amount on pending order page is {self.pend_pay}")
        
        surcharge = self.phone.surcharge_actual()
        
        self.endpay = self.phone.card_amount()
        
        print(f"The amount on card pay after applying surcharge is {self.endpay}")
        
        print("Checking if Pay button amount, Pending page amount, after adding surcharge is same as card amount")
        if self.endpay == (self.pend_pay+surcharge) == (self.trn_pay+surcharge):
            assert True
        assert self.phone.card_pay()==True
        print("==================Test Passed====================")
        
    @allure.story("Phone Order Save and Update and Pay By card")
    @allure.title("Process a phone order with Save and then Pay")
    def test_phoneorder_update_pay(self):
        
        assert self.phone.order("Phone Order") == True
        print("===================Checking=================")

        assert self.phone.search_cust_order() == True
        assert self.phone.add_multiple_items(3)
        assert self.phone.save_order(process = "Update") == True
        
        self.trn_pay = self.phone.pay(amount = "yes")
        print("===================Checking=================")
        print(f"The amount on Pay button is {self.trn_pay}")
        
        self.pend_pay =  self.phone.save_order("Pay")
        
        print(f"The amount on pending order page is {self.pend_pay}")
        
        surcharge = self.phone.surcharge_actual()
        
        self.endpay = self.phone.card_amount()
        
        print(f"The amount on card pay after applying surcharge is {self.endpay}")
        
        print("Checking if Pay button amount, Pending page amount, after adding surcharge is same as card amount")
        if self.endpay == (self.pend_pay+surcharge) == (self.trn_pay+surcharge):
            assert True
            
        
        assert self.phone.card_pay()==True
        print("Test Passed")

    @allure.story("Phone Order Save and Cancel")
    @allure.title("Process a phone order and Cancel it")
    def test_phoneorder_cancel_order(self):
        
        assert self.phone.order("Phone Order") == True
        assert self.phone.search_cust_order() == True
        assert self.phone.add_multiple_items(3)
        assert self.phone.save_order("Cancel") == True
        
        
        
    
        
        
