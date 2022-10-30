import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf


def plot_ichimoku(symbol: str):
    assert symbol
