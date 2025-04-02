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
 
#================Checking Setup===============
    
    def check_note(self,note_type = None):
        try:
            try:
                if note_type is None or note_type != "item_note":
                    self.wait.until(EC.element_to_be_clickable(self.locators.discount_menu)).click()
            except:
                pass
            if note_type == "item_note":
                self.wait.until(EC.presence_of_element_located(self.locators.add_item_note)).click()
                
            elif note_type == "add_note" or note_type is None:
                self.wait.until(EC.presence_of_element_located(self.locators.add_note)).click()
                
            p = '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvNotes"]/androidx.appcompat.widget.LinearLayoutCompat[1]/androidx.appcompat.widget.LinearLayoutCompat'
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,p))).click()
            self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
            l = self.driver.find_element(AppiumBy.XPATH,'//android.widget.TextView[@resource-id="com.pays.pos:id/txt_order_note"]').text
            if l == "Add Salt":
                return True
            else: 
                return f"Wrong Note Added:- {l}"
        except Exception as e:
            print("Cannot add Note")
            return f"Error is {e}"
    
    def check_discount(self,check = None):
        try:
            print("\n==============Checking If Discount Added================\n")
            discount_menu = self.wait.until(EC.presence_of_element_located(self.locators.discount_menu))
            discount_menu.click()
            self.wait.until(EC.presence_of_element_located(self.locators.add_discount)).click()
            
            if check == 0 or check is None:
                try:
                    self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiScrollable(new UiSelector().scrollable(true))''.setAsHorizontalList().scrollToEnd(10)')
                    print("✅ Scrolled to the end.")
                except:
                    print("⚠️ Could not scroll to the end. The list may be small.")
                try:
                    element = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.pays.pos:id/txtName" and @text="Happy Hours"]')))
                    element.click()
                    print("✅ Element found and clicked!")
                except:
                    print("❌ Element not found after scrolling.")
                    return False
                self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
                return True
            
            elif check == 1:
                try:
                    checking = False
                    self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiScrollable(new UiSelector().scrollable(true))''.setAsHorizontalList().scrollToEnd(10)')
                    print("✅ Scrolled to the end.")
                except:
                    print("⚠️ Could not scroll to the end. The list may be small.")
                try:
                    element = self.wait.until(
                        EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.pays.pos:id/txtName" and @text="Happy Hours"]')))
                    element.click()
                except:
                    checking = True
                if checking is True:
                    percentage_options = ['txt10', 'txt20', 'txt30']
            
                    chosen_option = random.choice(percentage_options)
            
                    self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,f'//android.widget.TextView[@resource-id="com.pays.pos:id/{chosen_option}"]'))).click()
                
                    self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
                    return True
            if check is None or check==1: 
                return f"The Discount not found"
            else:
                return f"The discount was not deleted"
        except Exception as e:
           return f"error {e}"
    
    def check_tax(self,check = None):
        if check is None or 0:
            try:
                self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,'//android.widget.ImageView[@resource-id="com.pays.pos:id/img_dropdown"]'))).click()
                
                m = self.driver.find_element(AppiumBy.XPATH,'//android.widget.TextView[@resource-id="com.pays.pos:id/txt_name" and @text="SBT "]').text
                if m == "SBT ":
                    print("Tax added successfully")
                    return True
                else:
                    return f"Tax not Added"
                
            except Exception as e:
                print("Element not found")
                return f"Error is {e}"
        elif check == 1:
            try:
                self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,'//android.widget.ImageView[@resource-id="com.pays.pos:id/img_dropdown"]'))).click()
                
                m = self.driver.find_element(AppiumBy.XPATH,'//android.widget.TextView[@resource-id="com.pays.pos:id/txt_name" and @text="SBT "]').text
                if m != "SBT":
                    print("Tax has been Removed")
                    return True
                else:
                    return f"Tax not removed"
                
            except Exception as e:
                print("Element not found")
                return f"Error is {e}"
    
    def check_tip(self,check = None):
        try:
            self.wait.until(EC.presence_of_element_located(self.locators.tip_button)).click()
            if check == 0 or check is None:
                try:
                    element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiScrollable(new UiSelector().scrollable(true)).setAsHorizontalList().scrollIntoView(new UiSelector().text("Good Service"))')
                    time.sleep(2)
                    element.click()
                    print("✅ Element found and clicked!")
                    self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
                    return True
                except:
                    print("❌ Element not found after scrolling.")
                    return False            
            elif check == 1:
                try:
                    checking = False
                    element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiScrollable(new UiSelector().scrollable(true)).setAsHorizontalList().scrollIntoView(new UiSelector().text("Good Service"))')
                    
                    element.click()
                    self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()

                    return False                   
                except:
                    checking = True                
                
                if checking is True:
                    percentage_options = ['txt10', 'txt20', 'txt30']
            
                    chosen_option = random.choice(percentage_options)
            
                    self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,f'//android.widget.TextView[@resource-id="com.pays.pos:id/{chosen_option}"]'))).click()
                
                    self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
                    return True
        except Exception as e:
           return f"error {e}"
    
    def add_multiple_items(self,num_items_to_add = None):
        try:
            if num_items_to_add is None:
                num_items_to_add = random.randint(2,5 )
            

            for _ in range(num_items_to_add):
                try:
                    # Select a random category (assuming categories are between indices 2 and 8)
                    category_index = random.randint(2, 8)
                    category = f'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvCategory"]/androidx.appcompat.widget.LinearLayoutCompat[{category_index}]'
                    self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, category))).click()

                    try:
                        item_elements = self.wait.until(EC.presence_of_all_elements_located(self.locators.items))


                        # Randomly select one item from the list
                        item_index = random.randint(1, len(item_elements))
                        
                        item = f'(//android.widget.LinearLayout[@resource-id="com.pays.pos:id/linear_item"])[{item_index}]'
                        
                        self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,item ))).click()

                        try:
                            # Wait for all modifier elements to be present
                            modifier_elements = self.short_wait.until(EC.presence_of_all_elements_located(self.locators.modifier_page))

                            if len(modifier_elements) < 1:
                                modifier_elements[0].click()
                            else:
                                # Randomly select 2 distinct modifiers from the list and click them
                                selected_modifiers = random.sample(modifier_elements, 2)
                                for modifier in selected_modifiers:
                                    modifier.click()

                            self.wait.until(EC.presence_of_element_located(self.locators.done)).click()

                        except Exception as e:
                            pass
                    except Exception as e:
                        pass
                except Exception as e:
                    pass
            return True
        except Exception as e:
            return f"Error is {e}"     
    
