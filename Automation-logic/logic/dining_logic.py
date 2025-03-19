from logic.takeout_logic import Calculations
from appium.webdriver.common.appiumby import AppiumBy
import random
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from logic.locators import Locators

class Dining:
    def __init__(self, appium_driver):
        self.driver = appium_driver
        
        self.short_wait = WebDriverWait(self.driver,5)
        self.wait = WebDriverWait(self.driver, 10)
        self.long_wait = WebDriverWait(self.driver,15)
        self.calc = Calculations(self.driver)
        self.guests = 0
        self.locators = Locators()
        self.locators.dining()
        self.locators.calculations_locators()
        self.locators.common_locators()
        
    def firing_items(self):
        try:
            print(self.guests)
            scroll_to_top_cmd = 'new UiScrollable(new UiSelector().resourceId("com.pays.pos:id/rvItemList")).scrollToBeginning(10)'
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_to_top_cmd)
            for i in range(1,7):
                check_box = self.wait.until(EC.presence_of_element_located(self.locators.checkbox))
                check_box.click()

                self.wait.until(EC.presence_of_element_located(self.locators.fire)).click()
                
                self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
                
                scrollable_cmd = f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().resourceId("com.pays.pos:id/checkedForFireHeader"))'
                self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scrollable_cmd)
            
            scrollable_cmd = f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().resourceId("com.pays.pos:id/checkedForFireHeader"))'            
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scrollable_cmd)
            
            self.wait.until(EC.presence_of_element_located(self.locators.checkbox)).click()
            
            self.wait.until(EC.presence_of_element_located(self.locators.fire)).click()
            
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            
            scroll_to_top_cmd = 'new UiScrollable(new UiSelector().resourceId("com.pays.pos:id/rvItemList")).scrollToBeginning(10)'
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_to_top_cmd)
            return True
            
        except Exception as e:
            return f"Error {e}"

    def connecting_printer(self):
        self.wait.until(EC.presence_of_element_located(self.locators.main_menu_button)).click()
        
        self.wait.until(EC.presence_of_element_located(self.locators.hardware)).click()
            
        self.wait.until(EC.presence_of_element_located(self.locators.printer)).click()
        
        print("Connect to your printer")
        
        time.sleep(10)
        
        print("Initializing connection")
        

        self.long_wait.until(EC.presence_of_element_located(self.locators.printer_unique_number)).send_keys("N434227FT0790")
        
        self.long_wait.until(EC.presence_of_element_located(self.locators.continue_button)).click()
        
        self.long_wait.until(EC.presence_of_element_located(self.locators.edit_printer)).click()
        
        try:
            self.long_wait.until(EC.presence_of_element_located(self.locators.dine_switch)).click()
        except:
            pass

        self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
        
        self.long_wait.until(EC.presence_of_element_located((AppiumBy.XPATH,'//android.widget.FrameLayout[@resource-id="android:id/custom"]/android.widget.LinearLayout/android.widget.LinearLayout'))).click()
        
        self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()

    def dine_in(self,square_table = None,floor = None):
        try:
            try:
                self.wait.until(EC.presence_of_element_located(self.locators.order_type_board))
            except:
                pass
            try:
                self.wait.until(EC.presence_of_element_located(self.locators.dine_in)).click()
            except:
                pass
            if floor is None:
                floor = random.randint(1,3)
            print(f"Floor Number {floor}")

            floor_path = f'(//androidx.appcompat.widget.LinearLayoutCompat[@resource-id="com.pays.pos:id/llItemName"])[{floor}]'    
            
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,floor_path))).click()
            
            square_tables  = self.wait.until(EC.presence_of_all_elements_located(self.locators.square_table))
            
            print(f" This Floor has {len(square_tables)} square tables")
            
            round_tables = self.wait.until(EC.presence_of_all_elements_located(self.locators.round_table))
            
            print(f"This Floor has {len(round_tables)} round tables")
            
            if square_table is None:
                square_table = random.randint(1,len(square_tables))
            print(f"table number {square_table}")

            table_path = f'(//android.widget.LinearLayout[@resource-id="com.pays.pos:id/llMainParentSquare"])[{square_table}]'
            
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,table_path))).click()
            
            return True
        
        except Exception as e:
            return f"Error {e}"
    
    def adding_items_dine_in(self,items_to_add= None,add_guest=None):
        try:
            self.guests = len(self.wait.until(EC.presence_of_all_elements_located(self.locators.guest_list)))
            print(f'guests present are {self.guests}')
            
            for i in reversed(range(1,self.guests+1)):
                path = f'(//android.view.ViewGroup[@resource-id="com.pays.pos:id/constraintHeader"])[{i}]'
                
                if add_guest == "add_guests" or add_guest is None:
                    if i>1:
                        add_customer_path = f'(//android.widget.ImageView[@resource-id="com.pays.pos:id/imgOrderMenu"])[{i}]'
                        self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,add_customer_path))).click()
                        self.wait.until(EC.presence_of_element_located(self.locators.assign_customers)).click()
                        self.wait.until(EC.presence_of_element_located(self.locators.adding_cust_one)).click()
                
                self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,path))).click()
                if items_to_add is None:
                    items_to_add = 2
                self.calc.add_multiple_items(items_to_add)
            
            self.wait.until(EC.presence_of_element_located(self.locators.proceed_to_fire)).click()
            
            return True
        
        except Exception as e:
        
            return f'Error {e}'
        
    def paying_individually(self,pay = None):
        payables = self.get_all_pay_texts()
        print(payables)
        try:
            for i in payables:
                    scroll_to_top_cmd = 'new UiScrollable(new UiSelector().resourceId("com.pays.pos:id/rvItemList")).scrollToBeginning(10)'
                    self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_to_top_cmd)
                    scrollable_cmd = f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{i}"))'
                    print(scrollable_cmd)
                    self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scrollable_cmd).click()
                    
                    if pay=="cash" or pay is None:
                        self.wait.until(EC.presence_of_element_located(self.locators.cash_pay)).click()
                    
                    elif pay=="card":
                        self.wait.until(EC.presence_of_element_located(self.locators.card_button)).click()
                    
                    else:
                        self.wait.until(EC.presence_of_element_located(self.locators.cash_pay)).click()

                    try:

                        self.wait.until(EC.presence_of_element_located(self.locators.checkout)).click()   
                    
                    except:
                    
                        pass
                    
                    try:
                    
                        self.wait.until(EC.presence_of_element_located(self.locators.payment_home)).click()
                    
                    except:
                    
                        pass
            return True    
        except Exception as e:
            return f"Error {e}"
    
    def swipe_down(self):
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.8)  # Start from 80% of screen height
        end_y = int(size["height"] * 0.2)  # Swipe to 20% of screen height

        self.driver.swipe(start_x, start_y, start_x, end_y, 800)  # Duration in milliseconds
        
    def get_all_pay_texts(self):
        collected_texts = set()
        last_count = -1

        while True:
            pay_elements = self.driver.find_elements(AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "Pay : $")]')

            for element in pay_elements:
                collected_texts.add(element.text.strip())

            # Stop scrolling when no new "Pay" options appear
            if len(collected_texts) == last_count:
                break

            last_count = len(collected_texts)

            # Scroll using swipe gesture (alternative)
            self.swipe_down()

        return list(collected_texts)

    def update_order(self,number_of_update = None):  
        try:
            self.wait.until(EC.presence_of_element_located(self.locators.update_order)).click()
            scroll_to_end_cmd = 'new UiScrollable(new UiSelector().resourceId("com.pays.pos:id/rvCartDineIn")).scrollToEnd(10)'
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_to_end_cmd)            
            if number_of_update is None:
                for i in range(5,7):  
                    scrollable_cmd = f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Guest {i}"))'
                    print(scrollable_cmd)
                    self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scrollable_cmd).click()
                    self.calc.add_multiple_items(1)
                self.wait.until(EC.presence_of_element_located(self.locators.proceed_to_fire)).click()
            else:
                for i in range(1,number_of_update):  
                    scrollable_cmd = f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Guest {i}"))'
                    print(scrollable_cmd)
                    self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scrollable_cmd).click()
                    self.calc.add_multiple_items(1)
                self.wait.until(EC.presence_of_element_located(self.locators.proceed_to_fire)).click()
                time.sleep(3)
            return True
        except Exception as e:
            return f"Error is {e}"
    
    def add_guests(self,number_of_guests = None):
        try:
            self.wait.until(EC.presence_of_element_located(self.locators.add_guests)).click()
            add_guests = ["tvZero","tvOne","tvTwo","tvThree","tvFour","tvFive","tvFive","tvSix","tvSeven","tvEight","tvNine"]
                    
            if number_of_guests is None:
                number_of_guests = "tvTwo"
                self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,f'//android.widget.TextView[@resource-id="com.pays.pos:id/{number_of_guests}"]'))).click()
                self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
                self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            else:
                    
                guests_to_add = random.choice(add_guests)
                self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,f'//android.widget.TextView[@resource-id="com.pays.pos:id/{guests_to_add}"]'))).click()
                self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
                self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            scroll_to_top_cmd = 'new UiScrollable(new UiSelector().resourceId("com.pays.pos:id/rvItemList")).flingToEnd(10)'
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_to_top_cmd)
            return True
        except Exception as e:
            return f"error is {e}"
        
    def remove_guests(self):
        try:
            scroll_to_top_cmd = 'new UiScrollable(new UiSelector().resourceId("com.pays.pos:id/rvItemList")).flingToEnd(10)'
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_to_top_cmd)
        
            added_number_of_guests = len(self.wait.until(EC.presence_of_all_elements_located(self.locators.remove_last_guest)))
            
            for i in range(added_number_of_guests-1):
                self.wait.until(EC.presence_of_element_located(self.locators.remove_guests)).click()
                self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
                scroll_to_top_cmd = 'new UiScrollable(new UiSelector().resourceId("com.pays.pos:id/rvItemList")).flingToEnd(10)'
                self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_to_top_cmd)
            self.wait.until(EC.presence_of_element_located(self.locators.remove_last_guest)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()

            return True
        
        except Exception as e:
            return f"Error is {e}"
        
    def wastage(self):
        try:
            time.sleep(2)
            for i in range(2):
                scroll_to_top_cmd = 'new UiScrollable(new UiSelector().resourceId("com.pays.pos:id/rvItemList")).flingToEnd(15)'
                self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_to_top_cmd)
                wastage_count = len(self.wait.until(EC.presence_of_all_elements_located(self.locators.wastage_count)))
                path = self.locators.wastage_icon[1].format(wastage_count)
                wastage = (AppiumBy.XPATH, path)

                
                self.wait.until(EC.presence_of_element_located(wastage)).click()
                
                reason = random.randint(1,5)
                self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,f'(//androidx.appcompat.widget.LinearLayoutCompat[@resource-id="com.pays.pos:id/llMain"])[{reason}]'))).click()
                self.wait.until(EC.presence_of_element_located(self.locators.done)).click()
                self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            return True
        except Exception as e:
            return f"error is {e}"
        
    def merge_tables(self):
        """Handles the merging of tables by selecting floors and tables sequentially."""
        try:
            time.sleep(2)
            self.wait.until(EC.element_to_be_clickable(self.locators.merge_table)).click()
            self.wait.until(EC.element_to_be_clickable(self.locators.spinner_floor)).click()
            self.wait.until(EC.element_to_be_clickable(self.locators.first_floor)).click()
            self.wait.until(EC.element_to_be_clickable(self.locators.spinner_table)).click()
            self.wait.until(EC.element_to_be_clickable(self.locators.first_table)).click()
            self.wait.until(EC.element_to_be_clickable(self.locators.merging_floor)).click()
            self.wait.until(EC.element_to_be_clickable(self.locators.second_floor)).click()
            self.wait.until(EC.element_to_be_clickable(self.locators.merging_table)).click()
            self.wait.until(EC.element_to_be_clickable(self.locators.third_table)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()

            return True
        except Exception as e:
            return f"Error occurred: {e}"          