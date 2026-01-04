import streamlit as st
import pandas as pd
from services.inventory_service import InventoryService

if "user" not in st.session_state:
    st.session_state.user=None

if st.session_state.user==None:
    st.title("Please first Login!!")
    
else:
    st.title("Inventory")

    inventory = InventoryService()

    col1, col2 = st.columns(2)

    with col1:
        sort_option = st.selectbox(
            "Sort products by",
            ["None", "Price", "Quantity", "Expiry Date"]
        )
        
        # if sort_option == "Price":
        #     products = inventory.get_sorted_products(by="price")
        # elif sort_option == "Quantity":
        #     products = inventory.get_sorted_products(by="quantity")
        # elif sort_option == "Expiry Date":
        #     products = inventory.get_sorted_products(by="expiry")
        # else:
        #     products = inventory.get_all_products()
        
    with col2:
        sort_order = st.selectbox(
            "Sort oder",
            ["Ascending", "Descending"]
        )

        if sort_order=="Ascending":
            if sort_option == "Price":
                products = inventory.get_sorted_products(by="price", order="Ascneding")
            elif sort_option == "Quantity":
                products = inventory.get_sorted_products(by="quantity", order="Ascneding")
            elif sort_option == "Expiry Date":
                products = inventory.get_sorted_products(by="expiry", order="Ascneding")
            else:
                products = inventory.get_all_products()
        elif sort_order=="Descending":
            if sort_option == "Price":
                products = inventory.get_sorted_products(by="price", order="Descending")
            elif sort_option == "Quantity":
                products = inventory.get_sorted_products(by="quantity", order="Descending")
            elif sort_option == "Expiry Date":
                products = inventory.get_sorted_products(by="expiry", order="Descending")
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

    df = pd.DataFrame(
        data,
        columns=["Name", "Category", "Price", "Quantity", "Expired", "Low Stock"]
    )

    st.dataframe(df, use_container_width=True)

    expired_count = df["Expired"].sum()
    low_stock_count = df["Low Stock"].sum()

    if expired_count > 0:
        st.warning(f"{expired_count} expired products found")

    if low_stock_count > 0:
        st.warning(f"{low_stock_count} products are low in stock")
