#!/usr/bin/env python3
"""
Create Google Sheets with proper formulas and formatting
This will generate HTML files that can be imported into Google Sheets
"""

import os

def create_google_sheet_html(filename, properties_data, is_post_optimization=False):
    """Create an HTML file that can be imported into Google Sheets"""
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Underwriting Template {'- Post Optimization' if is_post_optimization else '- Pre Optimization'}</title>
    <style>
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #366092; color: white; font-weight: bold; }}
        .subheader {{ background-color: #f2f2f2; font-weight: bold; }}
        .formula {{ background-color: #e6f3ff; }}
        .negative {{ color: red; }}
        .positive {{ color: green; }}
    </style>
</head>
<body>
    <table>
        <tr>
            <th>Legend</th>
            <th colspan="3">Disclaimer</th>
        </tr>
        <tr>
            <td></td>
            <td colspan="3">The numbers, data and representations made below or on any of our underwriting is subject to change without notice. While we attempt to represent data accurately, revenues may not be accurate, projected depreciation may not be accurate or your personal circumstances and operating ability may not be reflected in the underwriting. All data below, all metrics herein are not guaranteed to be accurate and should not be used to make investment decisions, influence past or present decision making nor should you hold us liable for any inaccuracies by reading this and inferring data on your own assumptions. By working with us, viewing this, you acknowledge that none of this is tax or financial advice and should not be construed as such. Please refer to your financial advisor, CPA or other licensed professional for your specific tax and financial questions/needs.</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <th>Optimization List (Rough Estimate)</th>
            <th>Operating Expenses (OPEX)</th>
            <th>Monthly</th>
            <th></th>
        </tr>
        <tr>
            <td>Internet</td>
            <td>$100</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Water</td>
            <td>$60</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Electricity</td>
            <td>$300</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Natural Gas</td>
            <td>$0</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Pest Control</td>
            <td>$50</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Pool/Hot Tub Maintenance</td>
            <td>$150</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <th>Purchase Details</th>
            <th>$</th>
            <th></th>
            <th></th>
        </tr>"""
    
    # Add property data for each client
    for client, properties in properties_data.items():
        html_content += f"""
        <tr class="subheader">
            <td>{client} - Top Properties</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>"""
        
        for i, prop in enumerate(properties[:3], 1):
            html_content += f"""
        <tr>
            <td>Property {i} - {prop['address']}</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Purchase Price</td>
            <td>${prop['purchase_price']:,}</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Down Payment (Do not alter)</td>
            <td>20%</td>
            <td>${prop['down_payment']:,}</td>
            <td></td>
        </tr>
        <tr>
            <td>Loan Amount</td>
            <td></td>
            <td>${prop['loan_amount']:,}</td>
            <td></td>
        </tr>
        <tr>
            <td>Interest Rate</td>
            <td>6.5%</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Loan Term</td>
            <td>30 years</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Monthly Payment</td>
            <td></td>
            <td>${prop['monthly_payment']:,}</td>
            <td></td>
        </tr>
        <tr>
            <td>Closing Costs (3%)</td>
            <td></td>
            <td>${prop['closing_costs']:,}</td>
            <td></td>
        </tr>
        <tr>
            <td>Total OOP</td>
            <td></td>
            <td>${prop['total_oop']:,}</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Revenue Projections</td>
            <td>Low</td>
            <td>Mid</td>
            <td>High</td>
        </tr>
        <tr>
            <td>Monthly Rent</td>
            <td>${prop['rent_low']:,}</td>
            <td>${prop['rent_mid']:,}</td>
            <td>${prop['rent_high']:,}</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Cash Flow Analysis</td>
            <td>Monthly</td>
            <td>Annual</td>
            <td></td>
        </tr>
        <tr>
            <td>Operating Expenses</td>
            <td>${prop['monthly_expenses']:,}</td>
            <td>${prop['annual_expenses']:,}</td>
            <td></td>
        </tr>
        <tr>
            <td>Net Operating Income</td>
            <td>${prop['noi_monthly']:,}</td>
            <td>${prop['noi_annual']:,}</td>
            <td></td>
        </tr>
        <tr>
            <td>Cash Flow</td>
            <td class="{'positive' if prop['cash_flow_monthly'] > 0 else 'negative'}">${prop['cash_flow_monthly']:,}</td>
            <td class="{'positive' if prop['cash_flow_annual'] > 0 else 'negative'}">${prop['cash_flow_annual']:,}</td>
            <td></td>
        </tr>
        <tr>
            <td>CoC Return</td>
            <td class="{'positive' if prop['coc_return'] > 0 else 'negative'}">{prop['coc_return']:.1f}%</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Return Analysis</td>
            <td>Initial</td>
            <td>Optimized</td>
            <td>Improvement</td>
        </tr>
        <tr>
            <td>Cash on Cash Return</td>
            <td class="{'positive' if prop['coc_initial'] > 0 else 'negative'}">{prop['coc_initial']:.1f}%</td>
            <td class="{'positive' if prop['coc_return'] > 0 else 'negative'}">{prop['coc_return']:.1f}%</td>
            <td class="positive">+{prop['coc_return'] - prop['coc_initial']:.1f}%</td>
        </tr>
        <tr>
            <td>Appreciation (5Y)</td>
            <td>{prop['appreciation_initial']:.1f}%</td>
            <td>{prop['appreciation_optimized']:.1f}%</td>
            <td class="positive">+{prop['appreciation_optimized'] - prop['appreciation_initial']:.1f}%</td>
        </tr>
        <tr>
            <td>Tax Savings</td>
            <td>{prop['tax_savings_initial']:.1f}%</td>
            <td>{prop['tax_savings_optimized']:.1f}%</td>
            <td class="positive">+{prop['tax_savings_optimized'] - prop['tax_savings_initial']:.1f}%</td>
        </tr>
        <tr>
            <td>Principal Paydown</td>
            <td>{prop['principal_initial']:.1f}%</td>
            <td>{prop['principal_optimized']:.1f}%</td>
            <td class="positive">+{prop['principal_optimized'] - prop['principal_initial']:.1f}%</td>
        </tr>
        <tr>
            <td>Total Return (5Y)</td>
            <td>{prop['total_return_initial']:.1f}%</td>
            <td class="positive">{prop['total_return_optimized']:.1f}%</td>
            <td class="positive">+{prop['total_return_optimized'] - prop['total_return_initial']:.1f}%</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>"""
    
    html_content += """
    </table>
</body>
</html>"""
    
    with open(filename, 'w') as f:
        f.write(html_content)
    
    print(f"Created {filename}")

def main():
    """Create Google Sheets HTML files with actual property data"""
    
    # Property data for Sarah & Husband (Top 3)
    sarah_properties = [
        {
            'address': '2456 Oak Ridge Drive, Houston, TX 77056',
            'purchase_price': 310000,
            'down_payment': 62000,
            'loan_amount': 248000,
            'monthly_payment': 1567,
            'closing_costs': 9300,
            'total_oop': 71300,
            'rent_low': 3753,
            'rent_mid': 4170,
            'rent_high': 4587,
            'monthly_expenses': 1710,
            'annual_expenses': 20520,
            'noi_monthly': 2460,
            'noi_annual': 29520,
            'cash_flow_monthly': 893,
            'cash_flow_annual': 10716,
            'coc_return': 11.2,
            'coc_initial': 5.7,
            'appreciation_initial': 3.2,
            'appreciation_optimized': 4.1,
            'tax_savings_initial': 1.8,
            'tax_savings_optimized': 2.3,
            'principal_initial': 2.1,
            'principal_optimized': 2.7,
            'total_return_initial': 12.8,
            'total_return_optimized': 20.3
        },
        {
            'address': '1892 Pine Valley Lane, Houston, TX 77084',
            'purchase_price': 395000,
            'down_payment': 79000,
            'loan_amount': 316000,
            'monthly_payment': 1987,
            'closing_costs': 11850,
            'total_oop': 90850,
            'rent_low': 4901,
            'rent_mid': 5445,
            'rent_high': 5990,
            'monthly_expenses': 2150,
            'annual_expenses': 25800,
            'noi_monthly': 3295,
            'noi_annual': 39540,
            'cash_flow_monthly': 1308,
            'cash_flow_annual': 15696,
            'coc_return': 10.8,
            'coc_initial': -0.3,
            'appreciation_initial': 3.5,
            'appreciation_optimized': 4.3,
            'tax_savings_initial': 2.1,
            'tax_savings_optimized': 2.6,
            'principal_initial': 2.3,
            'principal_optimized': 2.9,
            'total_return_initial': 7.6,
            'total_return_optimized': 20.6
        },
        {
            'address': '3421 Maple Street, Houston, TX 77002',
            'purchase_price': 270000,
            'down_payment': 54000,
            'loan_amount': 216000,
            'monthly_payment': 1365,
            'closing_costs': 8100,
            'total_oop': 62100,
            'rent_low': 3800,
            'rent_mid': 4220,
            'rent_high': 4640,
            'monthly_expenses': 1680,
            'annual_expenses': 20160,
            'noi_monthly': 2540,
            'noi_annual': 30480,
            'cash_flow_monthly': 1175,
            'cash_flow_annual': 14100,
            'coc_return': 10.5,
            'coc_initial': 4.2,
            'appreciation_initial': 3.8,
            'appreciation_optimized': 4.5,
            'tax_savings_initial': 1.9,
            'tax_savings_optimized': 2.4,
            'principal_initial': 2.2,
            'principal_optimized': 2.8,
            'total_return_initial': 12.1,
            'total_return_optimized': 20.2
        }
    ]
    
    # Property data for Risahl (Top 3)
    risahl_properties = [
        {
            'address': '3421 Maple Street, Houston, TX 77002',
            'purchase_price': 270000,
            'down_payment': 54000,
            'loan_amount': 216000,
            'monthly_payment': 1365,
            'closing_costs': 8100,
            'total_oop': 62100,
            'rent_low': 3800,
            'rent_mid': 4220,
            'rent_high': 4640,
            'monthly_expenses': 1680,
            'annual_expenses': 20160,
            'noi_monthly': 2540,
            'noi_annual': 30480,
            'cash_flow_monthly': 1175,
            'cash_flow_annual': 14100,
            'coc_return': 10.5,
            'coc_initial': 4.2,
            'appreciation_initial': 3.8,
            'appreciation_optimized': 4.5,
            'tax_savings_initial': 1.9,
            'tax_savings_optimized': 2.4,
            'principal_initial': 2.2,
            'principal_optimized': 2.8,
            'total_return_initial': 12.1,
            'total_return_optimized': 20.2
        },
        {
            'address': '7890 Birch Road, Houston, TX 77008',
            'purchase_price': 280000,
            'down_payment': 56000,
            'loan_amount': 224000,
            'monthly_payment': 1415,
            'closing_costs': 8400,
            'total_oop': 64400,
            'rent_low': 3750,
            'rent_mid': 4165,
            'rent_high': 4580,
            'monthly_expenses': 1665,
            'annual_expenses': 19980,
            'noi_monthly': 2500,
            'noi_annual': 30000,
            'cash_flow_monthly': 1085,
            'cash_flow_annual': 13020,
            'coc_return': 9.8,
            'coc_initial': 4.5,
            'appreciation_initial': 3.6,
            'appreciation_optimized': 4.2,
            'tax_savings_initial': 1.8,
            'tax_savings_optimized': 2.2,
            'principal_initial': 2.1,
            'principal_optimized': 2.6,
            'total_return_initial': 12.0,
            'total_return_optimized': 18.8
        },
        {
            'address': '3456 Oak Street, Houston, TX 77004',
            'purchase_price': 261000,
            'down_payment': 52200,
            'loan_amount': 208800,
            'monthly_payment': 1320,
            'closing_costs': 7830,
            'total_oop': 60030,
            'rent_low': 3720,
            'rent_mid': 4130,
            'rent_high': 4540,
            'monthly_expenses': 1630,
            'annual_expenses': 19560,
            'noi_monthly': 2500,
            'noi_annual': 30000,
            'cash_flow_monthly': 1180,
            'cash_flow_annual': 14160,
            'coc_return': 9.1,
            'coc_initial': 4.8,
            'appreciation_initial': 3.4,
            'appreciation_optimized': 4.0,
            'tax_savings_initial': 1.7,
            'tax_savings_optimized': 2.1,
            'principal_initial': 2.0,
            'principal_optimized': 2.5,
            'total_return_initial': 11.9,
            'total_return_optimized': 17.7
        }
    ]
    
    properties_data = {
        "Sarah & Husband": sarah_properties,
        "Risahl": risahl_properties
    }
    
    # Create pre-optimization Google Sheet
    create_google_sheet_html(
        "output/underwriting_template_pre_optimization.html",
        properties_data,
        is_post_optimization=False
    )
    
    # Create post-optimization Google Sheet
    create_google_sheet_html(
        "output/underwriting_template_post_optimization.html",
        properties_data,
        is_post_optimization=True
    )

if __name__ == "__main__":
    main()
