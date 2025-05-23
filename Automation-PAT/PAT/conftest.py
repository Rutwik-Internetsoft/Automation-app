# import sys
# import os
# import pytest
# import allure
# from typing import Dict, Any
# from appium import webdriver
# from appium.options.common.base import AppiumOptions
# from appium.webdriver.appium_service import AppiumService
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# if project_root not in sys.path:
#     sys.path.insert(0, project_root)


# # ========================= Appium =========================


# class AppiumDriver:
#     def __init__(self):
#         self.appium_service = AppiumService()
#         self.appium_service.start()
#         self.driver = None
#         self.url = "http://192.168.56.1:4723"        
#         self.caps: Dict[str, Any] ={
# 	"platformName": "Android",
# 	"appium:automationName": "UiAutomator2",
# 	"appium:appPackage": "com.internetsoft.pax",
# 	"appium:appActivity": ".payattable.ui.activities.MainActivity",
# 	"appium:noReset": True,
# 	"appium:fullReset": False,
# 	"appium:ensureWebviewsHavePages": True,
# 	"appium:nativeWebScreenshot": True,
# 	"appium:newCommandTimeout": 3600,
# 	"appium:connectHardwareKeyboard": True
# }

#     def start_driver(self):
#         """Initialize the Appium driver."""
#         if self.driver is None:
#             self.driver = webdriver.Remote(self.url, options=AppiumOptions().load_capabilities(self.caps))
#         return self.driver

#     def stop_driver(self):
#         """Quit the Appium driver."""
#         if self.driver:
#             self.driver.quit()
#             self.driver = None
#         """Stop the Appium server."""
#         if self.appium_service.is_running:
#             self.appium_service.stop()


# # ========================= Appium Driver Instance =========================


# @pytest.fixture(scope="session")
# def appium_driver():
#     """Session-scoped Appium driver fixture."""
#     driver_instance = AppiumDriver()
#     driver = driver_instance.start_driver()
#     yield driver
#     driver_instance.stop_driver()


# # # ========================= Screenshot on Failure =========================
# # @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# # def pytest_runtest_makereport(item, call):
# #     """Hook to detect if a test has failed and restart MainActivity if necessary."""
# #     outcome = yield
# #     report = outcome.get_result()
# #     setattr(item, "rep_" + report.when, report)


# # # ========================= Login Pluggin =========================



# # @pytest.fixture(autouse=True)
# # def capture_screenshot_on_failure(request, appium_driver):
# #     """Captures a screenshot on test failure and attaches it to Allure report."""
# #     yield
# #     if request.node.rep_call.failed:
# #         screenshot_dir = "Automation-logic/allure-report/screenshots"
# #         os.makedirs(screenshot_dir, exist_ok=True)  # Ensure the directory exists
        
# #         screenshot_path = os.path.join(screenshot_dir, f"{request.node.name}.png")
# #         appium_driver.get_screenshot_as_file(screenshot_path)  # Take screenshot
        
# #         allure.attach.file(screenshot_path, name=f"Screenshot_{request.node.name}", attachment_type=allure.attachment_type.PNG)

# # def pytest_configure(config):
# #     """Automatically set Allure results directory without requiring --alluredir."""
# #     allure_results_dir = "Automation-logic/allure-results"
# #     os.makedirs(allure_results_dir, exist_ok=True)  # Ensure the directory exists
# #     config.option.allure_report_dir = allure_results_dir

