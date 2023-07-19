from os import wait
import streamlit as st
from streamlit.logger import get_logger

from alphalib.tracker import get_portfolio
from alphalib.analysis.dividend import dividend_analysis


st.set_page_config(
    page_title="Dividend Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="💰",
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
    st.title("Dividend Analysis")
    portfolio = get_portfolio()
    portfolio["long_name"] = portfolio["symbol"] + "-" + portfolio["name"]
    with st.container():
        option = st.selectbox(
            "Stock", portfolio["long_name"], label_visibility="hidden"
        )
        if option:
            symbol = option.split("-")[0]
            analysis = dividend_analysis(symbol)

            st.header(f"{analysis.symbol} - {analysis.interval} Dividend")
            col1, col2 = st.columns([2, 4])
            with col1:
                st.text(f"Dividiend Yield: {analysis.dividend_yield_pct}")
                st.text(f"Annual Dividend: {analysis.annual_dividend}")
                st.text(f"PE Ratio: {analysis.pe_ratio}")
                st.text(f"Ex Dividend Date: {analysis.ex_dividend_date}")

            with col2:
                st.subheader("Dividend vs Prices")
                st.dataframe(analysis.result, use_container_width=True, hide_index=True)

            st.subheader("Dividend History")
            st.dataframe(
                analysis.dividend_history, use_container_width=True, hide_index=True
            )


def app():
    sidebar()
    content()
    footer()


if __name__ == "__main__":
    app()
