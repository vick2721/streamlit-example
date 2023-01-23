import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt

st.title("Time-Series Analysis of Customer Numbers")

# Load data
data = pd.read_csv("customer_data.csv")

# Create user interface
st.sidebar.header("Select Time Range")
start_date = st.sidebar.date_input("Start date")
end_date = st.sidebar.date_input("End date")
chart_type = st.sidebar.selectbox("Select chart type", ["Line", "Bar"])

# Filter data based on user input
filtered_data = data[(data["date"] >= start_date) & (data["date"] <= end_date)]

# Create chart
if chart_type == "Line":
    plt.plot(filtered_data["date"], filtered_data["customer_numbers"])
    plt.xlabel("Date")
    plt.ylabel("Customer Numbers")
    st.pyplot()
else:
    plt.bar(filtered_data["date"], filtered_data["customer_numbers"])
    plt.xlabel("Date")
    plt.ylabel("Customer Numbers")
    st.pyplot()

# Add export data functionality
if st.button("Export data"):
    st.write("Exported data to CSV.")
    filtered_data.to_csv("filtered_data.csv", index=False)
