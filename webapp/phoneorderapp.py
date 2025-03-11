import streamlit as st
import subprocess
import yaml

class PhoneOrderApp:
    def __init__(self, yaml_path="webapp/test_cases.yaml"):
        """Initialize state and load test cases from YAML."""
        if "page" not in st.session_state:
            st.session_state.page = "home"

        self.yaml_path = yaml_path
        self.test_cases = self.load_yaml()

    def load_yaml(self):
        """Load test cases from YAML file."""
        try:
            with open(self.yaml_path, "r", encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            st.error(f"Error loading YAML: {e}")
            return {}

    def run_test(self, test_path, test_function=None):
        """Run a pytest test suite or a specific test function."""
        try:
            command = ["pytest", test_path, "--alluredir=allure-results"]
            if test_function:
                command.insert(1, "-k")
                command.insert(2, test_function)
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                st.success("✅ Test execution completed successfully!")
            else:
                st.error(f"❌ Test execution failed! \n\n {result.stderr}")
            
        except Exception as e:
            st.error(f"Error executing test: {e}")

    def phone_order(self):
        """Phone Order test execution UI."""
        st.subheader("Select Order Type")

        order_types = {"test_phoneorder_cash": "💵 Phone Order Cash", 
                       "test_phoneorder_card": "💳 Phone Order Card"}

        for key, label in order_types.items():
            if st.button(label, key=key):
                st.session_state.page = key
                st.rerun()

        if st.button("🔙 Back", key="back_home"):
            st.session_state.page = "home"
            st.rerun()

    def phone_order_test_execution(self, order_type):
        """Render test execution UI for a specific phone order type using YAML."""
                
        st.subheader(f"🛠 {order_type.replace('_', ' ').title()} - Test Execution")

        test_data = self.test_cases.get(order_type)
        if not test_data:
            st.error("⚠️ Invalid test order type or missing YAML data!")
            return

        # Debugging: Print test data to check YAML loading

        test_path = test_data["full_test_path"]

        # Run Full Test Suite
        run_full_test = st.button("▶ Run Full Test Suite", key=f"full_test_{order_type}")
        if run_full_test:
            st.write(f"Running Full Test Suite: {test_path}")  # Debugging Output
            self.run_test(test_path)

        # Run Individual Test Cases
        st.write("### Run Individual Test Cases")
        for case in test_data.get("cases", []):
            run_case = st.button(case["name"], key=case["function"])
            if run_case:
                st.write(f"Running Test: {case['function']} from {test_path}")  # Debugging Output
                self.run_test(test_path, case["function"])

        # Back Button
        back_clicked = st.button("🔙 Back", key=f"back_{order_type}")
        if back_clicked:
            st.write("Navigating back to phone_order")  # Debugging Output
            st.session_state.page = "phone_order"
            st.rerun()
