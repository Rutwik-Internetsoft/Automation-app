from logic.takeout_logic import Calculations
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from logic.locators import Locators
from appium.webdriver.common.appiumby import AppiumBy

import random
class Cash_log:
    def __init__(self, appium_driver):
        self.driver = appium_driver
        
        self.short_wait = WebDriverWait(self.driver,5)
        self.wait = WebDriverWait(self.driver, 10)
        self.long_wait = WebDriverWait(self.driver,15)
        self.calc = Calculations(self.driver)
        self.locators = Locators()
        self.locators.calculations_locators()
        self.locators.common_locators()
        self.locators.cash_log()
        
        self.Cash_Drawer_AMT = 0.0
        self.Cash_out_AMT = 0.0
        self.Cash_in_AMT = 0.0    
        
    def check_cash_log_amt(self):
        try:
            
            self.wait.until(EC.presence_of_element_located(self.locators.main_menu_button)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.cash_log_button)).click()

            time.sleep(4)
            self.Cash_Drawer_AMT = float(self.wait.until(EC.presence_of_element_located(self.locators.cash_drawer_amt)).text.strip().replace("$",""))
        
            self.Cash_out_AMT = float(self.wait.until(EC.presence_of_element_located(self.locators.cash_out_amt)).text.strip().replace("$",""))
        
            self.Cash_in_AMT = float(self.wait.until(EC.presence_of_element_located(self.locators.cash_in_amt)).text.strip().replace("$",""))
            
            
            self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
            
            if (self.Cash_Drawer_AMT + self.Cash_out_AMT) == self.Cash_in_AMT:
                return True
            else:
                return False
            
        except Exception as e:
            return f"Error as {e}"
        
    def ordering(self,test = None):
        try:
            
            self.Checking_Cash_Drawer_AMT = self.Cash_Drawer_AMT
            self.Checking_Cash_out_AMT = self.Cash_out_AMT

            self.calc.add_multiple_items(2)
            order_price = self.calc.pay()
            print(f"Checking Cash Draw amount before transaction {self.Checking_Cash_Drawer_AMT}\n")
            print(f"Checking Cash out amount before transaction {self.Checking_Cash_out_AMT}\n")
            
            print(f"Order price is {order_price}\n")
            
            random_num = random.randint(1,3)
            
            cash = f'//android.widget.TextView[@resource-id="com.pays.pos:id/tvCash{random_num}"]'
            
            cash_paid  = float(self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,cash))).text.strip().replace("$",""))
            
            print(f"Amount paid by the customer {cash_paid}\n")
            
            self.Checking_Cash_Drawer_AMT +=cash_paid
            print(f"after taking cash from customer the drawer has {self.Checking_Cash_Drawer_AMT}\n")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,cash))).click()
            
            try:
                change_amount = self.wait.until(EC.presence_of_element_located(self.locators.change_amount)).text.strip().replace(" Change","")
                change_amount = float(change_amount.replace("$",""))
                self.Checking_Cash_Drawer_AMT -= change_amount
                self.Checking_Cash_out_AMT += change_amount
                print(f"Change amount returned to the customer {change_amount}\n")
                print(f"After giving the change back the drawer has {self.Checking_Cash_Drawer_AMT}")
                
            except:
                pass
            time.sleep(2)
            self.wait.until(EC.presence_of_element_located(self.locators.payment_home)).click()
            
            if test == "refund":
                self.calc.transaction("cash_log")
                refunded_amount = self.calc.cash_refund("cash_log")
                print(f"refuned amount is {refunded_amount}")
                self.Checking_Cash_Drawer_AMT -= refunded_amount
                self.Checking_Cash_out_AMT += refunded_amount
                
            if test == "tip":
                tip_percentage = self.calc.transaction_tip(1)
                self.Checking_Cash_Drawer_AMT += (order_price * tip_percentage)/100
            
            print(f"Checking Cash Drawer amount after transaction {self.Checking_Cash_Drawer_AMT}\n")
            print(f"Checking Cash out amount after transaction {self.Checking_Cash_out_AMT}\n")
        
            self.check_cash_log_amt()
            
            print(f"Cash drawer after Transaction {self.Cash_Drawer_AMT}\n")
            print(f"Cash out after Transaction {self.Cash_out_AMT}\n")
            print(f"Cash out after Transaction {self.Cash_in_AMT}\n")
            
            if abs(self.Checking_Cash_Drawer_AMT - self.Cash_Drawer_AMT)<=0.3 and abs(self.Checking_Cash_out_AMT- self.Cash_out_AMT)<=0.3 and ((self.Checking_Cash_Drawer_AMT + self.Checking_Cash_out_AMT)- self.Cash_in_AMT)<=0.3  :
                return True
            else:
                return f" the is difference in cash log check the logs"
            
        except Exception as e:
            return f"Error as {e}"
        
    
