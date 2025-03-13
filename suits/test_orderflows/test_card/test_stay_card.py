import pytest
import allure
from logic.dependencies import Dependencies

@allure.epic("POS System Automation")
@allure.feature("Stay Card Order")
class TestStayCash:
    
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        """Automatically inject the appium_driver fixture for every test."""
        self.driver = appium_driver
        self.deps = Dependencies(self.driver)
        self.calc = self.deps.get_calculations()
    
    @allure.story("Device Connection")
    @allure.title("Connect PAX Payment Terminal")
    def test_pax_connection(self):
        assert self.calc.connect_PAX() == True
        print("PAX Connected Successfully")

    @allure.story("Order Management")
    @allure.title("Select Stay Order")
    def test_stayorder_btn(self):
        with allure.step("Selecting Stay Order"):
            assert self.calc.order("Stay") == True


    @allure.story("Manual Item Management")
    @allure.title("Add a Manual Item and Set Quantity")
    @allure.description("Tests if a manual item can be added with a specified quantity.")
    def test_manual_item_and_qty(self):
        isTrue = self.calc.manual_item()
        assert isTrue is True

    @allure.story("Customer Management")
    @allure.title("Search Existing Customers")
    @allure.description("Tests if Existing customer can be added to the POS system.")
    def test_adding_existing_customers(self):
        assert self.calc.search_cust_order() == True

    @allure.story("Multiple Item Handling")
    @allure.title("Add Multiple Items")
    @allure.description("Tests if multiple items can be added to a single order.")
    def test_add_multiple_item(self):
        assert self.calc.add_multiple_items(3)

    @allure.story("Item Quantity Update")
    @allure.title("Update Item Quantity")
    @allure.description("Ensures that the quantity of an existing item can be updated.")
    def test_updating_item(self):
        assert self.calc.update_item_quantity() == True

    @allure.story("Total Calculation & Payment")
    @allure.title("Verify Total Calculation & Payment")
    @allure.description("Validates that the total amount before payment matches the expected calculations.")
    def test_pay_check(self):
        self.total = self.calc.total_calculation()
        print(self.total)
        self.end_pay = self.calc.pay()
        assert abs(self.end_pay - self.total) <= 0.3

    @allure.story("Card Payment Validation")
    @allure.title("Verify Card Payment with Surcharge")
    @allure.description("Checks if the total amount with surcharge matches the card payment deduction.")
    def test_card_amt_hike_check(self):
        card_amt = self.calc.card_amount()
        self.total = self.calc.total_calculation()
        print(self.total)
        self.surcharge_percentage = self.calc.surcharge_percentage()
        self.total_after_including_surcharge = self.total + ((self.total * self.surcharge_percentage) / 100)
        print(self.total_after_including_surcharge)
        assert abs(card_amt - self.total_after_including_surcharge) <= 0.3

    @allure.story("Cash Payment Validation")
    @allure.title("Verify Cash Payment Amount")
    @allure.description("Checks if the cash payment amount matches the expected total.")
    def test_cash_amt_check(self):
        cash_amount = self.calc.cash_amount()
        self.total = self.calc.total_calculation()
        assert abs(cash_amount - self.total) <= 0.3

    @allure.story("Finalizing Card Payment")
    @allure.title("Complete Card Payment")
    @allure.description("Ensures that card payments can be successfully processed.")
    def test_cash_pay(self):
        assert self.calc.card_pay() == True
