import random
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import Locators

class PAT:
    def __init__(self, appium_driver):
        self.driver = appium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.long_wait = WebDriverWait(self.driver, 30)
        self.short_wait = WebDriverWait(self.driver,2)  
        self.subtotal = 0.0
        self.disCount = 0.0
        self.serviceCharge = 0.0
        self.taxes = 0.0
        self.total = None
        self.end_pay = 0.0
        self.surcharge_ = 0.0        
        self.locators = Locators()
        self.locators.PAT()
        
    def login_logic(self):
        try:
            try:
            # Check if main page indicator is already present
                self.wait.until(EC.presence_of_element_located(self.locators.add_table))
                return True
            except Exception:
                pass
            
            self.wait.until(EC.presence_of_element_located(self.locators.email_login)).send_keys('automation@yopmail.com')
            self.wait.until(EC.presence_of_element_located(self.locators.password_login)).send_keys('654321')
            self.wait.until(EC.presence_of_element_located(self.locators.login_PAT)).click()
            return True

        except Exception as e:
            return f"Error is {e}"
        
    def passcode(self):
        try:
            try:
            # Check if main page indicator is already present
                self.wait.until(EC.presence_of_element_located(self.locators.add_table))
                return True
            except Exception:
                pass
            
            self.wait.until(EC.presence_of_element_located(self.locators.passcode)).send_keys("1111")
            return True
        except Exception as e:
            return f"Error is {e}"

    def add_table(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.locators.add_table)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.add_table_2)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.continue_btn)).click()
            return True
        except Exception as e:
            return f"Error is {e}"
        
    
        
    def add_multiple_items(self,num_items_to_add = None):
        try:
            if num_items_to_add is None:
                num_items_to_add = random.randint(2,5 )
            

            for _ in range(num_items_to_add):
                try:
                    
                    categories = len(self.wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.internetsoft.pax:id/rvCategory"]/androidx.appcompat.widget.LinearLayoutCompat'))))
                    print(categories)
                    category_index = random.randint(2, categories)
                    category = f'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.internetsoft.pax:id/rvCategory"]/androidx.appcompat.widget.LinearLayoutCompat[{category_index}]'
                    
                    self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, category))).click()

                    try:
                        items = '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.internetsoft.pax:id/rvCategory"]/androidx.appcompat.widget.LinearLayoutCompat'
                        item_elements = self.wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,items)))


                        # Randomly select one item from the list
                        item_index = random.randint(1, len(item_elements))
                        
                        item = f'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.internetsoft.pax:id/rvCategory"]/androidx.appcompat.widget.LinearLayoutCompat[{item_index}]'
                        
                        self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,item ))).click()

                        # try:
                        #     # Wait for all modifier elements to be present
                        #     modifier_elements = self.short_wait.until(EC.presence_of_all_elements_located(self.locators.modifier_page))

                        #     if len(modifier_elements) < 1:
                        #         modifier_elements[0].click()
                        #     else:
                        #         # Randomly select 2 distinct modifiers from the list and click them
                        #         selected_modifiers = random.sample(modifier_elements, 2)
                        #         for modifier in selected_modifiers:
                        #             modifier.click()

                        #     self.wait.until(EC.presence_of_element_located(self.locators.done)).click()

                        # except Exception as e:
                        #     pass
                    except Exception as e:
                        pass
                except Exception as e:
                    pass
            return True
        except Exception as e:
            return f"Error is {e}"
