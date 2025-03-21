from logic.takeout_logic import Calculations
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from logic.locators import Locators
from appium.webdriver.common.appiumby import AppiumBy

import random
class Setup:
    def __init__(self, appium_driver):
        self.driver = appium_driver
        
        self.short_wait = WebDriverWait(self.driver,5)
        self.wait = WebDriverWait(self.driver, 10)
        self.long_wait = WebDriverWait(self.driver,15)
        self.calc = Calculations(self.driver)
        self.locators = Locators()
        self.locators.calculations_locators()
        self.locators.common_locators()
        self.locators.set_up()
    def tax_editing(self):
        try:
            assert self.wait.until(EC.element_to_be_clickable(self.locators.main_menu_button)).click() is None,"Cannot press Menu Button"
            
            assert self.wait.until(EC.element_to_be_clickable(self.locators.setup_btn)).click() is None ,"Cannot press Setup Button"
            
            assert self.wait.until(EC.element_to_be_clickable(self.locators.tips_btn)).click() is None,"Tip Button Cannot be clicked"
            
            
        except Exception as e:
            return f"Error is {e}"        
        