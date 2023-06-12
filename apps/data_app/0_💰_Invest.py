import base64
from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit.logger import get_logger

PORTFOLIO_FILE = "data/portfolio.xlsx"

st.set_page_config(
    page_title="Alpha2phi - Investment",
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


def get_portfolio() -> pd.DataFrame:
    return pd.read_excel(PORTFOLIO_FILE)


def sidebar():
    st.sidebar.header("My Portfolio")


def content():
    df_portfolio = pd.read_excel(PORTFOLIO_FILE)


def main():
    sidebar()
    content()
    footer()


if __name__ == "__main__":
    main()
