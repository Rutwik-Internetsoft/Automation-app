import yaml
from appium.webdriver.common.appiumby import AppiumBy
import random

class LocatorLoader:
    def __init__(self, locator_file: str, default_section: str = "common"):
        """
        :param locator_file: Path to the YAML file containing locators.
        :param default_section: Default section if none is specified.
        """
        self.locator_file = locator_file
        self.default_section = default_section
        self.locators = self.load_locators()

    def load_locators(self) -> dict:
        """Load locator definitions from the YAML file."""
        try:
            with open(self.locator_file, "r") as stream:
                return yaml.safe_load(stream) or {}
        except yaml.YAMLError as exc:
            print(f"Error loading YAML: {exc}")
            return {}
        except FileNotFoundError as exc:
            print(f"Locator file not found: {exc}")
            return {}
        
    def get_locator(self, key: str, section: str = None, **kwargs):
        
        """
        Retrieve a locator.
        - `section` is optional; defaults to the pre-configured default section.
        - If the key is missing in the given section, it falls back to the default section.
        - If the locator requires formatting, pass the required `kwargs`.
        """
        section = section or self.default_section  # Use default if not provided
        section_data = self.locators.get(section, {})

        # If key is not found in the section, fall back to the default section
        locator_info = section_data.get(key)
        if not locator_info and section != self.default_section:
            print(f"Warning: Locator '{key}' not found in section '{section}', trying '{self.default_section}'")
            locator_info = self.locators.get(self.default_section, {}).get(key)

        if locator_info:
            by_key = locator_info.get("by")
            locator_str = locator_info.get("locator")

            # Format locator string if placeholders exist
            if kwargs:
                locator_str = locator_str.format(*kwargs.values())

            mapping = {
                "id": AppiumBy.ID,
                "xpath": AppiumBy.XPATH,
                "accessibility_id": AppiumBy.ACCESSIBILITY_ID,
                "android_uiautomator": AppiumBy.ANDROID_UIAUTOMATOR
            }
            return mapping.get(by_key, by_key), locator_str

        raise ValueError(f"Locator '{key}' not found in section '{section}' or fallback section '{self.default_section}'.")

