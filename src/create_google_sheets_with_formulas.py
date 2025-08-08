#!/usr/bin/env python3
"""
Create Google Sheets with actual formulas and formatting
This will create a template that can be imported into Google Sheets
"""

import csv
import os

def create_google_sheet_with_formulas(filename, properties_data, is_post_optimization=False):
    """Create a CSV file that can be imported into Google Sheets with formulas"""
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Header rows
        writer.writerow(['Legend', 'Disclaimer'])
        writer.writerow(['', 'The numbers, data and representations made below or on any of our underwriting is subject to change without notice. While we attempt to represent data accurately, revenues may not be accurate, projected depreciation may not be accurate or your personal circumstances and operating ability may not be reflected in the underwriting. All data below, all metrics herein are not guaranteed to be accurate and should not be used to make investment decisions, influence past or present decision making nor should you hold us liable for any inaccuracies by reading this and inferring data on your own assumptions. By working with us, viewing this, you acknowledge that none of this is tax or financial advice and should not be construed as such. Please refer to your financial advisor, CPA or other licensed professional for your specific tax and financial questions/needs.'])
        writer.writerow([])
        
        # Optimization List and Operating Expenses
        writer.writerow(['Optimization List (Rough Estimate)', 'Operating Expenses (OPEX)', 'Monthly', ''])
        writer.writerow(['Internet', '100', '', ''])
        writer.writerow(['Water', '60', '', ''])
        writer.writerow(['Electricity', '300', '', ''])
        writer.writerow(['Natural Gas', '0', '', ''])
        writer.writerow(['Pest Control', '50', '', ''])
        writer.writerow(['Pool/Hot Tub Maintenance', '150', '', ''])
        writer.writerow([])
        
        # Purchase Details
        writer.writerow(['Purchase Details', '', '', ''])
        
        # Property data for each client
        for client, properties in properties_data.items():
            writer.writerow([f'{client} - Top Properties', '', '', ''])
            
            for i, prop in enumerate(properties[:3], 1):
                writer.writerow([f'Property {i} - {prop["address"]}', '', '', ''])
                writer.writerow(['Purchase Price', prop['purchase_price'], '', ''])
                writer.writerow(['Down Payment (Do not alter)', '20%', f'=B{writer.line_num-1}*0.2', ''])
                writer.writerow(['Loan Amount', '', f'=B{writer.line_num-2}-C{writer.line_num-1}', ''])
                writer.writerow(['Interest Rate', '6.5%', '', ''])
                writer.writerow(['Loan Term', '30 years', '', ''])
                writer.writerow(['Monthly Payment', '', f'=PMT(0.065/12,360,C{writer.line_num-5})', ''])
                writer.writerow(['Closing Costs (3%)', '', f'=B{writer.line_num-7}*0.03', ''])
                writer.writerow(['Total OOP', '', f'=C{writer.line_num-7}+C{writer.line_num-1}', ''])
                writer.writerow([])
                
                # Revenue Projections
                writer.writerow(['Revenue Projections', 'Low', 'Mid', 'High'])
                writer.writerow(['Monthly Rent', prop['rent_low'], prop['rent_mid'], prop['rent_high']])
                writer.writerow([])
                
                # Cash Flow Analysis
                writer.writerow(['Cash Flow Analysis', 'Monthly', 'Annual', ''])
                writer.writerow(['Operating Expenses', prop['monthly_expenses'], f'=B{writer.line_num-1}*12', ''])
                writer.writerow(['Net Operating Income', f'=B{writer.line_num-7}-B{writer.line_num-1}', f'=C{writer.line_num-1}*12', ''])
                writer.writerow(['Cash Flow', f'=B{writer.line_num-1}-B{writer.line_num-13}', f'=C{writer.line_num-1}*12', ''])
                writer.writerow(['CoC Return', f'=C{writer.line_num-1}/C{writer.line_num-15}', '', ''])
                writer.writerow([])
                
                # Return Analysis
                writer.writerow(['Return Analysis', 'Initial', 'Optimized', 'Improvement'])
                writer.writerow(['Cash on Cash Return', prop['coc_initial'], prop['coc_return'], f'=C{writer.line_num-1}-B{writer.line_num-1}'])
                writer.writerow(['Appreciation (5Y)', prop['appreciation_initial'], prop['appreciation_optimized'], f'=C{writer.line_num-1}-B{writer.line_num-1}'])
                writer.writerow(['Tax Savings', prop['tax_savings_initial'], prop['tax_savings_optimized'], f'=C{writer.line_num-1}-B{writer.line_num-1}'])
                writer.writerow(['Principal Paydown', prop['principal_initial'], prop['principal_optimized'], f'=C{writer.line_num-1}-B{writer.line_num-1}'])
                writer.writerow(['Total Return (5Y)', prop['total_return_initial'], prop['total_return_optimized'], f'=C{writer.line_num-1}-B{writer.line_num-1}'])
                writer.writerow([])
    
    print(f"Created {filename}")

def create_google_sheets_instructions():
    """Create instructions for importing into Google Sheets"""
    
    instructions = """
# Google Sheets Import Instructions

## Step 1: Create New Google Sheet
1. Go to sheets.google.com
2. Click "Blank" to create a new spreadsheet
3. Name it "Underwriting Template - Pre Optimization" or "Post Optimization"

## Step 2: Import CSV Data
1. In your new Google Sheet, go to File > Import
2. Upload the CSV file from the output folder
3. Choose "Replace current sheet"
4. Click "Import data"

## Step 3: Add Formulas (Manual)
After importing, you'll need to add these formulas manually:

### Purchase Details Section:
- Down Payment: =B[Purchase Price Row]*0.2
- Loan Amount: =B[Purchase Price Row]-C[Down Payment Row]
- Monthly Payment: =PMT(0.065/12,360,C[Loan Amount Row])
- Closing Costs: =B[Purchase Price Row]*0.03
- Total OOP: =C[Down Payment Row]+C[Closing Costs Row]

### Cash Flow Analysis:
- Annual Operating Expenses: =B[Monthly Expenses Row]*12
- Net Operating Income: =B[Monthly Rent Row]-B[Monthly Expenses Row]
- Annual NOI: =C[Monthly NOI Row]*12
- Cash Flow: =B[Monthly NOI Row]-B[Monthly Payment Row]
- Annual Cash Flow: =C[Monthly Cash Flow Row]*12
- CoC Return: =C[Annual Cash Flow Row]/C[Total OOP Row]

### Return Analysis:
- Improvement: =C[Optimized Row]-B[Initial Row]

## Step 4: Formatting
1. Select header rows and apply bold formatting
2. Use conditional formatting for positive/negative values
3. Apply currency formatting to monetary values
4. Apply percentage formatting to return values

## Step 5: Share
1. Click "Share" in the top right
2. Set permissions to "Anyone with the link can view"
3. Copy the sharing link for distribution
"""
    
    with open("output/google_sheets_import_instructions.md", "w") as f:
        f.write(instructions)
    
    print("Created google_sheets_import_instructions.md")

def main():
    """Create Google Sheets templates with formulas"""
    
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
    create_google_sheet_with_formulas(
        "output/underwriting_template_pre_optimization_for_google_sheets.csv",
        properties_data,
        is_post_optimization=False
    )
    
    # Create post-optimization template
    create_google_sheet_with_formulas(
        "output/underwriting_template_post_optimization_for_google_sheets.csv",
        properties_data,
        is_post_optimization=True
    )
    
    # Create import instructions
    create_google_sheets_instructions()

if __name__ == "__main__":
    main()
