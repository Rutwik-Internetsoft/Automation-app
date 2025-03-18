import streamlit as st
import requests

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

# Sidebar Navigation
st.sidebar.title("📊 Dashboard")

if "page" not in st.session_state:
    st.session_state.page = "Run Sanity"

def set_page(page_name):
    st.session_state.page = page_name

st.sidebar.button("🚀 Run Sanity", use_container_width=True, on_click=set_page, args=("Run Sanity",))
st.sidebar.button("🐞 Bug Issues", use_container_width=True, on_click=set_page, args=("Bug Issues",))
st.sidebar.button("📜 Allure Report", use_container_width=True, on_click=set_page, args=("Allure Report",))

# Main Content
st.title(st.session_state.page)

# 👉 Run Sanity Tests Page
if st.session_state.page == "Run Sanity":
    st.subheader("Execute Sanity Test Suite")
    
    if st.button("▶ Start Sanity Tests", use_container_width=True):
        response = requests.get("http://127.0.0.1:8000/run-test")
        if response.status_code == 200:
            st.success("✅ Sanity tests started!")
        else:
            st.error("❌ Failed to execute tests!")

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
        response = requests.get("http://127.0.0.1:8000/run-test")
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
            response = requests.get(f"http://127.0.0.1:8000/run-test?test_name={bug['code']}")
            if response.status_code == 200:
                st.success(f"✅ {bug['code']} executed!")
            else:
                st.error(f"❌ Failed to run {bug['code']}")

# 👉 Allure Report Page
elif st.session_state.page == "Allure Report":
    st.subheader("📜 Allure Report")

    # Start Allure Button
    if st.button("▶ Start Allure Report", use_container_width=True):
        response = requests.get("http://127.0.0.1:8000/start-allure")
        if response.status_code == 200:
            st.success("✅ Allure server started!")
        else:
            st.error("❌ Could not start Allure server.")

    # Stop Allure Button
    if st.button("⛔ Stop Allure Report", use_container_width=True):
        response = requests.get("http://127.0.0.1:8000/stop-allure")
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error("❌ Could not stop Allure server.")

    # Embed Allure report if available
    response = requests.get("http://127.0.0.1:8000/get-allure-url")
    if response.status_code == 200:
        allure_url = response.json().get("url", "")
        if allure_url:
            st.markdown(f'<iframe src="{allure_url}" width="100%" height="600px"></iframe>', unsafe_allow_html=True)
        else:
            st.error("❌ Failed to load Allure report URL.")
    else:
        st.error("❌ Could not retrieve Allure report URL.")
