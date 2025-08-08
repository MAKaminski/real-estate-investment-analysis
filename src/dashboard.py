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
    
    # Navigation Tabs
    dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(label="Overview", tab_id="overview"),
                dbc.Tab(label="Financial Projections", tab_id="projections"),
            ], id="tabs", active_tab="overview")
        ])
    ], className="mb-4"),
    
    # Tab Content
    html.Div(id="tab-content"),
    
    # Hidden div to store data
    dcc.Store(id="property-data")
    
], fluid=True)

# Tab Content Callback
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
    Input("property-data", "data")
)
def render_tab_content(active_tab, data):
    """Render content based on active tab"""
    if active_tab == "overview":
        return create_overview_tab(data)
    elif active_tab == "projections":
        return create_projections_tab(data)
    return html.Div("Select a tab")

def create_overview_tab(data):
    """Create the overview tab content"""
    return [
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
        ], className="mb-4")
    ]

def create_projections_tab(data):
    """Create the financial projections tab content"""
    return [
        # Financial Projections Header
        dbc.Row([
            dbc.Col([
                html.H2("Financial Projections & Analysis", className="text-center mb-4"),
                html.P("Detailed financial forecasts for all properties including cash flow, returns, and investment metrics", 
                      className="text-center text-muted")
            ])
        ], className="mb-4"),
        
        # Projection Filters
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Projection Filters"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("Time Horizon (Years)"),
                                dcc.Slider(
                                    id="projection-years",
                                    min=1,
                                    max=10,
                                    step=1,
                                    value=5,
                                    marks={i: f"{i}Y" for i in range(1, 11)}
                                )
                            ], width=4),
                            dbc.Col([
                                html.Label("Min Cash-on-Cash Return (%)"),
                                dcc.Slider(
                                    id="min-coc-return",
                                    min=0,
                                    max=20,
                                    step=1,
                                    value=5,
                                    marks={i: f"{i}%" for i in range(0, 21, 5)}
                                )
                            ], width=4),
                            dbc.Col([
                                html.Label("Max Investment per Property ($)"),
                                dcc.Slider(
                                    id="max-investment",
                                    min=50000,
                                    max=100000,
                                    step=5000,
                                    value=60000,
                                    marks={i: f"${i:,}" for i in range(50000, 101000, 10000)}
                                )
                            ], width=4)
                        ])
                    ])
                ])
            ])
        ], className="mb-4"),
        
        # Financial Summary Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Portfolio Value", className="card-title"),
                        html.H2(id="total-portfolio-value", children="$0"),
                        html.P("After projection period", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Cash Flow", className="card-title"),
                        html.H2(id="total-cash-flow", children="$0"),
                        html.P("Cumulative over projection period", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Average Annual Return", className="card-title"),
                        html.H2(id="avg-annual-return", children="0%"),
                        html.P("Compound annual growth rate", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("ROI", className="card-title"),
                        html.H2(id="total-roi", children="0%"),
                        html.P("Return on investment", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3)
        ], className="mb-4"),
        
        # Projection Charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Cash Flow Projection"),
                    dbc.CardBody([
                        dcc.Graph(id="cash-flow-projection-chart")
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Portfolio Value Growth"),
                    dbc.CardBody([
                        dcc.Graph(id="portfolio-growth-chart")
                    ])
                ])
            ], width=6)
        ], className="mb-4"),
        
        # Detailed Projections Table
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Detailed Financial Projections"),
                    dbc.CardBody([
                        html.Div(id="projections-table")
                    ])
                ])
            ])
        ], className="mb-4")
    ]

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

# Financial Projections Callbacks
@app.callback(
    Output("total-portfolio-value", "children"),
    Output("total-cash-flow", "children"),
    Output("avg-annual-return", "children"),
    Output("total-roi", "children"),
    Input("property-data", "data"),
    Input("projection-years", "value"),
    Input("min-coc-return", "value"),
    Input("max-investment", "value")
)
def update_projection_summary(data, years, min_coc, max_investment):
    """Update financial projection summary cards"""
    if not data:
        return "$0", "$0", "0%", "0%"
    
    df = pd.DataFrame(data)
    
    # Filter properties based on criteria
    filtered_df = df[
        (df['cash_on_cash_return'] >= min_coc) &
        (df['down_payment'] <= max_investment)
    ]
    
    if len(filtered_df) == 0:
        return "$0", "$0", "0%", "0%"
    
    # Calculate projections
    total_investment = filtered_df['down_payment'].sum()
    annual_cash_flow = filtered_df['annual_cash_flow'].sum()
    
    # Project over years
    cumulative_cash_flow = annual_cash_flow * years
    appreciation_growth = filtered_df['price'].sum() * (1.03 ** years - 1)  # 3% annual appreciation
    total_portfolio_value = total_investment + cumulative_cash_flow + appreciation_growth
    
    # Calculate returns
    total_return = total_portfolio_value - total_investment
    roi = (total_return / total_investment) * 100 if total_investment > 0 else 0
    avg_annual_return = ((total_portfolio_value / total_investment) ** (1/years) - 1) * 100 if total_investment > 0 else 0
    
    return (
        f"${total_portfolio_value:,.0f}",
        f"${cumulative_cash_flow:,.0f}",
        f"{avg_annual_return:.1f}%",
        f"{roi:.1f}%"
    )

