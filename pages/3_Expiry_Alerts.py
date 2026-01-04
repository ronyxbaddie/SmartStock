import streamlit as st
import pandas as pd
from services.inventory_service import InventoryService

if "user" not in st.session_state:
    st.session_state.user=None

if st.session_state.user==None:
    st.title("Please First Login!!")

else:
    st.title("Expiry Alerts")

    inventory = InventoryService()

    expired_products = inventory.get_expired_products()
    near_expiry_products = inventory.get_near_expiry_products(days=7)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Expired Products", len(expired_products))

    with col2:
        st.metric("Near Expiry (7 days)", len(near_expiry_products))


    def to_dataframe(products):
        return pd.DataFrame([
            {
                "Name": p.name,
                "Category": p.category,
                "Price": p.price,
                "Quantity": p.quantity,
                "Expiry Date": p.expiry_date.date()
            }
            for p in products
        ])


    st.subheader("❌ Expired Products")

    if expired_products:
        st.dataframe(to_dataframe(expired_products), width="stretch")
    else:
        st.success("No expired products 🎉")

    command = st.button("Remove Expiry Products")

    if command:
        for p in expired_products:
            inventory.delete_product(p.name)

    st.subheader("⚠️ Near Expiry Products (Next 7 Days)")

    if near_expiry_products:
        st.dataframe(to_dataframe(near_expiry_products), width="stretch")
    else:
        st.success("No products nearing expiry 🎉")
