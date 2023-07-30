import pandas as pd
import streamlit as st
from streamlit.logger import get_logger

from alphalib.analysis.dividend import dividend_analysis
from alphalib.analysis.sentiment import finwiz_score
from alphalib.tracker import get_portfolio
from alphalib.utils.dateutils import month_from
from alphalib.analysis.ta.trend.ichimoku import plot_ichimoku

st.set_page_config(
    page_title="Balance Sheet",
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
    st.title("Balance Sheet")
    with st.container():
        st.write("Balance sheet analysis")


def app():
    sidebar()
    content()
    footer()


if __name__ == "__main__":
    app()
