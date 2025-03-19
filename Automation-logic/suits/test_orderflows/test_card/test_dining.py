# from logic.login_logic import Login  
# from logic.dining_logic import Dining 
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from appium.webdriver.common.appiumby import AppiumBy
# from logic.locators import Locators
# import pytest

# class TestCashLog:
#     @pytest.fixture(autouse=True)
#     def setup_driver(self, appium_driver):
#         """Automatically inject the appium_driver fixture for every test."""
#         self.driver = appium_driver
#         self.dining = Dining(self.driver)
#         self.locators = Locators()
#         self.locators.calculations_locators()
#         self.locators.common_locators()
#         self.locators.dining()
#         self.wait = WebDriverWait(self.driver,5)

        
#     def test_printer(self):
#         self.dining.connecting_printer()
    
#     def test_dine_in(self):
#         assert self.dining.dine_in(1,1) == True
#         assert self.dining.adding_items_dine_in() == True
#         assert self.dining.add_guests() == True
#         assert self.dining.firing_items() == True
#         assert self.dining.update_order() == True
#         assert self.dining.wastage() == True
#         assert self.dining.remove_guests() == True
#         assert self.dining.paying_individually() == True
        
#     def test_dine_in_merge(self):
#         assert self.dining.dine_in(1,1) == True
#         assert self.dining.adding_items_dine_in(1,"add_guests") == True
#         self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
#         assert self.dining.dine_in(2,3) == True
#         assert self.dining.adding_items_dine_in(1,"don't_add_guests") == True
#         self.wait.until(EC.presence_of_element_located(self.locators.floor_plan)).click()
#         assert self.dining.merge_tables() == True
#         assert self.dining.dine_in(1,1) == True
#         assert self.dining.add_guests() == True
#         assert self.dining.firing_items() == True
#         assert self.dining.update_order() == True
#         assert self.dining.wastage() == True
#         assert self.dining.remove_guests() == True
#         assert self.dining.paying_individually("card") == True
        