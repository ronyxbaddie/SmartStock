import streamlit as st
from services.inventory_service import InventoryService
from datetime import date

st.title("Add New Product")

inventory = InventoryService()

with st.form("add_product_form"):
    name = st.text_input("Product Name")
    category = st.text_input("Category")
    price = st.number_input("Price", min_value=0.0, step=0.5)
    quantity = st.number_input("Quantity", min_value=0, step=1)
    expiry_date = st.date_input("Expiry Date", min_value=date.today())

    submitted = st.form_submit_button("Add Product")

if submitted:
    if not name or not category:
        st.error("Please fill all required fields")
    else:
        inventory.add_product(
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            expiry_date=str(expiry_date)
        )
        st.success("Product added successfully")
