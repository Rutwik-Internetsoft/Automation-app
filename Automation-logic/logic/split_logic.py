
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logic.takeout_logic import Calculations
from logic.locators import Locators

class Split_cash:
    
    def __init__(self, appium_driver):
        self.driver = appium_driver
        self.wait = WebDriverWait(self.driver, 5)
        self.long_wait = WebDriverWait(self.driver,30)
        self.short_wait = WebDriverWait(self.driver,5)
        self.total_amount = 0.0
        self.surcharge = 0.0
        self.calc = Calculations(self.driver)
        self.locators = Locators()
        self.locators.split_locators()
        self.locators.calculations_locators()
        self.locators.common_locators()
    
    def price_checking_cash(self):
        paid_amount = self.calc.pay()
        
        print(f"The amount after adding items {paid_amount}")
        
        self.total_amount = self.calc.cash_amount()
        
        print(f"Amount on the cash plate {self.total_amount}")
        
        if paid_amount == self.total_amount:
            return True
        else:
            False
    
    def price_checking_card(self):
        paid_amount = self.calc.pay() 
        self.surcharge = self.calc.surcharge_actual()

        paid_amount+= self.surcharge
        print(f"The amount after adding items {paid_amount}")
        
        self.total_amount = self.calc.card_amount()
        
        print(f"Amount on the cash plate {self.total_amount}")
        
        if abs(paid_amount - self.total_amount)<=0.3:
            return True
        else:
            False
    
    def gift_card_balance(self):
        
        self.wait.until(EC.presence_of_element_located(self.locators.giftcard)).click()
        
        self.wait.until(EC.presence_of_element_located(self.locators.gift_card_balance)).click()
                    
        self.wait.until(EC.presence_of_element_located(self.locators.gift_card_number)).send_keys("76673389")
        
        self.wait.until(EC.presence_of_element_located(self.locators.check_balance)).click()
        
        self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
                
        balance = float(self.wait.until(EC.presence_of_element_located(self.locators.gift_balance)).text.strip().replace("$",""))
        
        print(f"Your gift card balance is {balance}$")
        
        self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
                
        self.wait.until(EC.presence_of_element_located(self.locators.back_button)).click()
        return balance
    
    def splitting_cash(self,tip=None):
        
        try:
            
            
            self.wait.until(EC.presence_of_element_located(self.locators.splitting_button)).click()
                        
            self.wait.until(EC.presence_of_element_located(self.locators.two_ways)).click()
                        
            self.wait.until(EC.presence_of_element_located(self.locators.next_button_split)).click()
            if tip != None:
                self.calc.tip()
            
            person_one_paid_amount = self.calc.cash_amount()
            
            print(f"Person one paid {person_one_paid_amount}")
                        
            self.wait.until(EC.presence_of_element_located(self.locators.cash_pay)).click()
            
            self.wait.until(EC.presence_of_element_located(self.locators.next_split)).click()

            if tip != None:
                self.calc.tip()
            person_two_paid_amount = self.calc.cash_amount()
            print(f"person two paid {person_two_paid_amount}")
            
            self.wait.until(EC.presence_of_element_located(self.locators.cash_pay)).click()
            
            self.long_wait.until(EC.element_to_be_clickable((AppiumBy.XPATH,"//android.widget.TextView[@resource-id='com.pays.pos:id/llHome']"))).click()
            
            if abs((person_one_paid_amount + person_two_paid_amount)) - self.total_amount <=0.3:
                return True
            else:
                return False
            
        except Exception as e:
            return f"error {e}"
          
    def splitting_card(self):
        
        try:
                        
            self.wait.until(EC.presence_of_element_located(self.locators.splitting_button)).click()
            
            self.wait.until(EC.presence_of_element_located(self.locators.two_ways)).click()
                        
            self.wait.until(EC.presence_of_element_located(self.locators.next_button)).click()
            
            person_one_paid_amount = self.calc.card_amount() 
            
            print(f"Person one paid {person_one_paid_amount}")
                        
            self.wait.until(EC.presence_of_element_located(self.locators.card_button)).click()
            
            self.long_wait.until(EC.presence_of_element_located(self.locators.next_split)).click()

            person_two_paid_amount = self.calc.card_amount()
            
            self.long_wait.until(EC.presence_of_element_located(self.locators.card_button)).click()
            print(f"person two paid {person_two_paid_amount}")

            self.long_wait.until(EC.element_to_be_clickable(self.locators.payment_home)).click()
            print(f"Total amount to pay {self.total_amount}")
            print(f"Surcharge Applie is {2*self.surcharge}")
            
            if abs(((person_one_paid_amount + person_two_paid_amount)) - (self.total_amount)) <=0.3:
                return True
            
            else:
                return False
            
        except Exception as e:
            return f"error {e}"
        
    def splitting_gift_card(self):
        
        try:
                        
            self.wait.until(EC.presence_of_element_located(self.locators.splitting_button)).click()
                        
            self.wait.until(EC.presence_of_element_located(self.locators.two_ways)).click()
                        
            self.wait.until(EC.presence_of_element_located(self.locators.next_button)).click()
            
            person_one_paid_amount = self.calc.cash_amount()
            
            print(f"Person one paid {person_one_paid_amount}")
                        
            self.wait.until(EC.presence_of_element_located(self.locators.gift_pay)).click()
                        
            self.wait.until(EC.presence_of_element_located(self.locators.gift_card_number)).send_keys("76673389")
        
            self.wait.until(EC.presence_of_element_located(self.locators.gift_charge)).click()
                        
            self.wait.until(EC.presence_of_element_located(self.locators.next_split)).click()

            person_two_paid_amount = self.calc.cash_amount()
            print(f"person two paid {person_two_paid_amount}")
            
            self.wait.until(EC.presence_of_element_located(self.locators.gift_pay)).click()
                        
            self.wait.until(EC.presence_of_element_located(self.locators.gift_card_number)).send_keys("76673389")
                        
            self.wait.until(EC.presence_of_element_located(self.locators.gift_charge)).click()
            
            self.long_wait.until(EC.element_to_be_clickable((AppiumBy.XPATH,"//android.widget.TextView[@resource-id='com.pays.pos:id/llHome']"))).click()
            
            if abs((person_one_paid_amount + person_two_paid_amount)) - self.total_amount <=0.3:
                return True
            else:
                return False
            
        except Exception as e:
            return f"error {e}"
        
    def transaction_checking(self): 
        try:
            self.long_wait.until(EC.presence_of_element_located(self.locators.transaction_button)).click()
            
            id1 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,'(//android.widget.TextView[@resource-id="com.pays.pos:id/txtTransactionId"])[1]'))).text
            
            print(f"order ID 1 {id1}")
            
            id2 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,'(//android.widget.TextView[@resource-id="com.pays.pos:id/txtTransactionId"])[2]'))).text
            
            print(f"order ID 2 {id2}")
            
            if id1!=id2:
                return False
            p1 = float(self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,'(//android.widget.TextView[@resource-id="com.pays.pos:id/tvTotalAmount"])[1]'))).text.strip().replace("$",""))
            
            print(f"order 1 amount {p1}")
            
            p2 = float(self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,'(//android.widget.TextView[@resource-id="com.pays.pos:id/tvTotalAmount"])[2]'))).text.strip().replace("$",""))
            
            print(f"order 1 amount {p2}")
                        
            self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
            
            if abs((p2+p1) - self.total_amount)<=0.3:
                return True
            else:
                return False
            
        except Exception as e:
            return f"error {e}"

        
            
            
            

            
            
        
        
        
        
