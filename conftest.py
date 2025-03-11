import sys
import os
import pytest
import allure
from typing import Dict, Any
from appium import webdriver
from appium.options.common.base import AppiumOptions
from logic.dependencies import Dependencies

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from appium.webdriver.common.appiumby import AppiumBy

class AppiumDriver:
    def __init__(self):
        self.driver = None
        self.url = 'http://127.0.0.1:4723'
        self.caps: Dict[str, Any] = {
            "platformName": "Android",
            "appium:deviceName": "TS43223941452",
            "appium:automationName": "UiAutomator2",
            "appium:appPackage": "com.pays.pos",
            "appium:appActivity": ".ui.activities.MainActivity",
            "appium:noReset": True,
            "appium:fullReset": False,
            "appium:ensureWebviewsHavePages": True,
            "appium:nativeWebScreenshot": True,
            "appium:newCommandTimeout": 3600,
            "appium:connectHardwareKeyboard": True
        }

    def start_driver(self):
        """Initialize the Appium driver."""
        if self.driver is None:
            self.driver = webdriver.Remote(self.url, options=AppiumOptions().load_capabilities(self.caps))
        return self.driver

    def stop_driver(self):
        """Quit the Appium driver."""
        if self.driver:
            self.driver.quit()
            self.driver = None

@pytest.fixture(scope="session")
def appium_driver():
    """Session-scoped Appium driver fixture."""
    driver_instance = AppiumDriver()
    driver = driver_instance.start_driver()
    yield driver
    driver_instance.stop_driver()


@pytest.fixture(scope="session", autouse=True)
@allure.story("User Login & Authentication")
def login_once(appium_driver):
    """
    Perform login once before all tests and share the session.
    If login fails, it won't be considered a test failure.
    """
    deps = Dependencies(appium_driver)
    testLogin = deps.get_login()

    try:
        with allure.step("Performing User Login"):
            assert testLogin.login() is True, "Login failed."
        
        with allure.step("Entering Passcode"):
            assert testLogin.passcode() is True, "Passcode entry failed."

        allure.attach("✅ Login completed successfully before the test flow.", name="Login Info", attachment_type=allure.attachment_type.TEXT)
        print("✅ Login completed successfully before the test flow.")

    except Exception as e:
        pass


# ========================= Screenshot on Failure =========================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to detect if a test has failed and mark it for later use in fixtures."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)

@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request, appium_driver):
    """Captures a screenshot on test failure and attaches it to Allure report."""
    yield
    if request.node.rep_call.failed:
        screenshot_dir = "allure-report/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)  # Ensure the directory exists
        
        screenshot_path = os.path.join(screenshot_dir, f"{request.node.name}.png")
        appium_driver.get_screenshot_as_file(screenshot_path)  # Take screenshot
        
        allure.attach.file(screenshot_path, name=f"Screenshot_{request.node.name}", attachment_type=allure.attachment_type.PNG)
