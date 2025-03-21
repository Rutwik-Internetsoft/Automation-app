from logic.locators import Locators
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Login:
    def __init__(self, appium_driver):
        self.driver = appium_driver
        self.wait = WebDriverWait(self.driver, 3)
        self.locators = Locators()
        self.locators.login_page_locators()

    def check_if_main_page(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.locators.main_page_indicator))
            print("Already logged in!")
            return True  
        except Exception as e:
            print(f"Not Logged in yet")
            return False

    def login(self):
        if self.check_if_main_page():
            return True
        try:
            self.wait.until(EC.presence_of_element_located(self.locators.username_field)).send_keys("automation@yopmail.com")
            self.wait.until(EC.presence_of_element_located(self.locators.password_field)).send_keys("654321")
            self.wait.until(EC.element_to_be_clickable(self.locators.login_button)).click()

            self.wait.until(EC.presence_of_element_located(self.locators.nav_host))
            print("Login successful!")
            return True
        
        except Exception as e:
            print(f"Login failed: {e}")
            return False  # Login failed

    def passcode(self):
        try:
            # Check if main page indicator is already present
            self.wait.until(EC.presence_of_element_located(self.locators.main_page_indicator))
            return True
        except Exception:
            pass
        
        try:
            time.sleep(2)
            self.wait.until(EC.presence_of_element_located(self.locators.passcode_field)).send_keys('1111')
            self.wait.until(EC.presence_of_element_located(self.locators.action_bar_root))
            self.wait.until(EC.presence_of_element_located(self.locators.main_page_indicator))
            return True
        except Exception as e:
            print(f"Passcode entry failed: {e}")
            return False
