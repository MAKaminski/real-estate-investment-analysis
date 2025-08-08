#!/usr/bin/env python3
"""
Create CSV templates that can be opened in Numbers, Excel, or Google Sheets
"""

import csv
import os

def create_csv_template(filename, properties_data, is_post_optimization=False):
    """Create a CSV file with the underwriting template structure"""
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Header rows
        writer.writerow(['Legend', 'Disclaimer'])
        writer.writerow(['', 'The numbers, data and representations made below or on any of our underwriting is subject to change without notice. While we attempt to represent data accurately, revenues may not be accurate, projected depreciation may not be accurate or your personal circumstances and operating ability may not be reflected in the underwriting. All data below, all metrics herein are not guaranteed to be accurate and should not be used to make investment decisions, influence past or present decision making nor should you hold us liable for any inaccuracies by reading this and inferring data on your own assumptions. By working with us, viewing this, you acknowledge that none of this is tax or financial advice and should not be construed as such. Please refer to your financial advisor, CPA or other licensed professional for your specific tax and financial questions/needs.'])
        writer.writerow([])
        
        # Optimization List and Operating Expenses
        writer.writerow(['Optimization List (Rough Estimate)', 'Operating Expenses (OPEX)', 'Monthly'])
        writer.writerow(['Internet', '$100', ''])
        writer.writerow(['Water', '$60', ''])
        writer.writerow(['Electricity', '$300', ''])
        writer.writerow(['Natural Gas', '$0', ''])
        writer.writerow(['Pest Control', '$50', ''])
        writer.writerow(['Pool/Hot Tub Maintenance', '$150', ''])
        writer.writerow([])
        
        # Purchase Details
        writer.writerow(['Purchase Details', '$', ''])
        
        # Property data for each client
        for client, properties in properties_data.items():
            writer.writerow([f'{client} - Top Properties', '', ''])
            
            for i, prop in enumerate(properties[:3], 1):
                writer.writerow([f'Property {i} - {prop["address"]}', '', ''])
                writer.writerow(['Purchase Price', f'${prop["purchase_price"]:,}', ''])
                writer.writerow(['Down Payment (Do not alter)', '20%', f'${prop["down_payment"]:,}'])
                writer.writerow(['Loan Amount', '', f'${prop["loan_amount"]:,}'])
                writer.writerow(['Interest Rate', '6.5%', ''])
                writer.writerow(['Loan Term', '30 years', ''])
                writer.writerow(['Monthly Payment', '', f'${prop["monthly_payment"]:,}'])
                writer.writerow(['Closing Costs (3%)', '', f'${prop["closing_costs"]:,}'])
                writer.writerow(['Total OOP', '', f'${prop["total_oop"]:,}'])
                writer.writerow([])
                
                # Revenue Projections
                writer.writerow(['Revenue Projections', 'Low', 'Mid', 'High'])
                writer.writerow(['Monthly Rent', f'${prop["rent_low"]:,}', f'${prop["rent_mid"]:,}', f'${prop["rent_high"]:,}'])
                writer.writerow([])
                
                # Cash Flow Analysis
                writer.writerow(['Cash Flow Analysis', 'Monthly', 'Annual'])
                writer.writerow(['Operating Expenses', f'${prop["monthly_expenses"]:,}', f'${prop["annual_expenses"]:,}'])
                writer.writerow(['Net Operating Income', f'${prop["noi_monthly"]:,}', f'${prop["noi_annual"]:,}'])
                writer.writerow(['Cash Flow', f'${prop["cash_flow_monthly"]:,}', f'${prop["cash_flow_annual"]:,}'])
                writer.writerow(['CoC Return', f'{prop["coc_return"]:.1f}%', ''])
                writer.writerow([])
                
                # Return Analysis
                writer.writerow(['Return Analysis', 'Initial', 'Optimized'])
                writer.writerow(['Cash on Cash Return', f'{prop["coc_initial"]:.1f}%', f'{prop["coc_return"]:.1f}%'])
                writer.writerow(['Appreciation (5Y)', f'{prop["appreciation_initial"]:.1f}%', f'{prop["appreciation_optimized"]:.1f}%'])
                writer.writerow(['Tax Savings', f'{prop["tax_savings_initial"]:.1f}%', f'{prop["tax_savings_optimized"]:.1f}%'])
                writer.writerow(['Principal Paydown', f'{prop["principal_initial"]:.1f}%', f'{prop["principal_optimized"]:.1f}%'])
                writer.writerow(['Total Return (5Y)', f'{prop["total_return_initial"]:.1f}%', f'{prop["total_return_optimized"]:.1f}%'])
                writer.writerow([])
    
    print(f"Created {filename}")

def main():
    """Create the CSV templates with actual property data"""
    
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
    
    # Create pre-optimization template
    create_csv_template(
        "output/underwriting_template_pre_optimization.csv",
        properties_data,
        is_post_optimization=False
    )
    
    # Create post-optimization template
    create_csv_template(
        "output/underwriting_template_post_optimization.csv",
        properties_data,
        is_post_optimization=True
    )

if __name__ == "__main__":
    main()
