import pytest
import allure
from logic.dependencies import Dependencies

total = None
tolerance = None
surcharge = None

@allure.epic("Orderflow")
@allure.feature("Takeout order in Cash")
class TestTakeoutFlow:
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        """Automatically inject the appium_driver fixture for every test."""
        self.driver = appium_driver
        self.deps = Dependencies(self.driver)
        self.calc = self.deps.get_calculations()
    

    @allure.story("Order Management")
    @allure.title("Select Takeout Order")
    def test_take_out_btn(self):
        assert self.calc.order("Take Out") == True
        print("Take out button clicked")

    @allure.story("Order Management")
    @allure.title("Add multiple items to the cart")
    def test_adding_items(self):
        print("\n===================Adding multiple Items===================\n")
        assert self.calc.add_multiple_items(3) == True
        print("\n==================Added Items Successfully==================\n")

    @allure.story("Order Modifications")
    @allure.title("Apply discount to the order")
    def test_add_discount(self):
        print("=======================Adding Discount=========================\n")
        assert self.calc.add_discount() == True
        print("=====================DISCOUNT ADDED SUCCESSFULLY====================\n")
        
    @allure.story("Order Modifications")
    @allure.title("Add a note to the order")
    def test_add_note(self):
        print("========================Adding Order Note=========================\n")
        assert self.calc.add_note() == True
        print("========================Order Note added==========================")

    @allure.story("Price Calculation")
    @allure.title("Validate cart calculations")
    def test_cart_calculations(self):
        print("=================Performing Cart Calculations=====================\n")
        global total, tolerance
        end_pay = self.calc.pay()
        tolerance = 0.3
        total = self.calc.total_calculation()
        print(f"Amount on Pay button is{end_pay}\n")
        assert abs(total - end_pay) <= tolerance, (f"Difference too high: {abs(total - end_pay)}")
        print(f"==================\n Card Calculation Test passed.=======================")

    @allure.story("Tips and Final Payment")
    @allure.title("Verify tip is applied correctly")
    def test_tip_added(self):
        print("================Adding Tip====================")
        global total, tolerance, tip
        tip = 0
        tip_percentage = self.calc.tip()
        amount_price = self.calc.cash_amount()
        cash_amount_check = (total) + (total * tip_percentage) / 100
        tip = ((total * tip_percentage) / 100)
        print("The Tip Added is ",tip)
        total = cash_amount_check
        assert abs(cash_amount_check - amount_price) <= tolerance, ("Tip calculation difference exceeds tolerance.")

    @allure.story("Payment Processing")
    @allure.title("Complete card payment")
    def test_final_pay(self):
        print("=================Cash Payment====================")
        assert self.calc.cash_pay() is True

    @allure.story("Payment Processing")
    @allure.title("Validate transaction details")
    def test_transaction(self):
        global total, tip
        transaction_amount = self.calc.transaction()
        print("Total price is ", total)
        print("Transaction amount is ", transaction_amount)
        assert abs(transaction_amount - total) <= 0.3  

    @allure.story("Order Type Validation")
    @allure.title("Ensure order type is TAKE OUT")
    def test_orderType(self):
        print("===================Checking is order is Take Out=======================")
        assert self.calc.isOrder("TAKE OUT") == True

    @allure.story("Refund Processing")
    @allure.title("Process a card refund")
    def test_refund(self):
        print("=====================Refunding=====================")
        refunded = self.calc.cash_refund()
        assert refunded == True