class Locators(LocatorLoader):
    
    def __init__(self):
        locator_file="C:/Users/rutwik/Automation/logic/locators.yaml"
        self.locator_loader = LocatorLoader(locator_file=locator_file)
    
    def get_locator(self, key, section, **kwargs):
        return self.locator_loader.get_locator(key, section, **kwargs)

    def calculations_locators(self):
        """Store and retrieve all calculation-related locators."""
        self.tip_parent = self.locator_loader.get_locator("tip_parent","calculations")
        self.cancel_reason = self.locator_loader.get_locator("cancel_reason","calculations")
        self.add_item_note = self.locator_loader.get_locator("add_item_note","calculations")
        self.plus_button = self.locator_loader.get_locator("plus_button","calculations")
        self.cart_qty = self.locator_loader.get_locator("Cart_qty","calculations")
        self.custom_item_name = self.locator_loader.get_locator("custom_item_name","calculations")
        self.keypad_view = self.locator_loader.get_locator("keypad_view","calculations")
        self.keypad = self.locator_loader.get_locator("keypad","calculations")
        self.takeout_btn = self.locator_loader.get_locator("takeout_btn","calculations")
        self.discount_menu = self.locator_loader.get_locator("discount_menu", "calculations")
        self.add_discount = self.locator_loader.get_locator("add_discount","calculations")
        self.modifier_page = self.locator_loader.get_locator("modifiers_page","calculations")
        self.tax = self.locator_loader.get_locator("tax", "calculations")
        self.sub_total = self.locator_loader.get_locator("sub_total", "calculations")
        self.discount = self.locator_loader.get_locator("discount", "calculations")
        self.tax_dropdown = self.locator_loader.get_locator("tax_dropdown", "calculations")
        self.tax_list = self.locator_loader.get_locator("tax_list", "calculations")
        self.service_charge = self.locator_loader.get_locator("service_charge", "calculations")
        self.cash_refund = self.locator_loader.get_locator("cash_refund", "calculations")
        self.done = self.locator_loader.get_locator("done", "calculations")
        self.surcharge = self.locator_loader.get_locator("surcharge", "calculations")
        self.surcharge_actual = self.locator_loader.get_locator("surcharge_actual", "calculations")
        self.tip_button = self.locator_loader.get_locator("tip_button", "calculations")
        self.tip_option = self.locator_loader.get_locator("tip_option", "calculations")
        self.tip_amount = self.locator_loader.get_locator("tip_amount", "calculations")
        self.save_tip = self.locator_loader.get_locator("save_tip", "calculations")
        self.save_refund = self.locator_loader.get_locator("save_refund", "calculations")
        self.ref_parent = self.locator_loader.get_locator("ref_parent", "calculations")
        self.tot_parent_card = self.locator_loader.get_locator("tot_parent_card", "calculations")
        self.tot_parent_cash = self.locator_loader.get_locator("tot_parent_cash", "calculations")
        self.card_amount = self.locator_loader.get_locator("card_amount", "calculations")
        self.credit_card_button = self.locator_loader.get_locator("credit_card_button", "calculations")
        self.home_button = self.locator_loader.get_locator("home_button", "calculations")
        self.cash_amount = self.locator_loader.get_locator("cash_amount", "calculations")
        self.items = self.locator_loader.get_locator("items","calculations")
        self.add_note  = self.locator_loader.get_locator("add_note","calculations")

    def common_locators(self):
        """Store and retrieve all common locators."""
        self.first_name_field = self.get_locator("first_name_field", "common")
        self.surname_field = self.locator_loader.get_locator("surname_field", "common")
        self.phone_field = self.locator_loader.get_locator("phone_field", "common")
        self.email_field = self.locator_loader.get_locator("email_field", "common")
        self.email_field_cust = self.locator_loader.get_locator("email_field_new_cust", "common")
        self.cancel = self.locator_loader.get_locator("cancel","common")
        self.phone_order_button = self.get_locator("phone_order_btn", "common")
        self.next_button = self.get_locator("next", "common") 
        self.update_order = self.locator_loader.get_locator("update_order","common")
        self.pending_order = self.locator_loader.get_locator("pending_order","common")
        self.date = self.locator_loader.get_locator("date","common")
        self.date1 = self.locator_loader.get_locator("date1","common")
        self.tvAmt = self.locator_loader.get_locator("tvAmt","common")
        self.add_customer = self.locator_loader.get_locator("add_customer", "common")
        self.create_customer = self.locator_loader.get_locator("create_customer","common")
        self.imgAdd = self.locator_loader.get_locator("imgAdd","common")
        self.end_tip = self.locator_loader.get_locator("end_tip","common")
        self.giftcard = self.locator_loader.get_locator("giftcard","common")
        self.next = self.locator_loader.get_locator("next", "common")
        self.order_type_board = self.locator_loader.get_locator("order_type_board", "common")
        self.transaction_order_type = self.locator_loader.get_locator("transaction_order_type","common")
        self.current_order_type = self.locator_loader.get_locator("current_order_type", "common")
        self.continue_button = self.locator_loader.get_locator("continue", "common")
        self.hardware = self.locator_loader.get_locator("hardware", "common")
        self.txtpay_button = self.locator_loader.get_locator("txtpay_button","common")
        self.pay_button = self.locator_loader.get_locator("pay_button", "common")
        self.printer = self.locator_loader.get_locator("printer", "common")
        self.main_menu_button = self.locator_loader.get_locator("main_menu", "common")
        self.card_machine = self.locator_loader.get_locator("card_machine","common")
        self.disconnect_pax = self.locator_loader.get_locator("disconnect_pax","common")
        self.connect_pax = self.locator_loader.get_locator("connect_pax","common")
        self.logout = self.locator_loader.get_locator("logout", "common")
        self.sure_popup = self.locator_loader.get_locator("sure_popup", "common")
        self.save = self.locator_loader.get_locator("save", "common")
        self.txtsave = self.locator_loader.get_locator("txtsave","common")
        self.login = self.locator_loader.get_locator("login", "common")
        self.cash_pay = self.locator_loader.get_locator("cash_pay", "common")
        self.open_order = self.locator_loader.get_locator("open_oder","common")
        self.stay = self.locator_loader.get_locator("stay","common")
        self.payment_home = self.locator_loader.get_locator("payment_home", "common")
        self.transaction_button = self.locator_loader.get_locator("transaction_button", "common")
        self.card_pay = self.locator_loader.get_locator("card_pay", "common")
        self.home_icon = self.locator_loader.get_locator("home_icon", "common")
        self.card_button = self.locator_loader.get_locator("card_button", "common")
        self.gift_pay = self.locator_loader.get_locator("gift_pay", "common")
        self.gift_card_number = self.locator_loader.get_locator("gift_card_number", "common")
        self.gift_charge = self.locator_loader.get_locator("gift_charge", "common")
        self.gift_card_balance = self.locator_loader.get_locator("gift_card_balance", "common")
        self.gift_balance = self.locator_loader.get_locator("gift_balance", "common")
        self.back_button = self.locator_loader.get_locator("back_button", "common")
        self.check_balance = self.locator_loader.get_locator("check_balance", "common")
        self.transaction_total_amt = self.locator_loader.get_locator("transaction_total_amt","common")

    def login_page_locators(self):
        
        """Store and retrieve all login page locators."""
        self.username_field = self.locator_loader.get_locator("username_field", "login_page")
        self.password_field = self.locator_loader.get_locator("password_field", "login_page")
        self.login_button = self.locator_loader.get_locator("login_button", "login_page")
        self.main_page_indicator = self.locator_loader.get_locator("main_page_indicator", "login_page")
        self.nav_host = self.locator_loader.get_locator("nav_host", "login_page")
        self.passcode_field = self.locator_loader.get_locator("passcode_field", "login_page")
        self.action_bar_root = self.locator_loader.get_locator("action_bar_root", "login_page")
        
    def loyality_locators(self):
        """Store and retrieve all loyalty-related locators."""
        self.phone = self.locator_loader.get_locator("phone", "loyality")
        self.customers = self.locator_loader.get_locator("customers", "loyality")
        self.loyalty_points_locator = self.locator_loader.get_locator("loyality_points_locator", "loyality")
        self.loyalty_checkbox = self.locator_loader.get_locator("loyality_checkbox", "loyality")
        self.loyalty_using = self.locator_loader.get_locator("loyality_using", "loyality")
    
    def split_locators(self):
        """Store and retrieve all split-related locators."""
        self.splitting_button = self.locator_loader.get_locator("splitting_button", "split")
        self.two_ways = self.locator_loader.get_locator("two_ways", "split")
        self.next_button = self.locator_loader.get_locator("next_button", "split")
        self.next_split = self.locator_loader.get_locator("next_split", "split")

    def dining(self):
        """Store and retrieve all dining-related locators."""
        
        self.fire = self.locator_loader.get_locator("fire", "dining")
        self.checkbox = self.locator_loader.get_locator("checkbox", "dining")
        self.printer_unique_number = self.locator_loader.get_locator("printer_unique_number", "dining")
        self.edit_printer = self.locator_loader.get_locator("edit_printer", "dining")
        self.dine_switch = self.locator_loader.get_locator("dine_switch", "dining")
        self.dine_in = self.locator_loader.get_locator("dine_in", "dining")
        self.square_table = self.locator_loader.get_locator("square_table", "dining")
        self.round_table = self.locator_loader.get_locator("round_table", "dining")
        self.guest_list = self.locator_loader.get_locator("guest_list", "dining")
        self.proceed_to_fire = self.locator_loader.get_locator("proceed_to_fire", "dining")
        self.checkout = self.locator_loader.get_locator("checkout", "dining")
        self.add_guests = self.locator_loader.get_locator("add_guests","dining")
        self.remove_guests = self.locator_loader.get_locator("remove_guests","dining")
        self.remove_last_guest = self.locator_loader.get_locator("remove_last_guest","dining")
        self.wastage_icon = self.locator_loader.get_locator("wastage_icon","dining")
        self.wastage_count = self.locator_loader.get_locator("wastage_count","dining")
        self.assign_customers = self.locator_loader.get_locator("assign_customers","dining")
        self.adding_cust_one = self.locator_loader.get_locator("adding_cust_one","dining")
        
        self.floor_plan = self.locator_loader.get_locator("floor_plan","dining")
                
        self.merge_table = self.locator_loader.get_locator("merge_table", "dining")
        
        self.spinner_floor = self.locator_loader.get_locator("spinnerFloor", "dining")
        
        self.first_floor = self.locator_loader.get_locator("first_floor", "dining")
        
        self.spinner_table = self.locator_loader.get_locator("spinnerTable", "dining")
        
        self.first_table = self.locator_loader.get_locator("first_table", "dining")
        
        self.merging_floor = self.locator_loader.get_locator("merging_floor", "dining")
        
        self.second_floor = self.locator_loader.get_locator("second_floor", "dining")
        
        self.merging_table = self.locator_loader.get_locator("merging_table", "dining")
        
        self.third_table = self.locator_loader.get_locator("third_table", "dining")
        
        self.merged_tables_selection = self.locator_loader.get_locator("merged_tables_selection","dining")
        
    def cash_log(self):
        random_number = random.randint(0, 3)

        self.cash_log_button = self.locator_loader.get_locator("cash_log_button","cash_log")
        self.cash_drawer_amt = self.locator_loader.get_locator("cash_drawer_amt","cash_log")
        self.cash_in_amt = self.locator_loader.get_locator("cash_in_amt","cash_log")
        self.cash_out_amt = self.locator_loader.get_locator("cash_out_amt","cash_log")
        self.change_amount = self.locator_loader.get_locator("change_amount","cash_log")