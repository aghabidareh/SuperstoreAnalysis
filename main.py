import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Loading and preparing data
df = pd.read_csv('superstore.csv')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year

# Dash with Dark Theme
app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

# Defining custom styles
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0.0,
    'left': 0.0,
    'bottom': 0.0,
    'width': "16rem",
    "padding": "2rem 1rem",
    "background-color": "#1a1a1a",
    "box-shadow": "2px 0 5px rgba(0,0,0,0.5)"
}

