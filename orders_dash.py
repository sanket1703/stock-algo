import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import json
from datetime import datetime
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Define a function to load JSON data


def load_json_data():
    with open("order_book/orders.json", 'r') as f:
        data = json.load(f)
    # Assuming JSON structure {"orders": [ ... ]}
    return pd.DataFrame(data["orders"])

# Define status color mapping


def status_color(status):
    return {
        "Traded": "green",
        "Failed": "red",
        "Placed": "blue",
    }.get(status, "lightgrey")

# Get current date and last updated timestamp


def get_current_date():
    return datetime.now().strftime("%d %B %Y")


def get_last_updated_time():
    return datetime.now().strftime("%d %B %Y %I:%M %p")


# Layout of the app
app.layout = html.Div([
    dbc.Container([
        # Header
        html.Div([
            html.H1("Order Status Dashboard", style={
                    'textAlign': 'center', 'color': 'white'}),
            html.Div([
                html.Div(f"Last Updated: {get_last_updated_time()}", id="last-updated", style={
                         'color': 'white', 'fontSize': '18px', 'textAlign': 'left'})
            ], style={'marginBottom': '20px'}),
        ], id="header", style={'padding': '20px', 'backgroundColor': '#333333', 'borderRadius': '8px'}),

        # Data Table
        dash_table.DataTable(
            id='orders-table',
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{{Status}} = "{}"'.format(status),
                        'column_id': 'Status'
                    },
                    'backgroundColor': 'lightgrey',
                    'color': 'Black'
                } for status in ["Traded", "Failed", "Placed"]
            ],
            style_cell={'textAlign': 'center', 'padding': '10px',
                        'color': 'white', 'fontSize': '14px'},
            style_header={'backgroundColor': '#2c2c2c',
                          'fontWeight': 'bold', 'color': 'white', 'textAlign': 'center'},
            style_table={'overflowX': 'auto', 'borderRadius': '10px',
                         'boxShadow': '0px 0px 10px rgba(0, 0, 0, 0.5)'},
            page_size=15,
            style_data={'backgroundColor': '#333333',
                        'border': '1px solid #444444'},
        ),

        # Auto-refresh Timer (Interval)
        dcc.Interval(
            id='interval-component',
            interval=10,  # in milliseconds (10 seconds for auto-refresh)
            n_intervals=0
        ),
    ])
])

# Update the table with new data and refresh the timestamp


@app.callback(
    Output('orders-table', 'data'),
    Output('last-updated', 'children'),
    Output('orders-table', 'style_data_conditional'),
    Input('interval-component', 'n_intervals')
)
def update_table(n):
    # Load data
    df = load_json_data()

    # Dark theme only
    background_color = "#333333"
    text_color = "white"

    # Set status colors for dark theme
    status_colors = [
        {
            'if': {
                'filter_query': '{{Status}} = "{}"'.format(status),
                'column_id': 'Status'
            },
            'backgroundColor': status_color(status),
            'color': text_color
        } for status in ["Traded", "Failed", "Placed"]
    ]

    # Header style change
    header_style = {'padding': '20px',
                    'backgroundColor': background_color, 'borderRadius': '8px'}

    # Adjust text color for the table depending on the theme
    table_style = {'backgroundColor': background_color,
                   'color': text_color, 'borderRadius': '10px'}

    # Get the current time for the "Last Updated" timestamp
    last_updated_time = get_last_updated_time()

    return df.to_dict('records'), f"Last Updated: {last_updated_time}", status_colors


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
