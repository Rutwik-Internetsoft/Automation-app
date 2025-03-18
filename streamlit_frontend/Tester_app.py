import streamlit as st
import subprocess
from logicclass import LogicOfApp
import os, sys

# Ensure the project root is in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 🔹 Define ORDER TYPES and PAYMENT METHODS
ORDER_TYPES = {
    "phoneorder": {"name": "Phone Order", "methods": ["cash", "card"]},
    "takeoutorder": {"name": "Takeout Order", "methods": ["cash", "card"]},
    "dineinorder": {"name": "Dine-in Order", "methods": ["cash", "card"]},
    "openorder": {"name": "Open Order", "methods": ["cash", "card"]},
    "stayorder": {"name": "Stay Order", "methods": ["cash", "card"]}
}

# List of available devices
DEVICES = {
    "Device 1": "192.168.0.248:5555",
    "Device 2": "192.168.0.208:5555",
    "Device 3": "192.168.0.78:5555",
    "Device 4": "192.168.0.142:5555"
}
# Function to connect to a device using ADB
def connect_to_device(device_name):
    """Runs adb connect with the selected device's IP"""
    ip_address = DEVICES[device_name]
    os.system(f"adb connect {ip_address}")
    st.success(f"Connected to {device_name} ({ip_address})")

def main():
    st.title("Test Execution Dashboard")
    app = LogicOfApp()

    # Device Selection
    st.sidebar.subheader("🔌 Device Connection")
    selected_device = st.selectbox("Select a Device:", list(DEVICES.keys()))

    if st.sidebar.button("Connect to Device"):
        output = connect_to_device(selected_device)
        st.sidebar.text(output)

    # Show connected devices
    st.sidebar.subheader("📱 Connected Devices")
    device_list = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
    st.sidebar.text(device_list.stdout)

    # Order Selection
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        st.subheader("Orders")
        for order_type, details in ORDER_TYPES.items():
            if st.button(f"📦 {details['name']}"):
                st.session_state.page = order_type
                st.rerun()

    elif st.session_state.page in ORDER_TYPES:
        app.order_selection(st.session_state.page)

    elif st.session_state.page.startswith("test_"):
        app.test_execution(st.session_state.page)

if __name__ == "__main__":
    main()
