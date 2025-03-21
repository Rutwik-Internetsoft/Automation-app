import pytest
import allure
from logic.dependencies import Dependencies

@allure.epic("Orderflow")
@allure.feature("Stay order in Cash")
class TestStayCash:
    
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        """Automatically inject the appium_driver fixture for every test."""
        self.driver = appium_driver
        self.deps = Dependencies(self.driver)
        self.calc = self.deps.get_calculations()

    @allure.story("Order Management")
    @allure.title("Select Open Order")
    def test_stayorder_btn(self):
        with allure.step("Selecting Open Order"):
            print("===========Starting Stay Order Test=================")
            assert self.calc.order("Stay") == True


    @allure.story("Manual Item Management")
    @allure.title("Add a Manual Item and Set Quantity")
    @allure.description("Tests if a manual item can be added with a specified quantity.")
    def test_manual_item_and_qty(self):
        print("\n===================Adding Manual Items===============\n")
        
        isTrue = self.calc.manual_item()
        assert isTrue is True

    @allure.story("Customer Management")
    @allure.title("Adding New Customers")
    @allure.description("Tests if new customers can be added to the POS system.")
    def test_adding_customers(self):
        print("\n=============Adding Customers===========")
        assert self.calc.adding_new_customer() == True

    @allure.story("Multiple Item Handling")
    @allure.title("Add Multiple Items")
    @allure.description("Tests if multiple items can be added to a single order.")
    def test_add_multiple_item(self):
        print("\n==========Adding Multiple Items==============")
        assert self.calc.add_multiple_items(2)

    @allure.story("Item Quantity Update")
    @allure.title("Update Item Quantity")
    @allure.description("Ensures that the quantity of an existing item can be updated.")
    def test_updating_item(self):
        print("\n==============Updating Quantity===============")
        assert self.calc.update_item_quantity() == True

    @allure.story("Total Calculation & Payment")
    @allure.title("Verify Total Calculation & Payment")
    @allure.description("Validates that the total amount before payment matches the expected calculations.")
    def test_pay_check(self):
        print("================Checking Cart=================")
        self.total = self.calc.total_calculation()
        self.end_pay = self.calc.pay()
        print(f"Checking if our calculation and pay button amt matches that is {self.total}::::::::::{self.end_pay}")

        assert abs(self.end_pay - self.total) <= 0.3

    @allure.story("Card Payment Validation")
    @allure.title("Verify Card Payment with Surcharge")
    @allure.description("Checks if the total amount with surcharge matches the card payment deduction.")
    def test_card_amt_hike_check(self):
        card_amt = self.calc.card_amount()
        self.total = self.calc.total_calculation()
        self.surcharge_percentage = self.calc.surcharge_percentage()
        self.total_after_including_surcharge = self.total + ((self.total * self.surcharge_percentage) / 100)
        assert abs(card_amt - self.total_after_including_surcharge) <= 0.3

    @allure.story("Cash Payment Validation")
    @allure.title("Verify Cash Payment Amount")
    @allure.description("Checks if the cash payment amount matches the expected total.")
    def test_cash_amt_check(self):
        cash_amount = self.calc.cash_amount()
        self.total = self.calc.total_calculation()
        assert abs(cash_amount - self.total) <= 0.3

    @allure.story("Finalizing Cash Payment")
    @allure.title("Complete Cash Payment")
    @allure.description("Ensures that cash payments can be successfully processed.")
    def test_cash_pay(self):
        assert self.calc.cash_pay() == True
