import pandas as pd
import streamlit as st
from streamlit.elements.data_editor import EditableData
from streamlit.logger import get_logger

from alpha import get_portfolio, save_portfolio


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


def sidebar_header():
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


def sidebar():
    sidebar_header()


def save(df: pd.DataFrame):
    df.sort_values(by="symbol", inplace=True)
    save_portfolio(df)
    st.success(f"Saved {len(df)} records!")


def refresh():
    st.experimental_rerun()


def page_header():
    st.title("Tracker")


def load_portfolio() -> EditableData:
    portfolio = get_portfolio()
    df = st.data_editor(
        portfolio,
        num_rows="dynamic",
        key="portfolio_editor",
        use_container_width=True,
    )
    return df


def content():
    page_header()
    df: EditableData = None
    with st.container():
        df = load_portfolio()

    with st.container():
        col1, col2, _, _ = st.columns([2, 2, 1, 4])
        with col1:
            if st.button("Refresh", use_container_width=True):
                refresh()
        with col2:
            if st.button("Save", use_container_width=True):
                save(df)


def main():
    sidebar()
    content()
    footer()


if __name__ == "__main__":
    main()
