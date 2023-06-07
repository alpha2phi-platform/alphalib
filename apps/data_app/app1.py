import streamlit as st
from yahooquery import Ticker

# Define a list of stocks
stocks = ["AAPL", "GOOGL", "MSFT", "AMZN"]

# Create a dropdown list of stocks
selected_stock = st.selectbox("Select a stock", stocks)

# Fetch the past 1 year price data using YahooQuery
ticker = Ticker(selected_stock)
price_data = ticker.history(period="1y")

# Display the price data
st.write("Past 1 year price data for", selected_stock)
st.data_editor(price_data.tail(10).reset_index())


# streamlit aggrid to edit Excel file


# sentiment score
# buy sell signal
# target % e.g. 15 %
# dividend history
