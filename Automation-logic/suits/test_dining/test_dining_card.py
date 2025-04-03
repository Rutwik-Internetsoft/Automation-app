from logic.login_logic import Login  
from logic.dining_logic import Dining 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from logic.locators import Locators
import pytest

class TestCashLog:
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        """Automatically inject the appium_driver fixture for every test."""
        self.driver = appium_driver
        self.dining = Dining(self.driver)
        self.locators = Locators()
        self.locators.calculations_locators()
        self.locators.common_locators()
        self.locators.dining()
        self.wait = WebDriverWait(self.driver,5)

        
    # def test_printer(self):
    #     self.dining.connecting_printer()
    
    # def test_dine_in(self):
    #     assert self.dining.dine_in(1,1) == True
    # def test_adding_items_to_whole_and_individuals(self):
    #     assert self.dining.adding_items_dine_in() == True
        
    # def test_adding_new_guests(self):    
    #     assert self.dining.add_guests() == True
        
    # def test_firing_items(self):
    #     assert self.dining.firing_items() == True
        
    # def test_updating_order(self):    
    #     assert self.dining.update_order() == True
        
    # def test_adding_items_to_waste(self):
    #     assert self.dining.wastage() == True
        
    # def test_removing_guests(self):    
    #     assert self.dining.remove_guests() == True
        
    # def test_individual_payment(self):
    #     assert self.dining.paying_individually() == True
        
        #=====================Merge Dining Test======================
        
    def test_dine_in_merge(self):
        assert self.dining.dine_in(1,1) == True
        
    def test_addming_items(self):    
        assert self.dining.adding_items_dine_in(1,"add_guests") == True
        
        self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
        
    def test_changing_dining_table_and_floor(self):    
        assert self.dining.dine_in(2,3) == True
        
    def test_adding_items_on_new_table(self):
        assert self.dining.adding_items_dine_in(1,"don't_add_guests") == True
        self.wait.until(EC.presence_of_element_located(self.locators.floor_plan)).click()
        
    def test_merging_both_tables(self):
        assert self.dining.merge_tables() == True
        
    def test_merge_of_tables(self):    
        assert self.dining.dine_in(1,1) == True
    
    def test_adding_guests(self):
        assert self.dining.add_guests() == True
        
    def test_firing_items_on_merged_table(self):
        assert self.dining.firing_items() == True
        
    def test_updating_order_for_merged_table(self):
        assert self.dining.update_order(2) == True
        
    def test_is_items_can_be_added_to_waste(self):
        assert self.dining.wastage() == True
        
    def test_removing_guests(self):
        assert self.dining.remove_guests() == True
        
    def test_individual_payments(self):
        assert self.dining.paying_individually("cash") == True
        