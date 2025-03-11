import pytest
import allure
from loguru import logger
from logic.dependencies import Dependencies

# Configure Loguru to log messages to a file (optional)
logger.add("test_logs.log", format="{time} {level} {message}", level="INFO")

@allure.feature("Dining POS System")
class TestCashLog:
    
    @pytest.fixture(autouse=True)
    def setup_driver(self, appium_driver):
        self.driver = appium_driver
        self.deps = Dependencies(self.driver)
        logger.info("Driver initialized for the test.")


    @allure.story("Cash Log Operations")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cash_log_only(self):
        logger.info("Starting Cash Log Test")
        self.cash_log = self.deps.get_cash_log()
        
        with allure.step("Navigating to Cash Log"):
            self.cash_log.check_cash_log_amt()
            logger.info("Checked cash log successfully.")

        with allure.step("Verifying ordering in cash log"):
            result = self.cash_log.ordering()
            logger.info(f"Ordering validation result: {result}")
            assert result == True, "Ordering validation failed."

    @allure.story("Refund in Cash Log")
    @allure.severity(allure.severity_level.NORMAL)
    def test_refund_cash_log(self):
        logger.info("Starting Refund Test in Cash Log")
        self.cash_log = self.deps.get_cash_log()
        
        with allure.step("Navigating to Cash Log"):
            self.cash_log.check_cash_log_amt()

        with allure.step("Verifying refund operation"):
            result = self.cash_log.ordering("refund")
            logger.info(f"Refund validation result: {result}")
            assert result == True, "Refund validation failed."

    @allure.story("Tip in Cash Log")
    @allure.severity(allure.severity_level.MINOR)
    def test_tip_cash_log(self):
        logger.info("Starting Tip Test in Cash Log")
        self.cash_log = self.deps.get_cash_log()
        
        with allure.step("Navigating to Cash Log"):
            self.cash_log.check_cash_log_amt()

        with allure.step("Verifying tip operation"):
            result = self.cash_log.ordering("tip")
            logger.info(f"Tip validation result: {result}")
            assert result == True, "Tip validation failed."
