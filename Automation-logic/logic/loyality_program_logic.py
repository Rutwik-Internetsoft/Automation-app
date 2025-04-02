from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logic.locators import Locators
from logic.dependencies import Dependencies

class Loyality:
    def __init__(self, appium_driver,calculations = None):
        self.driver = appium_driver
        self.short_wait = WebDriverWait(self.driver,5)
        self.wait = WebDriverWait(self.driver, 5)
        self.long_wait = WebDriverWait(self.driver,10)
        self.locators = Locators()
        self.locators.common_locators()
        self.locators.calculations_locators()
        self.locators.loyality_locators()
        test_deps = Dependencies(self.driver)
        self.calc = test_deps.get_calculations() 
        self.number = "(754) 831-9219"
        self.email = "Sophia4634@gmail.com"
            
    def adding_customer(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.locators.add_customer)).click()
            scrollable_command = ('new UiScrollable(new UiSelector().scrollable(true))'f'.scrollIntoView(new UiSelector().text("{self.number}"))')
            element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scrollable_command)
            element.click()
        except Exception as e:
            return f"Exception {e}"
    
    def finding_loyality_point(self):
        try:
            
            self.wait.until(EC.presence_of_element_located(self.locators.main_menu_button)).click()
            
            self.wait.until(EC.presence_of_element_located(self.locators.customers)).click()
                    
            scrollable_command = (f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{self.number} | {self.email}"))')
            # Wait for the element to be present and then click it
            element = self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, scrollable_command)))
            element.click()
            
            loyality_points = int(self.long_wait.until(EC.presence_of_element_located((self.locators.loyalty_points_locator))).text)
            
            self.long_wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
            return loyality_points
        except Exception as e:
            return f"Error {e}"
        
    def applied_loyality_points(self):
        try:
            checkbox = self.wait.until(EC.presence_of_element_located((self.locators.loyalty_checkbox)))

            # Check the attribute value; it typically returns "true" or "false"
            if checkbox.get_attribute("checked") != "true":
                checkbox.click()
                        
            applied_loyality_balance = 2 * float(self.wait.until(EC.presence_of_element_located((self.locators.loyalty_using))).text.strip().replace("- $",""))
            
            return int(applied_loyality_balance)
            
        except Exception as e:
            return f"error {e}"
          
    def adding_loyality_points(self):
        
        self.loyality_points = self.finding_loyality_point()
        try:
            self.calc.add_multiple_items(2)
            self.adding_customer()
            self.wait.until(EC.presence_of_element_located(self.locators.pay_button)).click()

            self.wait.until(EC.presence_of_element_located(self.locators.cash_pay)).click()
            
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH,'//android.view.ViewGroup[@resource-id="com.pays.pos:id/llOptions"]/androidx.appcompat.widget.LinearLayoutCompat[2]'))).click()
            
        except Exception as e:
            return f"{e}"
        return True
    
    def using_loyality_points(self):
        
        self.calc.add_multiple_items(1)
        
        self.adding_customer()
        
        before_order_loyality_points = self.finding_loyality_point()
        
        print(f"Before Transaction Points {before_order_loyality_points}")
        if before_order_loyality_points == 0:
            self.calc.pay()
            self.wait.until(EC.presence_of_element_located(self.locators.cash_pay)).click()
            self.long_wait.until(EC.element_to_be_clickable(self.locators.payment_home)).click()
            
            return f"Customer had 0 loyality Points, Re-Run the Test with Same Customer"
        useable_points = self.applied_loyality_points()
        
        print(f"Applied Points = {useable_points}")
        try:
            new_points_addition = int(self.calc.pay())
        
            print(f"The points that will be added after Transaction {new_points_addition}")
            
            
            self.wait.until(EC.presence_of_element_located(self.locators.cash_pay)).click()

            self.long_wait.until(EC.element_to_be_clickable(self.locators.payment_home)).click()
            
        except Exception as e:
            return f"{e}"
        
        used_points = before_order_loyality_points - useable_points
        
        print(f"used points = {used_points}")
        
        remaining_points = self.finding_loyality_point()
        
        print(f"remaining Points = {remaining_points}")
                
        print(type(remaining_points))        
        used_points += int(new_points_addition)
        print(f"final test of used points + new adding points {used_points}" )
        print(f"final remaining poinrs are {remaining_points}")
        
        if used_points == remaining_points:
            return True
        else:
            return False
        
        
        
        