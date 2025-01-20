import pandas as pd
import streamlit as st
import os
from PIL import Image
import requests

# saving and loading data
df = "https://raw.githubusercontent.com/shreyasnimkhedkar/store_management/refs/heads/main/hotel.csv"

# Initialize hotel DataFrame
if 'hotel_df' not in st.session_state:
    if os.path.exists(df):
        st.session_state.hotel_df = pd.read_csv(df)
    else:
        columns = ['Customer ID', 'Customer Name', 'State', 'City', 'Address',
                   'Check-In Date', 'Check-Out Date', 'Bed Type', 'Price']
        st.session_state.hotel_df = pd.DataFrame(columns=columns)
st.write('''The goal of this project is to create a simple and user-friendly hotel management system using Streamlit, a Python library for building web applications. 
         The system allows hotel staff to manage customer details, such as adding new customers, viewing existing customer records, updating customer information, and deleting customer records. 
         The data is stored in a CSV file, enabling the system to persist information between sessions.''')

# Function to save data to the CSV file
def save_data():
    st.session_state.hotel_df.to_csv(df, index=False)

# Function to add a customer
def customer():
    customer_id = st.text_input("Enter Customer ID")
    customer_name = st.text_input("Enter Customer Name")
    state = st.text_input("Enter State")
    city = st.text_input("Enter City")
    address = st.text_input("Enter Address")
    check_in_date = st.date_input("Enter Check-In Date")
    check_out_date = st.date_input("Enter Check-Out Date")
    bed_type = st.selectbox("Enter Bed Type", ['1 Bed', '2 Bed'])
    price = st.number_input("Enter Price", min_value=0.0, format="%.2f")
    
    if st.button("Add Customer"):
        new_customer = {
            'Customer ID': customer_id,
            'Customer Name': customer_name,
            'State': state,
            'City': city,
            'Address': address,
            'Check-In Date': str(check_in_date),
            'Check-Out Date': str(check_out_date),
            'Bed Type': bed_type,
            'Price': price
        }
        st.session_state.hotel_df = pd.concat([st.session_state.hotel_df, pd.DataFrame([new_customer])], ignore_index=True)
        save_data()
        st.success("Customer added successfully!")
        st.write(st.session_state.hotel_df)

# Function for view customer
def view_customer():
    if st.session_state.hotel_df.empty:
        st.warning("No customer records found.")
    else:
        st.write(st.session_state.hotel_df)

# Function for update cuustomer
def update_customer():
    customer_id = st.text_input("Enter Customer ID to update")
    
    if customer_id and customer_id in st.session_state.hotel_df['Customer ID'].astype(str).values:
        index = st.session_state.hotel_df[st.session_state.hotel_df['Customer ID'].astype(str) == customer_id].index[0]
        st.write(f"Updating details for {customer_id}:")
        
        customer_name = st.text_input("Customer Name", value=st.session_state.hotel_df.at[index, 'Customer Name'])
        state = st.text_input("State", value=st.session_state.hotel_df.at[index, 'State'])
        city = st.text_input("City", value=st.session_state.hotel_df.at[index, 'City'])
        address = st.text_input("Address", value=st.session_state.hotel_df.at[index, 'Address'])
        check_in_date = st.date_input("Check-In Date", value=pd.to_datetime(st.session_state.hotel_df.at[index, 'Check-In Date']))
        check_out_date = st.date_input("Check-Out Date", value=pd.to_datetime(st.session_state.hotel_df.at[index, 'Check-Out Date']))
        # bed_type = st.selectbox("Bed Type", ['1 Bed', '2 Bed'], index=['1 Bed', '2 Bed'].index(st.session_state.hotel_df.at[index, 'Bed Type']))
        bed_type = st.selectbox(
    "Bed Type",
    ['1 Bed', '2 Bed'],
    index=['1 Bed', '2 Bed'].index(st.session_state.hotel_df.at[index, 'Bed Type']) if st.session_state.hotel_df.at[index, 'Bed Type'] in ['1 Bed', '2 Bed'] else 0
)

        price = st.number_input("Price", min_value=0.0, value=st.session_state.hotel_df.at[index, 'Price'], format="%.2f")
        
        if st.button("Update Customer"):
            st.session_state.hotel_df.at[index, 'Customer Name'] = customer_name
            st.session_state.hotel_df.at[index, 'State'] = state
            st.session_state.hotel_df.at[index, 'City'] = city
            st.session_state.hotel_df.at[index, 'Address'] = address
            st.session_state.hotel_df.at[index, 'Check-In Date'] = str(check_in_date)
            st.session_state.hotel_df.at[index, 'Check-Out Date'] = str(check_out_date)
            st.session_state.hotel_df.at[index, 'Bed Type'] = bed_type
            st.session_state.hotel_df.at[index, 'Price'] = price
            save_data()
            st.success("Customer details updated successfully!")
            st.write(st.session_state.hotel_df)
    else:
        st.warning("Customer ID not found!")

# Function for delete a customer
def delete_customer():
    customer_id = st.text_input("Enter Customer ID to delete")
    
    if customer_id and customer_id in st.session_state.hotel_df['Customer ID'].astype(str).values:
        if st.button("Delete Customer"):
            st.session_state.hotel_df.drop(st.session_state.hotel_df[st.session_state.hotel_df['Customer ID'].astype(str) == customer_id].index, inplace=True)
            save_data()
            st.success("Customer deleted successfully!")
            st.write(st.session_state.hotel_df)
    else:
        st.warning("Customer ID not found!")
# st.image("D:\python_\hotel_img.jpg", caption="This is an image", use_column_width=True)
# streamlit layout
st.title("Hotel Management System")

menu = ["Add Customer", "View Customers", "Update Customer", "Delete Customer"]
choice = st.sidebar.selectbox("Choose an option", menu)

if choice == "Add Customer":
    customer()
elif choice == "View Customers":
    view_customer()
elif choice == "Update Customer":
    update_customer()
elif choice == "Delete Customer":
    delete_customer()
