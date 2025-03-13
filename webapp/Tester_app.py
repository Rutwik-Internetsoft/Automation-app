import streamlit as st
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
    "stayorder": {"name": "Stay Order", "methods": ["cash","card"]}
}

def main():
    st.title("Test Execution Dashboard")
    app = LogicOfApp()

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
