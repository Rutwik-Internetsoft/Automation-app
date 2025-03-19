import yaml
from appium.webdriver.common.appiumby import AppiumBy

class LocatorLoader:
    def __init__(self, locator_file: str, default_section: str = "common"):
        """
        :param locator_file: Path to the YAML file containing locators.
        :param default_section: Default section if none is specified.
        """
        self.locator_file = locator_file
        self.default_section = default_section
        self.locators = self.load_locators()

    def load_locators(self) -> dict:
        """Load locator definitions from the YAML file."""
        try:
            with open(self.locator_file, "r") as stream:
                return yaml.safe_load(stream) or {}
        except yaml.YAMLError as exc:
            print(f"Error loading YAML: {exc}")
            return {}
        except FileNotFoundError as exc:
            print(f"Locator file not found: {exc}")
            return {}
        
    def get_locator(self, key: str, section: str = None, **kwargs):
        
        """
        Retrieve a locator.
        - `section` is optional; defaults to the pre-configured default section.
        - If the key is missing in the given section, it falls back to the default section.
        - If the locator requires formatting, pass the required `kwargs`.
        """
        section = section or self.default_section  # Use default if not provided
        section_data = self.locators.get(section, {})

        # If key is not found in the section, fall back to the default section
        locator_info = section_data.get(key)
        if not locator_info and section != self.default_section:
            print(f"Warning: Locator '{key}' not found in section '{section}', trying '{self.default_section}'")
            locator_info = self.locators.get(self.default_section, {}).get(key)

        if locator_info:
            by_key = locator_info.get("by")
            locator_str = locator_info.get("locator")

            # Format locator string if placeholders exist
            if kwargs:
                locator_str = locator_str.format(*kwargs.values())

            mapping = {
                "id": AppiumBy.ID,
                "xpath": AppiumBy.XPATH,
                "accessibility_id": AppiumBy.ACCESSIBILITY_ID,
                "android_uiautomator": AppiumBy.ANDROID_UIAUTOMATOR
            }
            return mapping.get(by_key, by_key), locator_str

        raise ValueError(f"Locator '{key}' not found in section '{section}' or fallback section '{self.default_section}'.")

class Locators(LocatorLoader):
    
    def __init__(self):
        locator_file="Automation-logic/logic/locators.yaml"
        self.locator_loader = LocatorLoader(locator_file=locator_file)
    
    def get_locator(self, key, section, **kwargs):
        return self.locator_loader.get_locator(key, section, **kwargs)

    def PAT(self):
        self.email_login = self.locator_loader.get_locator("email_login","PAT")
        self.password_login = self.locator_loader.get_locator("password_login","PAT")
        self.login_PAT = self.locator_loader.get_locator("login","PAT")
        self.passcode = self.locator_loader.get_locator("passcode","PAT")
        self.main_page = self.locator_loader.get_locator("main_page","PAT")
        self.add_table = self.locator_loader.get_locator("add_table","PAT")
        self.add_table_2 = self.locator_loader.get_locator("add_table_2","PAT")
        self.continue_btn = self.locator_loader.get_locator("continue_btn","PAT")

        
        