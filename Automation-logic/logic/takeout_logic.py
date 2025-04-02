import re
import random
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from logic.locators import Locators

class Calculations:
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
        self.locators.calculations_locators()
        self.locators.common_locators()
    
    def order(self,order_type = None):
        try:
            
            if order_type == "Take Out":
                self.wait.until(EC.presence_of_element_located(self.locators.takeout_btn)).click()
                return True
            elif order_type == "Dine In":
                self.wait.until(EC.presence_of_element_located(self.locators.dine_in)).click()
                return True
            elif order_type == "Phone Order":
                self.wait.until(EC.presence_of_element_located(self.locators.phone_order_button)).click()
                return True
            elif order_type == "Open Order":
                self.wait.until(EC.presence_of_element_located(self.locators.open_order)).click()
                return True
            elif order_type == "Stay":
                self.wait.until(EC.presence_of_element_located(self.locators.stay)).click()
                return True

            elif order_type is None:
                self.wait.until(EC.presence_of_element_located(self.locators.takeout_btn)).click()
                return True
            else:
                return False
        except Exception as e:
            return f"ERROR IS {e}"
      
    def sub_total(self):
        try:
            self.subtotal = float(self.wait.until(EC.presence_of_element_located(self.locators.sub_total)).text.strip().replace("$", ""))
            print(f"Sub total is {self.subtotal}")
            return self.subtotal
        except Exception as e:
            print(f"Error in sub_total: {e}")
            return False

    def discount(self):
        """Extracts and returns the discount amount as a float."""
        try:
            el = self.wait.until(EC.presence_of_element_located(self.locators.discount))
            dis = el.text.replace("-$", "").strip()
            self.disCount = float(dis)
            print("discount is " , self.disCount)
            return self.disCount
        except Exception as e:
            print(f"Error fetching discount: {e}")
            return 0.0 

    def tax_calculation(self):
        try:
            
            tax = float(self.wait.until(EC.presence_of_element_located((self.locators.tax))).text.strip().replace("$",""))
            print(f"Tax applied is {tax}")
            return tax
        except Exception as e:
            print(f"Error in tax_calculation: {e}")
            return Exception
        
    def service_charge(self):
        try:
            self.serviceCharge = float(self.wait.until(EC.element_to_be_clickable(self.locators.service_charge)).text.strip().replace("$", ""))
            print(f"Service charge is {self.serviceCharge}")
            return self.serviceCharge
        except Exception as e:
            print(f"Error in service_charge: {e}")
            return False
        
    def surcharge_percentage(self):
        try:
            surcharge_element = self.wait.until(EC.presence_of_element_located(self.locators.surcharge))
            surcharge_text = surcharge_element.text
            match = re.search(r"(\d+(\.\d+)?)%", surcharge_text)
            surcharge = float(match.group(1)) if match else 0.0
            return surcharge
        except Exception as e:
            print(f"Error in paychecking: {e}")
            return False

    def pay(self,amount = None):
        try:
            pay_button = self.wait.until(EC.presence_of_element_located(self.locators.pay_button))
            self.end_pay = float(pay_button.text.strip().replace("Pay $", ""))
            if amount!=None:
                return self.end_pay
            pay_button.click()
            return self.end_pay

        except Exception as e:
            print(f"Error in pay: {e}")
            return Exception
    
    def surcharge_actual(self):
        try:
            self.surcharge_ = float(self.wait.until(EC.presence_of_element_located(self.locators.surcharge_actual)).text.strip().replace("$", ""))
            return self.surcharge_
        except Exception as e:
            print(f"Error in surcharge_actual: {e}")
            return Exception
    
    def total_calculation(self):
        total = self.sub_total() + self.tax_calculation() + self.service_charge()
        return total
    
    def tip(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.locators.tip_button)).click()

            percentage_options = ['txt10', 'txt20', 'txt30']
            chosen_option = random.choice(percentage_options)
            
            tip_xpath = self.locators.tip_option[1].format(chosen_option)
            
            tip_locator = (AppiumBy.XPATH, tip_xpath)
            tip_option = self.wait.until(EC.presence_of_element_located(tip_locator))
            tip_option.click()
            tip_percentage = float(tip_option.text.strip().replace("%", ""))

            self.wait.until(EC.presence_of_element_located(self.locators.save_tip)).click() 

            return tip_percentage

        except Exception as e:
            print(f"Error in tip: {e}")
            return Exception   


    def add_multiple_items(self,num_items_to_add = None):
        try:
            if num_items_to_add is None:
                num_items_to_add = random.randint(2,5 )
            

            for _ in range(num_items_to_add):
                try:
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

    def add_discount(self):
        try:
            print("Adding Discount")

            discount_menu = self.wait.until(EC.presence_of_element_located(self.locators.discount_menu))
            discount_menu.click()
            self.wait.until(EC.presence_of_element_located(self.locators.add_discount)).click()
            
            percentage_options = ['txt10', 'txt20', 'txt30']
            
            chosen_option = random.choice(percentage_options)
            
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,f'//android.widget.TextView[@resource-id="com.pays.pos:id/{chosen_option}"]'))).click()
            
            self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
            return True
        except Exception as e:
            return f"error {e}"
    
    def add_note(self,note_type = None):
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
                
            random_note = random.randint(1,3)
            p = f'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvNotes"]/androidx.appcompat.widget.LinearLayoutCompat[{random_note}]/androidx.appcompat.widget.LinearLayoutCompat'
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,p))).click()
            self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
            return True
        except Exception as e:
            print("Cannot add Note")
            
    def transaction(self,cash_log = None):
        time.sleep(1)
        try:
            
            self.long_wait.until(EC.presence_of_element_located(self.locators.transaction_button)).click()
            if cash_log == "cash_log":
                self.long_wait.until(EC.presence_of_element_located(self.locators.transaction_button)).click()
                return True
            time.sleep(1)
            
            transaction_total = float(self.long_wait.until(EC.presence_of_element_located(self.locators.transaction_total_amt)).text.strip().replace("$",""))
            
            return abs(transaction_total)
            
        except:
            return False

    def cash_itemwise_refund(self,cash_log = None):
        try:
            
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,'(//android.widget.TextView[@resource-id="com.pays.pos:id/tvOrderType"])[1]'))).click()
            
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,'//android.widget.TextView[@resource-id="com.pays.pos:id/tvIssueRefund"]'))).click()
            
            print("Refund Initiated")
            try:
                
                self.wait.until(EC.presence_of_element_located(self.locators.cash_refund))
                time.sleep(2)
                items = len(self.wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,'(//android.widget.ImageView[@resource-id="com.pays.pos:id/ivCheck"])'))))
                num = random.randint(1,items)
                self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,f'(//android.widget.ImageView[@resource-id="com.pays.pos:id/ivCheck"])[{num}]'))).click()
                
                itm_amount = float(self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,f'(//androidx.appcompat.widget.LinearLayoutCompat[@resource-id="com.pays.pos:id/linearLayoutCompat"])[{num}]/androidx.appcompat.widget.LinearLayoutCompat/android.widget.LinearLayout/following-sibling::*'))).text.strip().replace("$",""))
                
                print(f"The Item that user is not refunding is of {itm_amount}$\n")
                self.long_wait.until(EC.element_to_be_clickable(self.locators.done)).click()
                time.sleep(2)
                self.long_wait.until(EC.element_to_be_clickable(self.locators.done)).click()
                time.sleep(2)
                self.wait.until(EC.element_to_be_clickable(self.locators.save_refund)).click()
                time.sleep(2)
            except Exception as e:
                return f'Error {e}'
        
                 
            try:
                print("final Check")
                refunded_value_parent = self.wait.until(EC.presence_of_element_located(self.locators.ref_parent))

                text_views = refunded_value_parent.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")                
                refund_amount = float(text_views[1].text.strip().replace("$",""))
                
                print("refunded Amount ", refund_amount)
                total_refunded_amount = itm_amount + refund_amount
                total_value_parent = self.wait.until(EC.presence_of_element_located(self.locators.tot_parent_cash))

                text_view = total_value_parent.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
                
                paid_amount = float(text_view[1].text.strip().replace("$",""))
                print(paid_amount)
                
                if (abs(paid_amount - total_refunded_amount))<=0.3:
                    self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
                    if cash_log == "cash_log":
                        return itm_amount
                    return True
                else:
                    return False
            except Exception as e:
                return f"Error {e}"
        except Exception as e:
            return f'error is {e}'

    def cash_refund(self,cash_log = None):
        try:
            try:
                self.wait.until(EC.presence_of_element_located(self.locators.transaction_button)).click()
            except:
                pass

            self.wait.until(EC.presence_of_element_located(self.locators.order_1)).click()
            
            self.wait.until(EC.presence_of_element_located(self.locators.refund_button)).click()
            
            
            print("Refund Initiated")
            
            try: 
                self.wait.until(EC.presence_of_element_located(self.locators.cash_refund))
                time.sleep(2)
                self.long_wait.until(EC.element_to_be_clickable(self.locators.done)).click()
                time.sleep(2)
                self.long_wait.until(EC.element_to_be_clickable(self.locators.done)).click()
                time.sleep(2)
                self.wait.until(EC.element_to_be_clickable(self.locators.save_refund)).click()
                time.sleep(2)
                
            except Exception as e:
                return f"Error {e}"
                                            
            try:
                refunded_value_parent = self.wait.until(EC.presence_of_element_located(self.locators.ref_parent))

                text_views = refunded_value_parent.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")                
                refund_amount = float(text_views[1].text.strip().replace("$",""))
                
                print("refunded Amount ", refund_amount)
                
                total_value_parent = self.wait.until(EC.presence_of_element_located(self.locators.tot_parent_cash))

                text_view = total_value_parent.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
                
                paid_amount = float(text_view[1].text.strip().replace("$",""))
                print(f"The Paid amount is {paid_amount} $")
                
                tip_parent = self.wait.until(EC.presence_of_element_located(self.locators.tip_parent))
                
                text_tip = tip_parent.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")                
                
                tip_prize = float(text_tip[1].text.strip().replace("$",""))
                
                if (paid_amount-refund_amount-tip_prize)<=0.3:
                    self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
                    if cash_log == "cash_log":
                        return refund_amount
                    return True
                else:
                    return False
            except Exception as e:
                return f"Error {e}"
                        
        except Exception:
            return Exception

    def card_refund(self):
        try:
            try:
                self.wait.until(EC.presence_of_element_located(self.locators.transaction_button)).click()
            except:
                pass
            self.wait.until(EC.presence_of_element_located(self.locators.order_1)).click()
            
            self.wait.until(EC.presence_of_element_located(self.locators.refund_button)).click()
            
            print("Refund Initiated")
        
                
            try:
            
                self.long_wait.until(EC.presence_of_element_located(self.locators.save)).click()
                self.wait.until(EC.presence_of_element_located(self.locators.save_refund)).click()
            except:
                return "Could'nt save the refund"
            
            try:
                refunded_value_parent = self.wait.until(EC.presence_of_element_located(self.locators.ref_parent))
                                
                text_views = refunded_value_parent.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
                
                refund_amount = float(text_views[1].text.strip().replace("$",""))
                print(f" The Refunded Amount is {refund_amount}\n")
                
                total_value_parent = self.wait.until(EC.presence_of_element_located(self.locators.tot_parent_card))
                
                text_view = total_value_parent.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")                
                paid_amount = float(text_view[1].text.strip().replace("$",""))
                print(f"The Customer paid {paid_amount}")
                
                print(f"Checking if both amounts are same")
                if paid_amount==refund_amount:
                    print("The refunded Amount and Paid amount are same \n Test Passed")    
                    self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
                    return True
                else:
                    return False
            except Exception as e:
                return f"Error {e}"
                        
        except Exception:
            return Exception

    def isOrder(self,order_type = None):
        
        try:
            order_text = self.short_wait.until(EC.presence_of_element_located(self.locators.transaction_order_type)).text
        except:
            pass
        try:
            order_text = self.short_wait.until(EC.presence_of_element_located(self.locators.current_order_type)).text.strip().replace("Current Order: ","")
        except:
            pass    
        
        print("The Order Type should be ", order_text)
        
        try:
            if order_text == order_type:
                return True
            elif order_type is None:
                return False
            else:
                return False
        except Exception as e:
            return f"error {e}"

    def connect_PAX(self):
        try:
            self.long_wait.until(EC.presence_of_element_located(self.locators.main_menu_button)).click()
            
            self.wait.until(EC.presence_of_element_located(self.locators.hardware)).click()
            
            self.wait.until(EC.presence_of_element_located(self.locators.card_machine)).click()
            
            try:
                self.wait.until(EC.presence_of_element_located(self.locators.disconnect_pax))
                
                self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
                return True  

            except:
                pass                  
            
            try:
                self.wait.until(EC.presence_of_element_located(self.locators.connect_pax)).click()
                self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
                self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
                return True  

            except:
                pass
        except:
            return False

    def tear_down(self):
        try:

            # Use the locators in your tear_down method:

            # Click the drawer button
            self.wait.until(EC.presence_of_element_located(self.locators.main_menu_button)).click()

            # Click Logout
            self.wait.until(EC.presence_of_element_located(self.locators.logout)).click()

            # Wait for the custom linear element to be present
            self.wait.until(EC.presence_of_element_located(self.locators.sure_popup))

            # Click the save button
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()

            self.wait.until(EC.presence_of_element_located(self.locators.login))
            return True

        except:
            print("Error")
    
    def cash_amount(self):
        try:
            cash_text = self.wait.until(EC.presence_of_element_located(self.locators.cash_amount)).text
            match = re.search(r"\$(\d+\.\d+)", cash_text)
            amount = float(match.group(1)) if match else 0.0
            return amount
        except Exception as e:
            print(f"Error in amount: {e}")
            return Exception

    def card_amount(self):
        try:
            cash_text = self.wait.until(EC.presence_of_element_located(self.locators.card_amount)).text
            match = re.search(r"\$(\d+\.\d+)", cash_text)
            amount = float(match.group(1)) if match else 0.0
            return amount
        except Exception as e:
            print(f"Error in amount: {e}")
            return Exception
    
    def cash_pay(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.locators.cash_pay)).click()
            try:
                self.long_wait.until(EC.element_to_be_clickable(self.locators.payment_home)).click()
            except Exception as e:
                return f"Error {e}"
            return True
        except Exception as e:
            print(f"Payment Failed. Error: {e}")
            return False

    def card_pay(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.locators.credit_card_button)).click()
            try:
                self.long_wait.until(EC.element_to_be_clickable(self.locators.payment_home)).click()
            except Exception as e:
                return f"Error {e}"
            return True
        except Exception as e:
            print(f"Payment Failed. Error: {e}")
            return False

    def manual_item(self):
        try:
            
            self.wait.until(EC.element_to_be_clickable(self.locators.keypad)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.keypad))
            for j in range(3):
                
                food_item = ["Mango Ice Cream","Seasonal Fruits","sandwich chocolate"]
                
                self.wait.until(EC.presence_of_element_located(self.locators.custom_item_name)).send_keys(food_item[j])

                for i in range(3):
                    random_num = random.randint(0,8)
                    numbers = ["tvOne","tvTwo","tvThree","tvFive","tvFour","tvSix","tvSeven","tvEight","tvNine"]
                    prize = '//android.widget.TextView[@resource-id="com.pays.pos:id/{}"]'.format(numbers[random_num])
                    self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,prize))).click()
                self.wait.until(EC.element_to_be_clickable(self.locators.imgAdd)).click()
            self.wait.until(EC.element_to_be_clickable(self.locators.txtsave)).click()
            
            return True
        
        except Exception as e:
            return f"Error is {e}"
        
    def update_item_quantity(self):
        try:
            Cart_qty = len(self.wait.until(EC.presence_of_all_elements_located(self.locators.cart_qty)))
            itm = random.randint(1,Cart_qty)
            path = f'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvCartList"]/androidx.appcompat.widget.LinearLayoutCompat[{itm}]/android.widget.LinearLayout'
            
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,path))).click()
            
            clicks=random.randint(1,5)
            
            for _ in range(clicks):
                self.wait.until(EC.presence_of_element_located(self.locators.plus_button)).click()
                
            self.add_note("item_note")
            self.wait.until(EC.presence_of_element_located(self.locators.done)).click()
            qty_path = f'(//android.widget.TextView[@resource-id="com.pays.pos:id/txtQuantity"])[{itm}]'
            
            qty = int(self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,qty_path))).text)
            return True
        except Exception as e:
            return f"Error is {e}"
             
    def adding_new_customer(self):
        try:
            self.wait.until(EC.element_to_be_clickable(self.locators.add_customer)).click()    
            self.wait.until(EC.presence_of_element_located(self.locators.create_customer)).click()
            
            
            names = ["John", "Emma", "Michael", "Sophia", "David"]
            surnames = ["Anderson", "Miller", "Wilson", "Taylor", "Martinez"]
            domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]

            random_name = random.choice(names)
            random_surname = random.choice(surnames)
            area_code = random.randint(200, 999)
            prefix = random.randint(100, 999)
            line_number = random.randint(1000, 9999)
            random_phone = f"({area_code}) {prefix}-{line_number}"
            random_email = f"{random_name}{random.randint(1000, 9999)}@{random.choice(domains)}"
            
            
            self.wait.until(EC.presence_of_element_located(self.locators.first_name_field)).send_keys(random_name)

            self.wait.until(EC.presence_of_element_located(self.locators.surname_field)).send_keys(random_surname)
            self.wait.until(EC.presence_of_element_located(self.locators.phone_field)).send_keys(random_phone)
            self.wait.until(EC.presence_of_element_located(self.locators.email_field_cust)).send_keys(random_email)
            
            
            self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click()
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()

            cust = '//android.widget.TextView[@resource-id="com.pays.pos:id/txtName" and @text="{} {}  Loyalty Point: 0"]'.format(random_name, random_surname)
            
            time.sleep(2)
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,cust))).click()
            return True
        except Exception as e:
            return f"Error as {e}"
        # //android.widget.TextView[@resource-id="com.pays.pos:id/txtName" and @text="Emma Miller  Loyalty Point: 0"]
        
    def transaction_tip(self,transaction_number):
        try:
            self.wait.until(EC.presence_of_element_located(self.locators.transaction_button)).click()
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,f'(//android.widget.TextView[@resource-id="com.pays.pos:id/tvOrderType"])[{transaction_number}]'))).click()
            self.wait.until(EC.presence_of_element_located(self.locators.end_tip)).click()
            percentage_options = ['txt10', 'txt20', 'txt30']
            chosen_option = random.choice(percentage_options)
            
            tip_xpath = self.locators.tip_option[1].format(chosen_option)
            print(tip_xpath)
            
            tip_locator = (AppiumBy.XPATH, tip_xpath)
            tip_option = self.wait.until(EC.presence_of_element_located(tip_locator))
            tip_option.click()
            tip_percentage = float(tip_option.text.strip().replace("%", ""))
            time.sleep(2)
            self.wait.until(EC.presence_of_element_located(self.locators.txtsave)).click() 
            
            self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            time.sleep(2)
            self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()
            return tip_percentage
        except Exception as e:
            return f"Error as {e}"

    def phone_order(self):
        try:
            names = ["John", "Emma", "Michael", "Sophia", "David"]
            surnames = ["Anderson", "Miller", "Wilson", "Taylor", "Martinez"]
            domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]

            random_name = random.choice(names)
            random_surname = random.choice(surnames)
            area_code = random.randint(200, 999)
            prefix = random.randint(100, 999)
            line_number = random.randint(1000, 9999)
            random_phone = f"({area_code}) {prefix}-{line_number}"
            random_email = f"{random_name}{random.randint(1000, 9999)}@{random.choice(domains)}"
            
            self.wait.until(EC.presence_of_element_located(self.locators.first_name_field)).send_keys(random_name)
            self.wait.until(EC.presence_of_element_located(self.locators.surname_field)).send_keys(random_surname)
            self.wait.until(EC.presence_of_element_located(self.locators.phone_field)).send_keys(random_phone)
            self.wait.until(EC.presence_of_element_located(self.locators.email_field)).send_keys(random_email)
            
            self.wait.until(EC.presence_of_element_located(self.locators.next_button)).click()

            if self.isOrder("Phone Order"):
                return True
            else:
                return False
        
        except Exception as e:
            return f"Error is {e}" 
        
    def search_cust_order(self):
        try:
            try:
                self.wait.until(EC.element_to_be_clickable(self.locators.add_customer)).click() 
            except:
                pass   
            try:
                self.wait.until(EC.presence_of_element_located(self.locators.search_cust)).click()
            except:
                pass
            time.sleep(4)
            num_cust = len(self.wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvCustomerList"]/androidx.appcompat.widget.LinearLayoutCompat/androidx.appcompat.widget.LinearLayoutCompat'))))
            if num_cust == 0:
                self.adding_new_customer()
                return True
            
            random_cust = random.randint(1,num_cust)
            
            parent = f'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvCustomerList"]/androidx.appcompat.widget.LinearLayoutCompat[{random_cust}]/androidx.appcompat.widget.LinearLayoutCompat'

            parent_element = self.driver.find_element(AppiumBy.XPATH,parent)

            name_element = parent_element.find_element(AppiumBy.ID, "com.pays.pos:id/txtName")
                        # Extract the text
            name_text = name_element.text.strip()  # Remove extra spaces
            name = " ".join(name_text.split()[:2]) if name_text else "No name available"

            print(f"The Customer selected is {name}")
            
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,parent))).click()
            try:
                self.wait.until(EC.presence_of_element_located(self.locators.next)).click()
            except:
                pass
            
            added_cust = self.wait.until(EC.presence_of_element_located(self.locators.add_customer)).text.strip()
            print(f"The name on the reciept would be {added_cust}")
            if added_cust == name:
                print("Both the names are same")
                print("Test Passed")
                return True
            else:
                print(f"The names are not same {added_cust} != {name}")
                return False
        except Exception as e:
            return f"Error is {e}"      
    
    def cash_payment(self):
        to_pay = self.pay()
        cash_amount_final = self.cash_amount()
        if abs((to_pay)-cash_amount_final)<=0.3:
            self.cash_pay()
            return True
        else:
            return False

    def card_payment(self):
        to_pay = self.pay()
        surcharge = self.surcharge_actual()
        card_amount_final = self.card_amount()
        if abs((to_pay+surcharge)-card_amount_final)<=0.3:
            self.card_pay()
            return True
        else:
            return False
        
    def save_order(self,process):
        try:
            try:
                self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
            except:
                pass
            self.wait.until(EC.presence_of_element_located(self.locators.pending_order)).click()
            if process == "Pay":
                return self.ord_upt(process ="Pay")
            
            elif process == "Update":
                return self.ord_upt(process ="Update")
            
            elif process == "Cancel":
                return self.ord_upt(process = "Cancel")
            
            else:
                return self.ord_upt("Pay")
        except Exception as e:
            return f"Error as {e}"
        
    def ord_upt(self, process):
        
        try:
            if process is None or process == "Pay":
                tvAmt = float(self.wait.until(EC.presence_of_element_located(self.locators.tvAmt)).text.strip().replace("$",""))

                self.wait.until(EC.presence_of_element_located(self.locators.txtpay_button)).click()
                
                return tvAmt
            elif process == "Update":
                self.wait.until(EC.presence_of_element_located(self.locators.update_order)).click()
                self.add_multiple_items(2)  
                self.add_note("add_note")    
                self.add_discount()     
                return True
            elif process == "Cancel":
                try:
                    date1 = self.wait.until(EC.presence_of_element_located(self.locators.date)).text
                except:
                    pass
                try:
                    date1 = self.wait.until(EC.presence_of_element_located(self.locators.date1)).text
                except:
                    pass
                self.wait.until(EC.presence_of_element_located(self.locators.cancel)).click()
                reasons = len(self.wait.until(EC.presence_of_all_elements_located(self.locators.cancel_reason)))
                reason_num = random.randint(1,reasons)
                path = f'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvReasons"]/androidx.appcompat.widget.LinearLayoutCompat[{reason_num}]/androidx.appcompat.widget.LinearLayoutCompat'
                self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,path))).click()
                self.wait.until(EC.presence_of_element_located(self.locators.done)).click()
                self.wait.until(EC.presence_of_element_located(self.locators.save)).click()
                self.wait.until(EC.presence_of_element_located(self.locators.save)).click()  
                time.sleep(2)
                
                
                try:
                    date2 = self.wait.until(EC.presence_of_element_located(self.locators.date)).text
                except:
                    pass
                try:
                    date2 = self.wait.until(EC.presence_of_element_located(self.locators.date1)).text
                except:
                    pass                
                
                if date1 == date2: 
                    self.wait.until(EC.presence_of_element_located(self.locators.home_icon)).click()   
                    return True
                else: 
                    return f"Date Doesn't Match"
        except Exception as e:
            return f"Error is {e}"
        
    def remove_item(self):
        try:
            Cart_qty = len(self.wait.until(EC.presence_of_all_elements_located(self.locators.cart_qty)))
            itm = random.randint(1,Cart_qty)
            path = f'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.pays.pos:id/rvCartList"]/androidx.appcompat.widget.LinearLayoutCompat[{itm}]/android.widget.LinearLayout'
            
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,path))).click()
            self.wait.until(EC.presence_of_element_located(self.locators.remove_itm)).click()            
            return True
        except Exception as e:
            return f"Error is {e}"
            