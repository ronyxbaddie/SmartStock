import streamlit as st
from services.auth_service import AuthService
from services.inventory_service import InventoryService

st.set_page_config(
    page_title="SmartStock",
    page_icon="📦",
    layout="wide"
)

auth = AuthService()
auth.ensure_admin_exists()

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN GATE ----------------
if st.session_state.user is None:
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = auth.login(username, password)
        if user:
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------------- HOME UI ----------------
else:
    st.sidebar.title("SmartStock")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    inventory = InventoryService()
    products = inventory.get_all_products()

    total_products = len(products)
    total_quantity = sum(p.quantity for p in products)
    expired_count = len(inventory.get_expired_products())
    low_stock_count = len(inventory.get_low_stock_products())

    st.markdown(
        """
        <h1 style='text-align: center;'>📦 SmartStock</h1>
        <p style='text-align: center; font-size:18px;'>
            Inventory Management & Monitoring System
        </p>
        <hr>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Products", total_products)

    with col2:
        st.metric("Total Stock", total_quantity)

    with col3:
        st.metric("Expired Items", expired_count)

    with col4:
        st.metric("Low Stock Items", low_stock_count)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ➕ Add Products")
        st.write("Add new items to inventory with expiry tracking.")

    with col2:
        st.markdown("### 📋 View Inventory")
        st.write("Browse, sort, and monitor current stock levels.")

    with col3:
        st.markdown("### ⏳ Expiry Alerts")
        st.write("Identify expired and near-expiry products early.")

    st.markdown("---")
    st.info(
        "Use the sidebar to navigate between features. "
        "These metrics give you a quick health check of your inventory."
    )
