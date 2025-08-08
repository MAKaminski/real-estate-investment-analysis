#!/usr/bin/env python3
"""
Real Estate Investment Analysis Dashboard
========================================

A web-based dashboard for visualizing real estate investment analysis results.
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import os
import json
from typing import Dict, List
import src.config as config

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Real Estate Investment Analysis Dashboard"

# Sample data for demonstration
def create_sample_data():
    """Create sample data for the dashboard"""
    np.random.seed(42)
    
    # Generate sample properties
    n_properties = 100
    addresses = [f"Property {i+1}, City, State" for i in range(n_properties)]
    prices = np.random.uniform(150000, 300000, n_properties)
    cash_on_cash = np.random.uniform(5, 25, n_properties)
    appreciation = np.random.uniform(2, 8, n_properties)
    tax_savings = np.random.uniform(1, 4, n_properties)
    principal_paydown = np.random.uniform(2, 6, n_properties)
    total_returns = cash_on_cash + appreciation + tax_savings + principal_paydown
    
    df = pd.DataFrame({
        'address': addresses,
        'price': prices,
        'cash_on_cash_return': cash_on_cash,
        'appreciation_return': appreciation,
        'tax_savings_return': tax_savings,
        'principal_paydown_return': principal_paydown,
        'total_return': total_returns,
        'monthly_cash_flow': np.random.uniform(200, 1500, n_properties),
        'annual_cash_flow': np.random.uniform(2400, 18000, n_properties),
        'down_payment': prices * 0.2,
        'sqft': np.random.uniform(1000, 2500, n_properties),
        'beds': np.random.randint(2, 5, n_properties),
        'baths': np.random.randint(1, 4, n_properties)
    })
    
    return df

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Real Estate Investment Analysis Dashboard", 
                   className="text-center mb-4"),
            html.Hr()
        ])
    ]),
    
    # Summary Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Properties", className="card-title"),
                    html.H2(id="total-properties", children="0")
                ])
            ], className="text-center")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Avg Total Return", className="card-title"),
                    html.H2(id="avg-total-return", children="0%")
                ])
            ], className="text-center")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Investment", className="card-title"),
                    html.H2(id="total-investment", children="$0")
                ])
            ], className="text-center")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Annual Cash Flow", className="card-title"),
                    html.H2(id="annual-cash-flow", children="$0")
                ])
            ], className="text-center")
        ], width=3)
    ], className="mb-4"),
    
    # Charts Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Return Distribution"),
                dbc.CardBody([
                    dcc.Graph(id="return-distribution-chart")
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Return Components"),
                dbc.CardBody([
                    dcc.Graph(id="return-components-chart")
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # Charts Row 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Price vs Total Return"),
                dbc.CardBody([
                    dcc.Graph(id="price-return-scatter")
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Cash Flow Distribution"),
                dbc.CardBody([
                    dcc.Graph(id="cash-flow-histogram")
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # Filters and Data Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Filters"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Min Total Return (%)"),
                            dcc.Slider(
                                id="min-return-slider",
                                min=0,
                                max=30,
                                step=1,
                                value=0,
                                marks={i: f"{i}%" for i in range(0, 31, 5)}
                            )
                        ], width=6),
                        dbc.Col([
                            html.Label("Max Price ($)"),
                            dcc.Slider(
                                id="max-price-slider",
                                min=100000,
                                max=500000,
                                step=10000,
                                value=300000,
                                marks={i: f"${i:,}" for i in range(100000, 501000, 100000)}
                            )
                        ], width=6)
                    ])
                ])
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Top Properties"),
                dbc.CardBody([
                    html.Div(id="top-properties-table")
                ])
            ])
        ], width=8)
    ], className="mb-4"),
    
    # Hidden div to store data
    dcc.Store(id="property-data")
    
], fluid=True)

# Callbacks
@app.callback(
    Output("property-data", "data"),
    Input("min-return-slider", "value"),
    Input("max-price-slider", "value")
)
def filter_data(min_return, max_price):
    """Filter data based on slider values"""
    df = create_sample_data()
    
    # Apply filters
    filtered_df = df[
        (df['total_return'] >= min_return) &
        (df['price'] <= max_price)
    ]
    
    return filtered_df.to_dict('records')

@app.callback(
    Output("total-properties", "children"),
    Output("avg-total-return", "children"),
    Output("total-investment", "children"),
    Output("annual-cash-flow", "children"),
    Input("property-data", "data")
)
def update_summary_cards(data):
    """Update summary cards"""
    if not data:
        return "0", "0%", "$0", "$0"
    
    df = pd.DataFrame(data)
    
    total_properties = len(df)
    avg_total_return = f"{df['total_return'].mean():.1f}%"
    total_investment = f"${df['down_payment'].sum():,.0f}"
    annual_cash_flow = f"${df['annual_cash_flow'].sum():,.0f}"
    
    return total_properties, avg_total_return, total_investment, annual_cash_flow

@app.callback(
    Output("return-distribution-chart", "figure"),
    Input("property-data", "data")
)
def update_return_distribution(data):
    """Update return distribution chart"""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    fig = px.histogram(
        df, 
        x='total_return',
        nbins=20,
        title="Distribution of Total Returns",
        labels={'total_return': 'Total Return (%)', 'count': 'Number of Properties'}
    )
    
    fig.update_layout(
        xaxis_title="Total Return (%)",
        yaxis_title="Number of Properties"
    )
    
    return fig

@app.callback(
    Output("return-components-chart", "figure"),
    Input("property-data", "data")
)
def update_return_components(data):
    """Update return components chart"""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    # Calculate average returns
    avg_returns = {
        'Cash on Cash': df['cash_on_cash_return'].mean(),
        'Appreciation': df['appreciation_return'].mean(),
        'Tax Savings': df['tax_savings_return'].mean(),
        'Principal Paydown': df['principal_paydown_return'].mean()
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(avg_returns.keys()),
            y=list(avg_returns.values()),
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        )
    ])
    
    fig.update_layout(
        title="Average Return Components",
        xaxis_title="Return Type",
        yaxis_title="Return (%)"
    )
    
    return fig

@app.callback(
    Output("price-return-scatter", "figure"),
    Input("property-data", "data")
)
def update_price_return_scatter(data):
    """Update price vs return scatter plot"""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    fig = px.scatter(
        df,
        x='price',
        y='total_return',
        size='annual_cash_flow',
        color='cash_on_cash_return',
        hover_data=['address', 'beds', 'baths'],
        title="Price vs Total Return",
        labels={
            'price': 'Property Price ($)',
            'total_return': 'Total Return (%)',
            'annual_cash_flow': 'Annual Cash Flow ($)',
            'cash_on_cash_return': 'Cash on Cash Return (%)'
        }
    )
    
    fig.update_layout(
        xaxis_title="Property Price ($)",
        yaxis_title="Total Return (%)"
    )
    
    return fig

@app.callback(
    Output("cash-flow-histogram", "figure"),
    Input("property-data", "data")
)
def update_cash_flow_histogram(data):
    """Update cash flow distribution chart"""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    fig = px.histogram(
        df,
        x='monthly_cash_flow',
        nbins=15,
        title="Monthly Cash Flow Distribution",
        labels={'monthly_cash_flow': 'Monthly Cash Flow ($)', 'count': 'Number of Properties'}
    )
    
    fig.update_layout(
        xaxis_title="Monthly Cash Flow ($)",
        yaxis_title="Number of Properties"
    )
    
    return fig

@app.callback(
    Output("top-properties-table", "children"),
    Input("property-data", "data")
)
def update_top_properties_table(data):
    """Update top properties table"""
    if not data:
        return html.P("No data available")
    
    df = pd.DataFrame(data)
    
    # Sort by total return and get top 10
    top_properties = df.nlargest(10, 'total_return')
    
    table_rows = []
    for idx, row in top_properties.iterrows():
        table_rows.append(
            html.Tr([
                html.Td(row['address'][:30] + "..."),
                html.Td(f"${row['price']:,.0f}"),
                html.Td(f"{row['total_return']:.1f}%"),
                html.Td(f"${row['monthly_cash_flow']:.0f}"),
                html.Td(f"{row['beds']} bed, {row['baths']} bath")
            ])
        )
    
    table = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Address"),
                html.Th("Price"),
                html.Th("Total Return"),
                html.Th("Monthly Cash Flow"),
                html.Th("Details")
            ])
        ]),
        html.Tbody(table_rows)
    ], striped=True, bordered=True, hover=True)
    
    return table

if __name__ == "__main__":
    import socket
    
    def find_free_port(start_port=8050):
        """Find a free port starting from start_port"""
        port = start_port
        while port < start_port + 100:  # Try up to 100 ports
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                port += 1
        return None
    
    print("Starting Real Estate Investment Analysis Dashboard...")
    
    # Find a free port
    port = find_free_port(8050)
    if port is None:
        print("Error: No free ports available in range 8050-8149")
        sys.exit(1)
    
    print(f"Open your browser and go to: http://127.0.0.1:{port}")
    try:
        app.run(debug=True, host='0.0.0.0', port=port)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port {port} is in use. Trying alternative port...")
            alt_port = find_free_port(port + 1)
            if alt_port:
                print(f"Using alternative port: {alt_port}")
                print(f"Open your browser and go to: http://127.0.0.1:{alt_port}")
                app.run(debug=True, host='0.0.0.0', port=alt_port)
            else:
                print("Error: No free ports available")
                sys.exit(1)
        else:
            raise e