@app.callback(
    Output("cash-flow-projection-chart", "figure"),
    Input("property-data", "data"),
    Input("projection-years", "value")
)
def update_cash_flow_projection(data, years):
    """Update cash flow projection chart"""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    # Calculate yearly cash flows
    annual_cash_flow = df['annual_cash_flow'].sum()
    years_list = list(range(1, years + 1))
    cumulative_cash_flow = [annual_cash_flow * year for year in years_list]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years_list,
        y=cumulative_cash_flow,
        mode='lines+markers',
        name='Cumulative Cash Flow',
        line=dict(color='#2ca02c', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Cumulative Cash Flow Projection",
        xaxis_title="Years",
        yaxis_title="Cash Flow ($)",
        hovermode='x unified'
    )
    
    return fig

@app.callback(
    Output("portfolio-growth-chart", "figure"),
    Input("property-data", "data"),
    Input("projection-years", "value")
)
def update_portfolio_growth(data, years):
    """Update portfolio value growth chart"""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    # Calculate portfolio value growth
    total_investment = df['down_payment'].sum()
    annual_cash_flow = df['annual_cash_flow'].sum()
    total_price = df['price'].sum()
    
    years_list = list(range(0, years + 1))
    portfolio_values = []
    
    for year in years_list:
        if year == 0:
            portfolio_values.append(total_investment)
        else:
            cash_flow = annual_cash_flow * year
            appreciation = total_price * (1.03 ** year - 1)  # 3% annual appreciation
            portfolio_value = total_investment + cash_flow + appreciation
            portfolio_values.append(portfolio_value)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years_list,
        y=portfolio_values,
        mode='lines+markers',
        name='Portfolio Value',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Portfolio Value Growth Projection",
        xaxis_title="Years",
        yaxis_title="Portfolio Value ($)",
        hovermode='x unified'
    )
    
    return fig

@app.callback(
    Output("projections-table", "children"),
    Input("property-data", "data"),
    Input("projection-years", "value"),
    Input("min-coc-return", "value"),
    Input("max-investment", "value")
)
def update_projections_table(data, years, min_coc, max_investment):
    """Update detailed projections table"""
    if not data:
        return html.Div("No data available")
    
    df = pd.DataFrame(data)
    
    # Filter properties
    filtered_df = df[
        (df['cash_on_cash_return'] >= min_coc) &
        (df['down_payment'] <= max_investment)
    ]
    
    if len(filtered_df) == 0:
        return html.Div("No properties match the criteria")
    
    # Calculate projections for each property
    projections_data = []
    
    for _, prop in filtered_df.iterrows():
        # Year 0 (initial investment)
        initial_investment = prop['down_payment']
        initial_value = initial_investment
        
        # Year 1 projections
        year1_cash_flow = prop['annual_cash_flow']
        year1_appreciation = prop['price'] * 0.03  # 3% appreciation
        year1_value = initial_value + year1_cash_flow + year1_appreciation
        
        # Year 5 projections
        year5_cash_flow = prop['annual_cash_flow'] * 5
        year5_appreciation = prop['price'] * (1.03 ** 5 - 1)
        year5_value = initial_value + year5_cash_flow + year5_appreciation
        
        # Year 10 projections
        year10_cash_flow = prop['annual_cash_flow'] * 10
        year10_appreciation = prop['price'] * (1.03 ** 10 - 1)
        year10_value = initial_value + year10_cash_flow + year10_appreciation
        
        projections_data.append({
            'Address': prop['address'],
            'Initial Investment': f"${initial_investment:,.0f}",
            'Year 1 Value': f"${year1_value:,.0f}",
            'Year 5 Value': f"${year5_value:,.0f}",
            'Year 10 Value': f"${year10_value:,.0f}",
            'Cash-on-Cash Return': f"{prop['cash_on_cash_return']:.1f}%",
            'Total Return (5Y)': f"{((year5_value - initial_investment) / initial_investment * 100):.1f}%"
        })
    
    # Create table
    if projections_data:
        table = dbc.Table.from_dataframe(
            pd.DataFrame(projections_data),
            striped=True,
            bordered=True,
            hover=True,
            responsive=True,
            className="mt-3"
        )
        return table
    else:
        return html.Div("No projections available")

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