#===============Editing Setup================
    
    def tip_editing(self):
        try:
            self.setting_up()
        except:
            pass        
        
        try:    
            self.wait.until(EC.element_to_be_clickable(self.locators.tips_btn)).click() 
            
            self.wait.until(EC.element_to_be_clickable(self.locators.tips_add_new)).click()
            
            self.wait.until(EC.presence_of_element_located(self.locators.tip_name)).send_keys("Good Service")
            
            self.wait.until(EC.presence_of_element_located(self.locators.tip_amt)).send_keys("10")
            
            self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
            
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            
            text_views = self.driver.find_elements(AppiumBy.XPATH, 
    '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvTipList"]'
    '/androidx.appcompat.widget.LinearLayoutCompat[4]/androidx.appcompat.widget.LinearLayoutCompat//android.widget.TextView')
            
            if text_views[0].text!= "Good Service" or text_views[1].text!= "10.00%":
                return False
            time.sleep(2)
            
            r = len(self.wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvTipList"]/androidx.appcompat.widget.LinearLayoutCompat/androidx.appcompat.widget.LinearLayoutCompat'))))
            
            
            element1 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, f'(//android.widget.ImageView[@resource-id="com.pays.pos:id/imageCheck"])[{r}]')))
            
            element2 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.ImageView[@resource-id="com.pays.pos:id/imageCheck"])[1]')))

            self.driver.execute_script("mobile: dragGesture", {
    "elementId": element1.id,
    "endX": element2.location['x'],
    "endY": element2.location['y']
})
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            text_views = self.driver.find_elements(AppiumBy.XPATH, 
    '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvTipList"]'
    '/androidx.appcompat.widget.LinearLayoutCompat[1]/androidx.appcompat.widget.LinearLayoutCompat//android.widget.TextView')

            if text_views[0].text!= "Good Service" or text_views[1].text!= "10.00%":
                return False    
            return True     
        except Exception as e:
            return f"Error is {e}"        
        
    def tax_editing(self):
        
        try:
            self.setting_up()
        except:
            pass
        try:
            self.wait.until(EC.element_to_be_clickable(self.locators.taxes_btn)).click() 
            self.wait.until(EC.element_to_be_clickable(self.locators.taxes_add_new)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.tax_name)).send_keys("SBT")
            self.wait.until(EC.presence_of_element_located(self.locators.tip_amount)).send_keys("5")
            self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
            self.long_wait.until(EC.presence_of_element_located(self.locators.save)).click()
            assert self.wait.until(EC.presence_of_element_located(self.locators.tax_added_successfully)),"Tax not Added"
            return True

        except Exception as e:
            print("Tip Not ADD")
            return f"Errorr is {e}"
    
    def discount_editing(self):
        
        try:
            self.setting_up()
        except:
            pass
        try:
            discount_name = "Happy Hours"
            discount_amt = "15"
            self.wait.until(EC.element_to_be_clickable(self.locators.discount_btn)).click() 
            self.wait.until(EC.element_to_be_clickable(self.locators.discount_add_btn)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.discount_name_btn)).send_keys(f"{discount_name}")
            self.wait.until(EC.presence_of_element_located(self.locators.discount_atm)).send_keys(f"{discount_amt}")
            self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,f'//android.widget.TextView[@text="{discount_name}"]/preceding-sibling::*[@resource-id="com.pays.pos:id/imgCheckBox"]'))).click()
            
            amt = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,f'//android.widget.TextView[@text="{discount_name}"]/following-sibling::*[@resource-id="com.pays.pos:id/tvRate"]'))).text.strip().replace(".00 %","")

            if amt == "15":
                return True
            else:
                return f"Amount Entered is Wrong"
        except Exception as e:
            print("Discount Not Added")
            return f"Error is {e}"
        
    def order_note_editing(self):
        try:
            self.setting_up()
        except:
            pass   
        try:
            Order_note = "Add Salt"
            self.wait.until(EC.element_to_be_clickable(self.locators.order_note_btn)).click() 
            self.wait.until(EC.element_to_be_clickable(self.locators.order_note_add_btn)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.order_note_title)).send_keys(f"{Order_note}")  
            self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            element1 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,'(//android.widget.ImageView[@resource-id="com.pays.pos:id/imageCheck"])[1]')))
            new_order = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,'//android.widget.TextView[@text="Add Salt"]/preceding-sibling::android.widget.ImageView[@resource-id="com.pays.pos:id/imageCheck"]')))
            
            self.driver.execute_script("mobile: dragGesture", {
    "elementId": new_order.id,
    "endX": element1.location['x'],
    "endY": element1.location['y']
})
            try:
                self.short_wait.until(EC.presence_of_element_located(self.locators.save)).click()
            except:
                pass
            return True
        
        except Exception as e:
            return f"Error as {e}"
        
        
