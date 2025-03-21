import sys
import os
import pytest
import allure
from typing import Dict, Any
from appium import webdriver
from appium.options.common.base import AppiumOptions
import subprocess

from appium.webdriver.common.appiumby import AppiumBy
import time
from logic.dependencies import Dependencies
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


# ========================= Appium =========================


class AppiumDriver:
    def __init__(self):
        self.driver = None
        self.url = "http://192.168.56.1:4723"
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
            "appium:connectHardwareKeyboard": True,
            "allowInsecure": ["adb_shell"]

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


# ========================= Appium Driver Instance =========================

@pytest.fixture(scope="session")
def appium_driver():
    """Session-scoped Appium driver fixture."""
    driver_instance = AppiumDriver()
    driver = driver_instance.start_driver()
    yield driver
    driver_instance.stop_driver()


# ========================= Screenshot on Failure =========================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to detect if a test has failed and restart MainActivity if necessary."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


# ========================= Login Pluggin =========================

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
            time.sleep(2)
            assert testLogin.passcode() is True, "Passcode entry failed."

        allure.attach("✅ Login completed successfully before the test flow.", name="Login Info", attachment_type=allure.attachment_type.TEXT)
        print("✅ Login completed successfully before the test flow.")

    except Exception as e:
        pass

@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request, appium_driver):
    """Captures a screenshot on test failure and attaches it to Allure report."""
    yield
    if request.node.rep_call.failed:
        screenshot_dir = "Automation-logic/allure-report/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)  # Ensure the directory exists
        
        screenshot_path = os.path.join(screenshot_dir, f"{request.node.name}.png")
        appium_driver.get_screenshot_as_file(screenshot_path)  # Take screenshot
        
        allure.attach.file(screenshot_path, name=f"Screenshot_{request.node.name}", attachment_type=allure.attachment_type.PNG)

def pytest_configure(config):
    """Automatically set Allure results directory without requiring --alluredir."""
    allure_results_dir = "Automation-logic/allure-results"
    os.makedirs(allure_results_dir, exist_ok=True)  # Ensure the directory exists
    config.option.allure_report_dir = allure_results_dir



@pytest.fixture(scope="function", autouse=True)
def capture_android_crash_logs(request):
    """Captures Android crash logs after each test and attaches to Allure if a crash is detected."""

    device_id = "emulator-5554"  # Update based on your connected device/emulator

    def get_crash_logs():
        """Extract logs related to crashes from Android logcat."""
        try:
            logcat_output = subprocess.run(
                ["adb", "-s", device_id, "logcat", "-d"],
                capture_output=True, text=True
            )
            logs = logcat_output.stdout
            return logs if logs else "No logs captured."
        except Exception as e:
            return f"Error while fetching logs: {str(e)}"

    yield  # Run the test first

    # After test execution, check for crashes
    logs = get_crash_logs()

    if logs and ("FATAL EXCEPTION" in logs or "ANR in" in logs):  # Ensure logs is not None
        allure.attach(logs, name="Android Crash Logs", attachment_type=allure.attachment_type.TEXT)
