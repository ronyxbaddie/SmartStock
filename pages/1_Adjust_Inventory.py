import streamlit as st
from services.inventory_service import InventoryService
from datetime import date

st.title("Adjust Inventory")

inventory = InventoryService()

st.info(
    "Use a positive quantity to add stock and a negative quantity to remove stock. "
    "If the final quantity becomes zero, the product will be removed automatically."
)

with st.form("adjust_inventory_form"):
    name = st.text_input("Product Name")

    quantity_change = st.number_input(
        "Quantity Change",
        step=1,
        help="Positive to add stock, negative to remove stock"
    )

    category = st.text_input("Category (required for new product only)")
    price = st.number_input(
        "Price (required for new product only)",
        min_value=0.0,
        step=0.5
    )
    expiry_date = st.date_input(
        "Expiry Date (required for new product only)",
        min_value=date.today()
    )

    submitted = st.form_submit_button("Apply Change")

if submitted:
    if not name:
        st.error("Product name is required")
    else:
        try:
            inventory.adjust_quantity(
                name=name,
                delta=quantity_change,
                category=category if category else None,
                price=price if price > 0 else None,
                expiry_date=str(expiry_date)
            )
            st.success("Inventory updated successfully")
        except Exception as e:
            st.error(str(e))
