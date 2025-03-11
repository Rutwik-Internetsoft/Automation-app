import pytest
import allure
from logic.dependencies import Dependencies

total = None
tolerance = None
surcharge = None

@allure.feature("Open Order Flow")
@allure.label("App", "POS System")
@allure.label("OS", "Android")
class TestOpenOrderCard:
    
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        """Automatically inject the appium_driver fixture for every test."""
        self.driver = appium_driver
        self.deps = Dependencies(self.driver)
        self.calc = self.deps.get_calculations()
        
    @allure.story("Device Connection")
    @allure.title("Connect PAX Payment Terminal")
    def test_pax_connection(self):
        with allure.step("Connecting to PAX Terminal"):
            assert self.calc.connect_PAX() == True
        allure.attach("PAX Connected Successfully", name="Connection Log")

    @allure.story("Order Management")
    @allure.title("Select Open Order")
    def test_take_out_btn(self):
        with allure.step("Selecting Open Order"):
            assert self.calc.order("Open Order") == True

    @allure.story("Order Management")
    @allure.title("Add multiple items to the cart")
    def test_adding_items(self):
        with allure.step("Adding multiple items"):
            assert self.calc.add_multiple_items(3) == True

    @allure.story("Order Modifications")
    @allure.title("Apply discount to the order")
    def test_add_discount(self):
        with allure.step("Applying discount"):
            assert self.calc.add_discount() == True

    @allure.story("Order Modifications")
    @allure.title("Add a note to the order")
    def test_add_note(self):
        with allure.step("Adding a note"):
            assert self.calc.add_note() == True

    @allure.story("Manual Item Management")
    @allure.title("Add a Manual Item and Set Quantity")
    @allure.description("Tests if a manual item can be added with a specified quantity.")
    def test_manual_item_and_qty(self):
        with allure.step("Adding a manual item"):
            assert self.calc.manual_item() == True

    @allure.story("Item Quantity Update")
    @allure.title("Update Item Quantity")
    @allure.description("Ensures that the quantity of an existing item can be updated.")
    def test_updating_item(self):
        with allure.step("Updating item quantity"):
            assert self.calc.update_item_quantity() == True

    @allure.story("Price Calculation")
    @allure.title("Validate cart calculations")
    def test_cart_calculations(self):
        global total, tolerance
        with allure.step("Calculating total price"):
            end_pay = self.calc.pay()
            tolerance = 0.5
            total = self.calc.total_calculation()
        allure.attach(f"Expected Total: {total}, Actual Payment: {end_pay}", name="Calculation Log")
        assert abs(total - end_pay) <= tolerance, f"Difference too high: {abs(total - end_pay)}"

    @allure.story("Price Calculation")
    @allure.title("Verify surcharge is applied correctly")
    def test_card_price_hike(self):
        global total, tolerance, surcharge
        with allure.step("Calculating surcharge"):
            surcharge_percentage = self.calc.surcharge_percentage()
            surcharge = ((total * surcharge_percentage) / 100)
            amount_price = self.calc.card_amount()
        allure.attach(f"Surcharge: {surcharge}, Expected Price: {total + surcharge}, Actual Price: {amount_price}", name="Surcharge Log")
        assert abs((total + surcharge) - amount_price) <= tolerance, "Price hike difference exceeds tolerance."

    @allure.story("Tips and Final Payment")
    @allure.title("Verify tip is applied correctly")
    def test_tip_added(self):
        global total, surcharge, tolerance
        with allure.step("Applying tip to order"):
            tip_percentage = self.calc.tip()
            amount_price = self.calc.card_amount()
            card_amount_check = (total + surcharge) + ((total + surcharge) * tip_percentage) / 100
            total = card_amount_check
        allure.attach(f"Tip: {tip_percentage}%, Expected Price: {card_amount_check}, Actual Price: {amount_price}", name="Tip Calculation Log")
        assert abs(card_amount_check - amount_price) <= tolerance, "Tip calculation difference exceeds tolerance."

    @allure.story("Payment Processing")
    @allure.title("Complete card payment")
    def test_final_pay(self):
        with allure.step("Processing final payment"):
            card = self.calc.card_pay()
        allure.attach("Card Payment Successful", name="Payment Log")
        assert card == True

    @allure.story("Payment Processing")
    @allure.title("Validate transaction details")
    def test_transaction(self):
        global total
        with allure.step("Verifying transaction amount"):
            transaction_amount = self.calc.transaction()
        allure.attach(f"Total price: {total}, Transaction Amount: {transaction_amount}", name="Transaction Log")
        assert abs(transaction_amount - total) <= 0.5

    @allure.story("Order Type Validation")
    @allure.title("Ensure order type is TAKE OUT")
    def test_orderType(self):
        with allure.step("Validating order type"):
            assert self.calc.isOrder("OPEN ORDER") == True

    @allure.story("Refund Processing")
    @allure.title("Process a card refund")
    def test_refund(self):
        with allure.step("Processing refund"):
            refunded = self.calc.card_refund()
        allure.attach("Refund Processed Successfully", name="Refund Log")
        assert refunded == True
