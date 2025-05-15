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

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2ren",
    "padding": "2rem 1rem",
    "background": "linear-gradient(135deg, #2b2b2b 0%, #1a1a1a 100%)",
}

# Define Sidebar
sidebar = html.Div(
    [
        html.H2("Superstore Dashboard", style={"color": "#00ffcc", "font-weight": "bold"}),
        html.Hr(style={"border-color": "#00ffcc"}),
        html.P("Filter Data", style={"color": "#ffffff"}),
        html.Label("Select Region", style={"color": "#00ffccc"}),
        dcc.Dropdown(
            id="region-dropdown",
            options=[{"label": region, "value": region} for region in df['Regiob'].unique()],
            value=None,
            multi=True,
            style={"background-color": "#333", "color": "#000"},
        ),
        html.Label("Select Category", style={"color": "#00ffcc", "margin-top": "1rem"}),
        dcc.Dropdown(
            id="category-dropdown",
            options=[{"label": cat, "value": cat} for cat in df['Category'].unique()],
            value=None,
            multi=True,
            style={"background-color": "#333", "color": "#000"},
        ),
        dcc.Dropdown(
            id="year-dropdown",
            options=[{"label": year, "value": year} for year in df["Year"].unique()],
            value=None,
            multi=True,
            style={"background-color": "#333", "color": "#000"},
        ),
        html.Label("Discount Range", style={"color": "#00ffcc", "margin-top": "1rem"}),
        dcc.RangeSlider(
            id="discount-slider",
            min=0,
            max=0.8,
            step=0.1,
            value=[0, 0.8],
            marks={i / 10: str(i / 10) for i in range(0, 9, 2)},
        ),
    ],
    style=SIDEBAR_STYLE,
)

# Define main content
content = html.Div(
    [
        html.H1("Interactive Superstore Analytics", style={"color": "#00ffcc", "text-align": "center"}),
        dcc.Graph(id="sales-bar"),
        dcc.Graph(id="profit-scatter"),
        dcc.Graph(id="sales-trend"),
        dcc.Graph(id="category-pie"),
        dcc.Graph(id="correlation-heatmap"),
    ],
    style=CONTENT_STYLE,
)

# Main layout
app.layout = html.Div([sidebar, content])


