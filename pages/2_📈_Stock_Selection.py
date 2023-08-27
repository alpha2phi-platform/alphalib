import streamlit as st
from streamlit.logger import get_logger

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
    with st.container():
        st.write("Stock Selection")


def app():
    sidebar()
    content()
    footer()


if __name__ == "__main__":
    app()
