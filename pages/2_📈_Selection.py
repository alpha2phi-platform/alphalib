import streamlit as st
import pandas as pd
import numpy as np
from streamlit.logger import get_logger
from time import sleep

from alphalib.tracker import load_portfolio, save_portfolio
from alphalib.analysis.dividend import dividend_analysis

st.set_page_config(
    page_title="Selection",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🗸",
)
LOGGER = get_logger(__name__)


def footer():
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: visible;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def sidebar():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "Alphalib";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def content():
    st.title("Stock Selection")

    if "stock_selection" in st.session_state:
        stock_selection = st.session_state.stock_selection
    else:
        portfolio = load_portfolio()
        stock_selection = portfolio[
            ["symbol", "name", "current_price", "target_buy_price"]
        ]
        # stock_selection = portfolio[portfolio["symbol"].isin(["ABBV", "AMZN", "GOGL"])][
        #     ["symbol", "name", "current_price", "target_buy_price"]
        # ]
        # stock_selection.reset_index(drop=True, inplace=True)

    with st.form("stock_selection_form"):
        col1, col2 = st.columns([2, 2])
        with col1:
            if st.form_submit_button("New Target Price", use_container_width=True):
                st.write("Calculating new target prices...")
                new_target_prices = []
                counter = 0
                for symbol in stock_selection["symbol"]:
                    LOGGER.info("Processing {}".format(symbol))
                    counter = counter + 1
                    new_target_prices.append(
                        {
                            "symbol": symbol,
                            "target_buy_price": dividend_analysis(
                                symbol
                            ).target_buy_price,
                        }
                    )
                    if counter % 5 == 0:
                        sleep(1)
                stocks_with_new_prices = pd.DataFrame(new_target_prices)
                stock_selection["new_target_buy_price"] = np.where(
                    stocks_with_new_prices["target_buy_price"] > 0,
                    stocks_with_new_prices["target_buy_price"],
                    stock_selection["target_buy_price"],
                )
                st.write("Done")
        with col2:
            if st.form_submit_button("Save New Target Price", use_container_width=True):
                portfolio = load_portfolio()
                portfolio["target_buy_price"] = stock_selection["new_target_buy_price"]
                save_portfolio(portfolio)
                st.success(f"Saved {len(portfolio)} records!")

    with st.container():
        data = st.data_editor(
            stock_selection,
            num_rows="dynamic",
            use_container_width=True,
            height=600,
            key="portfolio_editor",
        )
        st.session_state.stock_selection = data


def app():
    sidebar()
    content()
    footer()


if __name__ == "__main__":
    app()
