import streamlit as st
import pandas as pd
from services.inventory_service import InventoryService

st.title("Inventory")

inventory = InventoryService()

sort_option = st.selectbox(
    "Sort products by",
    ["None", "Price", "Quantity", "Expiry Date"]
)

if sort_option == "Price":
    products = inventory.get_sorted_products(by="price")
elif sort_option == "Quantity":
    products = inventory.get_sorted_products(by="quantity")
elif sort_option == "Expiry Date":
    products = inventory.get_sorted_products(by="expiry")
else:
    products = inventory.get_all_products()

data = []

for p in products:
    data.append({
        "Name": p.name,
        "Category": p.category,
        "Price": p.price,
        "Quantity": p.quantity,
        "Expired": p.is_expired(),
        "Low Stock": p.low_stock()
    })

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)

expired_count = df["Expired"].sum()
low_stock_count = df["Low Stock"].sum()

if expired_count > 0:
    st.error(f"{expired_count} expired products found")

if low_stock_count > 0:
    st.warning(f"{low_stock_count} products are low in stock")
