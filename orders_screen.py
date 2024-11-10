import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import json
import time

app = dash.Dash(__name__)

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
        "Placed": "yellow",
    }.get(status, "lightgrey")


# Layout of the app
app.layout = html.Div([
    html.H1("Order Status Dashboard"),
    dash_table.DataTable(
        id='orders-table',
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{{Status}} = "{}"'.format(status),
                    'column_id': 'Status'
                },
                'backgroundColor': status_color(status),
                'color': 'Black'
            } for status in ["Traded", "Failed", "Placed"]
        ],
        style_cell={'textAlign': 'center'},
        page_size=10
    ),
    dcc.Interval(
        id='interval-component',
        interval=100,  # in milliseconds
        n_intervals=0
    )
])

# Update the table with new data


@app.callback(
    Output('orders-table', 'data'),
    Input('interval-component', 'n_intervals')
)
def update_table(n):
    df = load_json_data()
    return df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True,port=8050)
