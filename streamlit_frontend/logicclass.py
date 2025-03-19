import streamlit as st
import subprocess
import yaml,time,webbrowser

class LogicOfApp:
    def __init__(self, yaml_path="streamlit_frontend/test_cases.yaml"):
        """Initialize state and load test cases from YAML."""
        if "page" not in st.session_state:
            st.session_state.page = "home"

        self.yaml_path = yaml_path
        self.test_cases = self.load_yaml()

    def load_yaml(self):
        """Load test cases from YAML file."""
        try:
            with open(self.yaml_path, "r", encoding='utf-8') as file:
                data = yaml.safe_load(file)
                return data
        except Exception as e:
            st.error(f"Error loading YAML: {e}")
            return {}

    def order_selection(self, order_type):
        ORDER_TYPES = {
        "phoneorder": {"name": "Phone Order", "methods": ["cash", "card"]},
        "takeoutorder": {"name": "Takeout Order", "methods": ["cash", "card"]},
        "dineinorder": {"name": "Dine-in Order", "methods": ["cash", "card"]},
        "openorder": {"name": "Open Order", "methods": ["cash", "card"]},
        "stayorder": {"name": "Stay Order", "methods": ["cash","card"]}}
        
        
        
        """Dynamically generate payment method selection for any order type."""
        
        st.subheader(f"Select Payment Method for {ORDER_TYPES[order_type]['name']}")

        # 🔹 Generate buttons for cash/card dynamically
        for method in ORDER_TYPES[order_type]["methods"]:
            key = f"test_{order_type}_{method}"  # e.g., "test_phone_order_cash"
            label = f"💵 {method.capitalize()} Payment" if method == "cash" else f"💳 {method.capitalize()} Payment"
            
            if st.button(label, key=key):
                st.session_state.page = key  # Set session state for execution
                st.rerun()

        # 🔙 Back Button
        if st.button("🔙 Back", key=f"back_{order_type}"):
            st.session_state.page = "home"
            st.rerun()

   
    def test_execution(self, order_type):
        """Render test execution UI for a specific phone order type using YAML."""

        st.subheader(f"🛠 {order_type.replace('_', ' ').title()} - Test Execution")

        test_data = self.test_cases.get(order_type)
        if not test_data:
            st.error(f"⚠️ Invalid test order type or missing YAML data! Order Type: {order_type}")
            return

        test_path = test_data["full_test_path"]

        # Run Full Test Suite
        run_full_test = st.button("▶ Run Full Test Suite", key=f"full test {order_type}")
        if run_full_test:
            st.write(f"Running Full Test Suite: {test_path}")  # Debugging Output
            st.session_state.run_command = ["pytest", test_path, "-s"]
            st.session_state.run_test_now = True  # Trigger execution

        # Run Individual Test Cases
        st.write("### Run Individual Test Cases")
        for case in test_data.get("cases", []):
            case_name = case["name"]
            case_function = case["function"]

            if st.button(case_name, key=case_function):
                st.session_state.run_command = ["pytest", test_path, "-k", case_function, "-s"]
                st.session_state.run_test_now = True  # Trigger execution

        # Back Button
        back_clicked = st.button("🔙 Back", key=f"back_{order_type}")
        if back_clicked:
            st.write("Navigating back to phone_order")  # Debugging Output
            st.session_state.page = "home"
            st.rerun()

        # Ensure the output box is **always** at the bottom
        st.write("---")  # Just for UI separation
        st.subheader("📜 Execution Output")
        
        output_box = st.empty()  # Placeholder for execution output

        def run_test_and_capture_output(command):
            """Execute a subprocess and capture real-time output."""
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            output_text = ""
            for line in iter(process.stdout.readline, ''):
                output_text += line
                output_box.text_area("📜 Execution Logs", output_text, height=300)

            stderr_output = process.stderr.read()
            if stderr_output:
                output_text += "\n❌ ERROR:\n" + stderr_output
                output_box.text_area("📜 Execution Logs", output_text, height=300)

            process.wait()


        # Execute the test only if a button was clicked
        if st.session_state.get("run_test_now", False):
            run_test_and_capture_output(st.session_state.run_command)
            st.session_state.run_test_now = False  # Reset flag
