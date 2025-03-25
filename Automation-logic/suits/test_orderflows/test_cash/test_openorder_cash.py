import pytest
import allure
import os
from logic.dependencies import Dependencies

# Global variables for price validation
total = None
tolerance = None

@allure.epic("Orderflow")
@allure.feature("Open order in Cash")
class TestOpenOrderCash:
    
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        """Injects the Appium driver for every test."""
        self.driver = appium_driver
        self.deps = Dependencies(self.driver)
        self.calc = self.deps.get_calculations()

    @allure.story("Order Creation")
    @allure.title("Select 'Open Order' for Cash Payment")
    @allure.description("Verifies that the user can successfully select the 'Open Order' option in POS.")
    def test_openorder_btn(self):
        with allure.step("Selecting 'Open Order' from Order Types"):
            result = self.calc.order("Open Order")
            allure.attach(f"Order Type Selection Result: {result}", name="Order Selection Status", attachment_type=allure.attachment_type.TEXT)
            assert result, "Failed to select 'Open Order'"
        print("✅ Open Order button clicked successfully.")

    @allure.story("Cart Management")
    @allure.title("Add Multiple Items to the Cart")
    @allure.description("Ensures multiple items can be successfully added to the cart.")
    def test_adding_items(self):
        with allure.step("Adding 3 items to the cart"):
            result = self.calc.add_multiple_items(3)
            allure.attach(f"Items Added: {result}", name="Cart Update", attachment_type=allure.attachment_type.TEXT)
            assert result, "Failed to add multiple items"
        print("✅ Items added successfully.")


    @allure.story("Order Modifications")
    @allure.title("Add a Note to the Order")
    @allure.description("Verifies that a note can be added to an order successfully.")
    def test_add_note(self):
        with allure.step("Adding a note to the order"):
            assert self.calc.add_note(), "Failed to add note"
        print("✅ Note added successfully.")

    @allure.story("Manual Item Management")
    @allure.title("Add a Manual Item with Specified Quantity")
    @allure.description("Tests if a manual item can be added to the cart with a specified quantity.")
    def test_manual_item_and_qty(self):
        with allure.step("Adding a manual item with quantity"):
            assert self.calc.manual_item(), "Failed to add a manual item"
        print("✅ Manual item added successfully.")

    @allure.story("Item Quantity Management")
    @allure.title("Update Quantity of an Item in the Cart")
    @allure.description("Ensures the quantity of an existing item can be updated successfully.")
    def test_updating_item(self):
        with allure.step("Updating item quantity in the cart"):
            assert self.calc.update_item_quantity(), "Failed to update item quantity"
        print("✅ Item quantity updated successfully.")

    @allure.story("Order Modifications")
    @allure.title("Apply Discount to the Order")
    @allure.description("Validates that a discount can be applied to an order.")
    def test_add_discount(self):
        with allure.step("Applying discount to the order"):
            before_discount_subtotal = self.calc.sub_total()
            result = self.calc.add_discount()
            added_discount = self.calc.discount()
            after_discount_subtotal = self.calc.sub_total()
            if abs((before_discount_subtotal - added_discount) - after_discount_subtotal)<=0.3:
                assert True
            allure.attach(f"Sub Total Before Discount: {before_discount_subtotal} and subtotal after Discount: {after_discount_subtotal}", name="Subtotal",attachment_type=allure.attachment_type.TEXT)
            
            allure.attach(f"Discount Applied: {added_discount}", name="Discount Applied", attachment_type=allure.attachment_type.TEXT)
            assert result, "Failed to apply discount"
        print("✅ Discount applied successfully.")


    @allure.story("Billing & Price Calculation")
    @allure.title("Validate Total Price Calculation in Cart")
    @allure.description("Ensures the total price of the cart items is calculated accurately before payment.")
    def test_cart_calculations(self):
        global total, tolerance
        tolerance = 0.3

        with allure.step("Capturing screenshot before checking price calculation"):
            screenshot_dir = "Automation-logic/allure-report/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)  # Ensure directory exists
            screenshot_path = os.path.join(screenshot_dir, "before_pay.png")
            self.driver.get_screenshot_as_file(screenshot_path)
            allure.attach.file(screenshot_path, name="Before Pay Button", attachment_type=allure.attachment_type.PNG)

        with allure.step("Fetching amount displayed on Pay button"):
            end_pay = self.calc.pay()
            allure.attach(f"Pay Button Amount: {end_pay}", name="Displayed Pay Amount", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Performing total price calculation"):
            total = self.calc.total_calculation()
            allure.attach(f"Calculated Total: {total}", name="Computed Total", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Validating displayed and calculated totals"):
            assert abs(total - end_pay) <= tolerance, f"Price mismatch! Expected {total}, but Pay button shows {end_pay}"
            allure.attach("Total Price Validation Passed ✅", name="Validation Status", attachment_type=allure.attachment_type.TEXT)

        print("✅ Total price calculation passed.")

    @allure.story("Payment Processing")
    @allure.title("Complete Cash Payment Transaction")
    @allure.description("Validates that a cash payment can be completed successfully.")
    def test_final_pay(self):
        with allure.step("Processing cash payment"):
            result = self.calc.cash_pay()
            allure.attach(f"Payment Successful: {result}", name="Payment Status", attachment_type=allure.attachment_type.TEXT)
            assert result, "Failed to complete cash payment"
        print("✅ Cash payment processed successfully.")

    @allure.story("Payment Processing")
    @allure.title("Validate Transaction Amount After Payment")
    @allure.description("Ensures the recorded transaction amount matches the expected total.")
    def test_transaction(self):
        global total
        with allure.step("Fetching transaction amount from POS"):
            transaction_amount = self.calc.transaction()
            allure.attach(f"Transaction Amount: {transaction_amount}", name="Transaction Amount", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Validating transaction amount against expected total"):
            print(f"Expected Total: {total}, Transaction Amount: {transaction_amount}")
            assert abs(transaction_amount - total) <= 0.5, "Transaction amount mismatch"
            allure.attach("Transaction Validation Passed ✅", name="Validation Status", attachment_type=allure.attachment_type.TEXT)

        print("✅ Transaction amount validated successfully.")

    @allure.story("Refund Processing")
    @allure.title("Process a Cash Item-Wise Refund")
    @allure.description("Ensures that an item-wise refund is processed successfully for a cash order.")
    def test_refund(self):
        with allure.step("Processing item-wise refund for cash payment"):
            result = self.calc.cash_itemwise_refund()
            allure.attach(f"Refund Status: {result}", name="Refund Result", attachment_type=allure.attachment_type.TEXT)
            assert result, "Failed to process refund"
        print("✅ Item-wise refund processed successfully.")
