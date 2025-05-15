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


# callback to update plots
@app.callback(
    [
        Output("sales-bar", "figure"),
        Output("profit-scatter", "figure"),
        Output("sales-trend", "figure"),
        Output("category-pie", "figure"),
        Output("correlation-heatmap", "figure"),
    ],
    [
        Input("region-dropdown", "value"),
        Input("category-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("discount-slider", "value"),
    ],
)
def update_graphs(
        selected_regions,
        selected_categories,
        selected_years,
        discount_range
):
    filtered_df = df.copy()
    if selected_regions:
        filtered_df = filtered_df[filtered_df["Region"].isin(selected_regions)]
    if selected_categories:
        filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]
    if selected_years:
        filtered_df = filtered_df[filtered_df["Year"].isin(selected_years)]
    filtered_df = filtered_df[
        (filtered_df["Discount"] >= discount_range[0]) & (filtered_df["Discount"] <= discount_range[1])
        ]

    sales_by_category = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig_bar = px.bar(
        sales_by_category,
        x="Category",
        y="Sales",
        title="Total Sales by Category",
        color="Category",
        color_discrete_sequence=px.colors.sequential.Plasma,
    )
    fig_bar.update_layout(
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#1a1a1a",
        font_color="#ffffff",
        title_font_color="#00ffcc",
        showlegend=False,
    )

    fig_scatter = px.scatter(
        filtered_df,
        x="Sales",
        y="Profit",
        color="Discount",
        size="Quantity",
        hover_data=["Product Name", "Region"],
        title="Sales vs Profit (Colored by Discount)",
        color_continuous_scale=px.colors.sequential.Viridis,
    )
    fig_scatter.update_layout(
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#1a1a1a",
        font_color="#ffffff",
        title_font_color="#00ffcc",
    )

    sales_trend = filtered_df.groupby("Order Date")["Sales"].sum().resample("M").sum().reset_index()
    fig_trend = px.line(
        sales_trend,
        x="Order Date",
        y="Sales",
        title="Sales Trend Over Time",
        markers=True,
    )
    fig_trend.update_traces(line_color="#00ffcc")
    fig_trend.update_layout(
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#1a1a1a",
        font_color="#ffffff",
        title_font_color="#00ffcc",
    )

    category_share = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig_pie = px.pie(
        category_share,
        names="Category",
        values="Sales",
        title="Sales Share by Category",
        color_discrete_sequence=px.colors.sequential.Plasma,
    )
    fig_pie.update_layout(
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#1a1a1a",
        font_color="#ffffff",
        title_font_color="#00ffcc",
    )

    numeric_cols = ["Sales", "Quantity", "Discount", "Profit"]
    corr_matrix = filtered_df[numeric_cols].corr()
    fig_heatmap = go.Figure(
        data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale="RdBu",
            showscale=True,
            text=corr_matrix.values.round(2),
            texttemplate="%{text}",
            textfont={"size": 12, "color": "#ffffff"},
        )
    )
    fig_heatmap.update_layout(
        title="Correlation Heatmap",
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#1a1a1a",
        font_color="#ffffff",
        title_font_color="#00ffcc",
    )

    return fig_bar, fig_scatter, fig_trend, fig_pie, fig_heatmap
