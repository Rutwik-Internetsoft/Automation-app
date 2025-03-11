import pytest
import allure
from logic.dependencies import Dependencies

total = None
tolerance = None

@allure.feature("Open Order Flow - Cash Payment")
@allure.label("Module", "Order Management")
@allure.label("Type", "Functional Test")
class TestOpenOrderCash:
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        """Automatically inject the appium_driver fixture for every test."""
        self.driver = appium_driver
        self.deps = Dependencies(self.driver)
        self.calc = self.deps.get_calculations()

    @allure.story("Order Creation")
    @allure.title("Select 'Open Order' for Cash Payment")
    @allure.description("Verifies that the user can successfully select the 'Open Order' option in POS.")
    def test_take_out_btn(self):
        assert self.calc.order("Open Order") == True
        print("Take out button clicked")

    @allure.story("Cart Management")
    @allure.title("Add Multiple Items to the Cart")
    @allure.description("Ensures multiple items can be successfully added to the cart.")
    def test_adding_items(self):
        assert self.calc.add_multiple_items(3) == True
        print("Added Items Successfully")

    @allure.story("Order Modifications")
    @allure.title("Apply Discount to the Order")
    @allure.description("Validates that a discount can be applied to an order.")
    def test_add_discount(self):
        assert self.calc.add_discount() == True
        print("DISCOUNT ADDED SUCCESSFULLY")

    @allure.story("Order Modifications")
    @allure.title("Add a Note to the Order")
    @allure.description("Verifies that a note can be added to an order successfully.")
    def test_add_note(self):
        assert self.calc.add_note() == True

    @allure.story("Manual Item Management")
    @allure.title("Add a Manual Item with Specified Quantity")
    @allure.description("Tests if a manual item can be added to the cart with a specified quantity.")
    def test_manual_item_and_qty(self):
        assert self.calc.manual_item() is True
        
    @allure.story("Item Quantity Management")
    @allure.title("Update Quantity of an Item in the Cart")
    @allure.description("Ensures the quantity of an existing item can be updated successfully.")
    def test_updating_item(self):
        assert self.calc.update_item_quantity() == True

    @allure.story("Billing & Price Calculation")
    @allure.title("Validate Total Price Calculation in Cart")
    @allure.description("Ensures the total price of the cart items is calculated accurately before payment.")
    def test_cart_calculations(self):
        global total, tolerance
        end_pay = self.calc.pay()
        tolerance = 0.5
        total = self.calc.total_calculation()
        print(end_pay, total)
        assert abs(total - end_pay) <= tolerance, (f"Difference too high: {abs(total - end_pay)}")
        print(f"Total Price {total}\nCash Calculation Test passed.")

    @allure.story("Tips & Additional Charges")
    @allure.title("Verify Tip Calculation for Cash Payments")
    @allure.description("Checks if the tip is applied correctly and the final total is accurate.")
    def test_tip_added(self):
        global total, tolerance
        tip_percentage = self.calc.tip()
        amount_price = self.calc.cash_amount()
        cash_amount_check = (total) + ((total) * tip_percentage) / 100
        total = cash_amount_check
        assert abs(cash_amount_check - amount_price) <= tolerance, ("Tip calculation difference exceeds tolerance.")

    @allure.story("Payment Processing")
    @allure.title("Complete Cash Payment Transaction")
    @allure.description("Validates that a cash payment can be completed successfully.")
    def test_final_pay(self):
        cash = self.calc.cash_pay()
        assert cash == True      

    @allure.story("Payment Processing")
    @allure.title("Validate Transaction Amount After Payment")
    @allure.description("Ensures the recorded transaction amount matches the expected total.")
    def test_transaction(self):
        global total
        transaction_amount = self.calc.transaction()
        print("Total price is ", total)
        print("Transaction amount is ", transaction_amount)
        assert abs(transaction_amount - total) <= 0.5

    @allure.story("Order Type Verification")
    @allure.title("Confirm Order Type is 'Open Order'")
    @allure.description("Verifies that the selected order type is correctly set to 'Open Order'.")
    def test_orderType(self):
        assert self.calc.isOrder("OPEN ORDER") == True

    @allure.story("Refund Processing")
    @allure.title("Process a Cash Item-Wise Refund")
    @allure.description("Ensures that an item-wise refund is processed successfully for a cash order.")
    def test_refund(self):
        refunded = self.calc.cash_itemwise_refund()
        assert refunded == True
