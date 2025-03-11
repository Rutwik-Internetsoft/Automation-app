import streamlit as st
from webapp.phoneorderapp import PhoneOrderApp

def main():
    st.title("Test Execution Dashboard")
    app = PhoneOrderApp()

    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        st.subheader("Orders")
        if st.button("📞 Phone Order"):
            st.session_state.page = "phone_order"
            st.rerun()

    elif st.session_state.page == "phone_order":
        app.phone_order()

    elif st.session_state.page in ["test_phoneorder_cash", "test_phoneorder_card"]:

        # 🔹 Fetch order type dynamically from session state
        order_type = "test_phoneorder_cash" if st.session_state.page == "phone_order_cash" else "test_phoneorder_card"
        
        # 🔹 Debug: Show selected order type
        
        # 🔹 Call the correct test execution function
        app.phone_order_test_execution(order_type)

if __name__ == "__main__":
    main()
