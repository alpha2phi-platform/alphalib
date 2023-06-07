import streamlit as st
from api import get_screener_data

# Config app
st.set_page_config(page_title="Stock Screener", layout="wide")
st.title("Stock Screener")

demo_api = "7e487314d31d9ce712a84b5147937316"


# Input widgets in sidebar
def stock_screener(my_api_key):
    with st.sidebar.form(key="my_form", clear_on_submit=False):
        market_cap = st.selectbox(label="Market cap", options=("1000000", "1000000000"))
        beta = st.selectbox(label="Beta", options=("1", "2"))
        volume = st.selectbox(label="Volume", options=("10000", "100000"))
        sector = st.selectbox(label="Sector", options=("Technology", "Healthcare"))
        exchange = st.selectbox(label="Exchange", options=("nasdaq", "nyse"))
        dividend = st.selectbox(label="Dividend", options=(0, 1))
        # Input widget 2
        pressed = st.form_submit_button(label="Submit")

    if not pressed:
        st.dataframe(get_screener_data(api_key=my_api_key), height=800)
    else:
        st.dataframe(
            get_screener_data(
                api_key=my_api_key,
                marketcapmorethan=market_cap,
                betamorethan=beta,
                volmorethan=volume,
                sector=sector,
                exchange=exchange,
                dividendmorethan=dividend,
            ),
            height=800,
        )


# Call the function
stock_screener(my_api_key=demo_api)
