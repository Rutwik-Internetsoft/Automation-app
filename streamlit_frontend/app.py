import streamlit as st
import requests
import time
import urllib.parse

API_BASE_URL = "http://127.0.0.1:8000/" 
# Custom Styles
def apply_custom_styles():
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #1E1E1E;
        }
        .block-container {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
            font-size: 14px;
        }
        iframe {
            border: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

apply_custom_styles()
ORDER_TYPES = {
    "phoneorder": {"name": "Phone Order", "methods": ["cash", "card"]},
    "takeoutorder": {"name": "Takeout Order", "methods": ["cash", "card"]},
    "dineinorder": {"name": "Dine-in Order", "methods": ["cash", "card"]},
    "openorder": {"name": "Open Order", "methods": ["cash", "card"]},
    "stayorder": {"name": "Stay Order", "methods": ["cash", "card"]}
}
# Sidebar Navigation
st.sidebar.title("📊 Dashboard")
# Initialize session state if not set
if "page" not in st.session_state:
    st.session_state.page = "Run Sanity"
if "selected_order" not in st.session_state:
    st.session_state.selected_order = None
if "payment_methods" not in st.session_state:
    st.session_state.payment_methods = []
if "logs" not in st.session_state:
    st.session_state.logs = None

def set_page(page_name):
    st.session_state.page = page_name

st.sidebar.button("🚀 Run Sanity", use_container_width=True, on_click=set_page, args=("Run Sanity",))
st.sidebar.button("🐞 Bug Issues", use_container_width=True, on_click=set_page, args=("Bug Issues",))
st.sidebar.button("📜 Allure Report", use_container_width=True, on_click=set_page, args=("Allure Report",))

# Main Content
st.title(st.session_state.page)

# 👉 Run Sanity Tests Page
if st.session_state.page == "Run Sanity":
    

    suit = "Automation-logic/suits/test_orderflows/test_cash"
    encoded_suit = urllib.parse.quote(suit, safe="")


    if st.button("Run Cash Suit"):
        with st.empty():  # Placeholder for logs
            response = requests.get(f"{API_BASE_URL}/run-test/{encoded_suit}")

            logs = ""
            for chunk in response.iter_content(chunk_size=1024):
                logs += chunk.decode()
                st.text_area("📜 Execution Logs", logs, height=300)
        
    
    # Step 1: Select Order Type
    if not st.session_state.selected_order:
        st.subheader("Orders")
        
        for order_type in ["phoneorder", "takeoutorder", "dineinorder", "openorder", "stayorder"]:
            if st.button(f"📦 {order_type.replace('order', ' Order').title()}"):
                response = requests.get(f"{API_BASE_URL}/order-selection/{order_type}")
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.selected_order = order_type
                    st.session_state.payment_methods = data["payment_methods"]
                    st.rerun()  # Refresh UI to show payment options

    # Step 2: Show Payment Methods (After Order Selection)
    else:
        st.subheader(f"Select Payment Method for {st.session_state.selected_order.replace('order', ' Order').title()}")

        for method in st.session_state.payment_methods:
            key = f"test_{st.session_state.selected_order}_{method}"
            label = f"💵 {method.capitalize()} Payment" if method == "cash" else f"💳 {method.capitalize()} Payment"
            
            if st.button(label, key=key):
                st.session_state.selected_payment = method
                st.session_state.page = "test_execution"
                st.rerun()

        # Back Button to Order Selection
        if st.button("🔙 Back"):
            st.session_state.selected_order = None  # Reset order selection
            st.session_state.payment_methods = []
            st.session_state.page = "Run Sanity"
            st.rerun()

elif st.session_state.page == "test_execution":
    order_type = st.session_state.selected_order
    payment_method = st.session_state.selected_payment
    
    full_suit_runner = f"test_{order_type}_{payment_method}"
    

    # Run Full Test Suite
    if st.button("▶ Run Full Test Suite"):
        response = requests.get(f"{API_BASE_URL}/run-test/{full_suit_runner}")
        if response.status_code == 200:
            st.session_state.logs = response.json()["logs"]
        else:
            st.session_state.logs = "❌ Failed to execute full test suite!"
    

    response = requests.get(f"{API_BASE_URL}/individual_test_case/{full_suit_runner}")
    if response.status_code == 200:
        data = response.json()
        for case in data:
            case_name = case["name"]
            case_function = case["function"]

            if st.button(case_name, key=case_function):
                response = requests.get(f"{API_BASE_URL}/run-test/{full_suit_runner}/{case_function}")
                if response.status_code == 200:
                    st.session_state.logs = response.json()["logs"]
                else:
                    st.session_state.logs = f"❌ Failed to execute {case_function} Retry!"
    

    if st.button("🔙 Back"):
        st.session_state.page = "Run Sanity"
        st.rerun()

    # Execution Logs
    st.write("---")
    st.subheader("📜 Execution Output")
    st.text_area("Logs", st.session_state.logs, height=300)   
         
# 👉 Bug Tracking & Test Execution Page
elif st.session_state.page == "Bug Issues":
    st.subheader("Bug Tracking and Issues")
    st.write("🔍 View, report, and track bugs here.")

    # Bug List (Table)
    bugs = [
        {"code": "BUG101", "desc": "PAX terminal connection issue"},
        {"code": "BUG102", "desc": "Takeout order button not working"},
        {"code": "BUG103", "desc": "Adding multiple items to cart fails"}
    ]

    # Run Whole Test Script Button
    if st.button("▶ Run All Tests", use_container_width=True):
        response = requests.get(f"{API_BASE_URL}/run-test")
        if response.status_code == 200:
            st.success("✅ All tests executed!")
        else:
            st.error("❌ Failed to execute tests!")

    # Bug Table with Run Buttons
    st.write("### 📝 Bug List")
    for bug in bugs:
        col1, col2, col3 = st.columns([1, 3, 2])

        col1.write(f"🔹 **{bug['code']}**")
        col2.write(bug["desc"])

        if col3.button(f"▶ Run {bug['code']}", key=bug["code"]):
            response = requests.get(f"{API_BASE_URL}/run-test?test_name={bug['code']}")
            if response.status_code == 200:
                st.success(f"✅ {bug['code']} executed!")
            else:
                st.error(f"❌ Failed to run {bug['code']}")

# 👉 Allure Report Page
elif st.session_state.page == "Allure Report":
    st.subheader("📜 Allure Report")

    # Start Allure Button
    if st.button("▶ Start Allure Report"):
        response = requests.get(f"{API_BASE_URL}/start-allure")
        if response.status_code == 200:
            st.success("✅ Allure server started!")
        else:
            st.error("❌ Could not start Allure server.")

    # Stop Allure Button
    if st.button("⛔ Stop Allure Report"):
        response = requests.get(f"{API_BASE_URL}/stop-allure")
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error("❌ Could not stop Allure server.")

    if st.button("📊 Get Allure Report"):
    # Embed Allure report if available
        response = requests.get(f"{API_BASE_URL}/get-allure-url")
        if response.status_code == 200:
            allure_url = response.json().get("url", "")
            if allure_url:
                st.markdown(
            f"""<div style="display: flex; justify-content: center;"><iframe src="{allure_url}" width="100%" height="600px"></iframe></div>""",unsafe_allow_html=True)       
                time.sleep(5)
            else:
                st.error("❌ Failed to load Allure report URL.")
    else:
        st.toast("❌ Start Allure report Server by Clicking Start Allue Report.")