#===============Set Up===================
        
    def setup_check(self):
        try:
            try:
                self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
            except:
                pass
            self.wait.until(EC.presence_of_element_located(self.locators.takeout_btn)).click()
            self.add_multiple_items(2)
            return True
            
        except Exception as e:
            return f"Error is as {e}"
    
    def setting_up(self):
        try:
            self.wait.until(EC.element_to_be_clickable(self.locators.main_menu_button)).click() 
            
            self.wait.until(EC.element_to_be_clickable(self.locators.setup_btn)).click() 
            return True
        except Exception as e:
            return f"Error is {e}"           


#===========Removing Setup================

    def remove_tip(self):
        try:
            self.setting_up()
            self.wait.until(EC.presence_of_element_located(self.locators.tips_btn)).click()
            
            r = len(self.wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvTipList"]/androidx.appcompat.widget.LinearLayoutCompat/androidx.appcompat.widget.LinearLayoutCompat'))))
            
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,'//android.widget.TextView[@text="Good Service"]/following-sibling::*[@resource-id="com.pays.pos:id/layout_menu"]'))).click()
            self.wait.until(EC.presence_of_element_located(self.locators.delete_btn)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            time.sleep(2)
            m = len(self.wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvTipList"]/androidx.appcompat.widget.LinearLayoutCompat/androidx.appcompat.widget.LinearLayoutCompat'))))
            self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
            
            if m<r:
                return True
            else:
                return False
            
        except Exception as e:
            return f"error is {e}"
        
    def remove_tax(self):
        
        try:
            self.setting_up()
        except:
            pass
        try:
            self.wait.until(EC.element_to_be_clickable(self.locators.taxes_btn)).click() 
            m = len(self.wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvTaxList"]/androidx.appcompat.widget.LinearLayoutCompat/androidx.appcompat.widget.LinearLayoutCompat'))))
            
            assert self.wait.until(EC.presence_of_element_located(self.locators.tax_added_successfully)),"Tax not Added"
            
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,'(//android.widget.ImageView[@content-desc="Menu"])[4]'))).click()            
            self.wait.until(EC.presence_of_element_located(self.locators.delete_btn)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            time.sleep(2)
            r = len(self.wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvTaxList"]/androidx.appcompat.widget.LinearLayoutCompat/androidx.appcompat.widget.LinearLayoutCompat'))))
            self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
            if r<m:
                return True
            else:
                return False
        except Exception as e:
            print("Tip Not ADD")
            return f"Errorr is {e}"

    def remove_discount(self):
        
        try:
            self.setting_up()
        except:
            pass
        try:
            self.wait.until(EC.element_to_be_clickable(self.locators.discount_btn)).click() 
            m = len(self.wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvDiscountList"]/androidx.appcompat.widget.LinearLayoutCompat/androidx.appcompat.widget.LinearLayoutCompat'))))
            
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,'//android.widget.TextView[@text="Happy Hours"]/following-sibling::*[@resource-id="com.pays.pos:id/layout_menu"]'))).click()

            self.wait.until(EC.presence_of_element_located(self.locators.delete_btn)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            time.sleep(2)
            r = len(self.wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvDiscountList"]/androidx.appcompat.widget.LinearLayoutCompat/androidx.appcompat.widget.LinearLayoutCompat'))))
            self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
            if r<m:
                return True
            else:
                return False
        except Exception as e:
            print("Tip Not ADD")
            return f"Errorr is {e}"

    def remove_ordernote(self):
        try:
            self.setting_up()
            self.wait.until(EC.presence_of_element_located(self.locators.order_note_btn)).click()
            
            r = len(self.wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvNoteLise"]/androidx.appcompat.widget.LinearLayoutCompat/androidx.appcompat.widget.LinearLayoutCompat'))))
            
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,'(//android.widget.ImageView[@content-desc="Menu"])[1]'))).click()            
            #//android.widget.TextView[@text="Add Salt"]
            self.wait.until(EC.presence_of_element_located(self.locators.delete_btn)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            
            m = len(self.wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvNoteLise"]/androidx.appcompat.widget.LinearLayoutCompat/androidx.appcompat.widget.LinearLayoutCompat'))))
            self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
            if m<r:
                return True
            else:
                return False
        except Exception as e:
            return f"error is {e}"