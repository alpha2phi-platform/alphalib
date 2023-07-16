import pandas as pd
import streamlit as st
from streamlit.elements.data_editor import EditableData
from streamlit.logger import get_logger

from alpha import get_portfolio, save_portfolio, refresh_porfolio


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


def sidebar():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "MyInvestor";
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


def save():
    portfolio = st.session_state.portfolio
    portfolio.sort_values(by="symbol", inplace=True)
    save_portfolio(portfolio)
    st.success(f"Saved {len(portfolio)} records!")


def refresh():
    st.info("Refreshing portfolio...")
    refresh_porfolio(st.session_state.portfolio)
    st.experimental_rerun()


def content():
    st.title("Tracker")
    portfolio: EditableData | pd.DataFrame = None
    if "portfolio" in st.session_state:
        portfolio = st.session_state.portfolio
    else:
        portfolio = get_portfolio()
    with st.container():
        data = st.data_editor(
            portfolio,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "nasdaq_url": st.column_config.LinkColumn(),
                "yahoo_finance_url": st.column_config.LinkColumn(),
            },
            key="portfolio_editor",
        )
        st.session_state.portfolio = data

    with st.container():
        col1, col2, _, _ = st.columns([2, 2, 1, 4])
        with col1:
            if st.button("Refresh", use_container_width=True):
                refresh()
        with col2:
            if st.button("Save", use_container_width=True):
                save()


def app():
    sidebar()
    content()
    footer()


if __name__ == "__main__":
    app()
