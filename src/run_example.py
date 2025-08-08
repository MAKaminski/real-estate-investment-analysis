#!/usr/bin/env python3
"""
Example script demonstrating the Real Estate Investment Analysis Tool
==================================================================

This script shows how to use the tool with sample data and different configurations.
"""

import sys
import os
import logging
from datetime import datetime
import pandas as pd
import numpy as np

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_collector import PropertyDataCollector
from src.data_processor import DataProcessor
from src.financial_calculator import FinancialCalculator
import src.config as config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_properties(n_properties: int = 1000) -> list:
    """Create sample property data for demonstration"""
    logger.info(f"Creating {n_properties} sample properties...")
    
    np.random.seed(42)  # For reproducible results
    
    properties = []
    
    # Sample cities and states
    cities = [
        ("Dallas", "TX"), ("Austin", "TX"), ("Houston", "TX"),
        ("Phoenix", "AZ"), ("Tucson", "AZ"), ("Mesa", "AZ"),
        ("Miami", "FL"), ("Orlando", "FL"), ("Tampa", "FL"),
        ("Las Vegas", "NV"), ("Reno", "NV"), ("Henderson", "NV"),
        ("Atlanta", "GA"), ("Savannah", "GA"), ("Athens", "GA"),
        ("Charlotte", "NC"), ("Raleigh", "NC"), ("Durham", "NC")
    ]
    
    street_names = [
        "Main St", "Oak Ave", "Pine Rd", "Elm St", "Maple Dr",
        "Cedar Ln", "Birch Way", "Willow Ct", "Cherry Blvd", "Poplar St"
    ]
    
    for i in range(n_properties):
        # Random city and state
        city, state = cities[np.random.randint(0, len(cities))]
        
        # Random address
        street_num = np.random.randint(100, 9999)
        street_name = street_names[np.random.randint(0, len(street_names))]
        address = f"{street_num} {street_name}, {city}, {state}"
        
        # Property characteristics
        price = np.random.uniform(150000, 300000)
        sqft = np.random.uniform(1200, 2500)
        beds = np.random.randint(2, 5)
        baths = np.random.randint(1, 4)
        year_built = np.random.randint(1980, 2020)
        
        # Estimate rental income based on characteristics
        base_rent_per_sqft = 1.0
        location_multiplier = 1.0
        
        # Adjust for location
        if state == "CA":
            location_multiplier = 1.5
        elif state == "NY":
            location_multiplier = 1.8
        elif state == "TX":
            location_multiplier = 0.8
        elif state == "FL":
            location_multiplier = 1.2
        elif state == "NV":
            location_multiplier = 0.9
        
        estimated_rent = sqft * base_rent_per_sqft * location_multiplier * np.random.uniform(0.8, 1.2)
        
        property_data = {
            'address': address,
            'price': round(price, 2),
            'sqft': int(sqft),
            'beds': beds,
            'baths': baths,
            'year_built': year_built,
            'property_type': 'Single Family',
            'estimated_rental_income': round(estimated_rent, 2),
            'source': 'sample',
            'listing_id': f"sample_{i}"
        }
        
        properties.append(property_data)
    
    logger.info(f"Created {len(properties)} sample properties")
    return properties

def run_sample_analysis():
    """Run a complete sample analysis"""
    logger.info("Starting sample real estate investment analysis...")
    
    # Step 1: Create sample data
    sample_properties = create_sample_properties(1000)
    
    # Step 2: Process the data
    processor = DataProcessor()
    
    logger.info("Processing sample properties...")
    results = processor.process_and_export(
        properties=sample_properties,
        output_format='xlsx',
        min_total_return=0
    )
    
    # Step 3: Display results
    if results and 'summary' in results:
        summary = results['summary']
        df = results.get('dataframe', None)
        
        print("\n" + "="*60)
        print("SAMPLE REAL ESTATE INVESTMENT ANALYSIS RESULTS")
        print("="*60)
        
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Properties Analyzed: {summary.get('total_properties', 0):,}")
        print(f"Total Investment Required: ${summary.get('total_investment', 0):,.2f}")
        print(f"Total Annual Cash Flow: ${summary.get('total_annual_cash_flow', 0):,.2f}")
        print(f"Portfolio Cash-on-Cash Return: {summary.get('portfolio_cash_on_cash', 0):.2f}%")
        
        print("\nRETURN METRICS:")
        print(f"  Average Total Return: {summary.get('avg_total_return', 0):.2f}%")
        print(f"  Average Cash-on-Cash Return: {summary.get('avg_cash_on_cash', 0):.2f}%")
        print(f"  Average Appreciation Return: {summary.get('avg_appreciation', 0):.2f}%")
        print(f"  Average Tax Savings Return: {summary.get('avg_tax_savings', 0):.2f}%")
        print(f"  Average Principal Paydown Return: {summary.get('avg_principal_paydown', 0):.2f}%")
        
        print("\nPROPERTY DISTRIBUTION:")
        print(f"  Properties with Positive Cash Flow: {summary.get('properties_with_positive_cash_flow', 0)}")
        print(f"  Properties with 10%+ Total Return: {summary.get('properties_with_10_plus_return', 0)}")
        print(f"  Properties with 15%+ Total Return: {summary.get('properties_with_15_plus_return', 0)}")
        print(f"  Properties with 20%+ Total Return: {summary.get('properties_with_20_plus_return', 0)}")
        
        if df is not None and not df.empty:
            print("\nTOP 10 PROPERTIES BY TOTAL RETURN:")
            top_10 = df.head(10)
            for idx, row in top_10.iterrows():
                print(f"  {row['address']} - {row['total_return']:.2f}% - ${row['price']:,.0f}")
        
        if 'export_files' in results:
            print("\nEXPORTED FILES:")
            for file_type, file_path in results['export_files'].items():
                print(f"  {file_type.upper()}: {file_path}")
        
        print("="*60 + "\n")
        
        return results
    else:
        logger.error("No results generated")
        return None

def demonstrate_financial_calculations():
    """Demonstrate the financial calculations with sample properties"""
    logger.info("Demonstrating financial calculations...")
    
    calculator = FinancialCalculator()
    
    # Sample property
    sample_property = {
        'price': 250000,
        'estimated_rental_income': 2200,
        'sqft': 1800,
        'beds': 3,
        'baths': 2,
        'property_type': 'Single Family'
    }
    
    # Calculate all returns
    financial_metrics = calculator.calculate_total_return(sample_property)
    
    print("\n" + "="*50)
    print("FINANCIAL CALCULATION DEMONSTRATION")
    print("="*50)
    
    print(f"Sample Property: {sample_property.get('beds', 0)} bed, {sample_property.get('baths', 0)} bath")
    print(f"Purchase Price: ${sample_property.get('price', 0):,.0f}")
    print(f"Estimated Monthly Rent: ${sample_property.get('estimated_rental_income', 0):,.0f}")
    print(f"Square Footage: {sample_property.get('sqft', 0):,}")
    
    print("\nRETURN CALCULATIONS:")
    print(f"  Cash on Cash Return: {financial_metrics.get('cash_on_cash_return', 0):.2f}%")
    print(f"  Appreciation Return: {financial_metrics.get('appreciation_return', 0):.2f}%")
    print(f"  Tax Savings Return: {financial_metrics.get('tax_savings_return', 0):.2f}%")
    print(f"  Principal Paydown Return: {financial_metrics.get('principal_paydown_return', 0):.2f}%")
    print(f"  Total Return: {financial_metrics.get('total_return', 0):.2f}%")
    
    print("\nCASH FLOW ANALYSIS:")
    print(f"  Monthly Cash Flow: ${financial_metrics.get('monthly_cash_flow', 0):,.2f}")
    print(f"  Annual Cash Flow: ${financial_metrics.get('annual_cash_flow', 0):,.2f}")
    print(f"  Down Payment: ${financial_metrics.get('down_payment', 0):,.2f}")
    print(f"  Loan Amount: ${financial_metrics.get('loan_amount', 0):,.2f}")
    print(f"  Monthly Mortgage: ${financial_metrics.get('monthly_mortgage', 0):,.2f}")
    print(f"  Annual Expenses: ${financial_metrics.get('annual_expenses', 0):,.2f}")
    
    print("="*50 + "\n")

def show_configuration():
    """Display the current configuration settings"""
    print("\n" + "="*50)
    print("CURRENT CONFIGURATION SETTINGS")
    print("="*50)
    
    print("FINANCIAL ASSUMPTIONS:")
    print(f"  Down Payment: {config.DEFAULT_DOWN_PAYMENT_PCT * 100}%")
    print(f"  Interest Rate: {config.DEFAULT_INTEREST_RATE * 100}%")
    print(f"  Loan Term: {config.DEFAULT_LOAN_TERM} years")
    print(f"  Appreciation Rate: {config.DEFAULT_APPRECIATION_RATE * 100}%")
    print(f"  Tax Rate: {config.DEFAULT_TAX_RATE * 100}%")
    print(f"  Property Management Fee: {config.DEFAULT_PROPERTY_MANAGEMENT_FEE * 100}%")
    print(f"  Insurance Rate: {config.DEFAULT_INSURANCE_RATE * 100}%")
    print(f"  Maintenance Rate: {config.DEFAULT_MAINTENANCE_RATE * 100}%")
    print(f"  Vacancy Rate: {config.DEFAULT_VACANCY_RATE * 100}%")
    
    print("\nINVESTMENT CRITERIA:")
    print(f"  Monthly Budget: ${config.MONTHLY_INVESTMENT_BUDGET:,.0f}")
    print(f"  Target Properties per Month: {config.MONTHLY_INVESTMENT_BUDGET / config.TARGET_PROPERTY_PRICE:.0f}")
    print(f"  Property Price Range: ${config.MIN_PROPERTY_PRICE:,.0f} - ${config.MAX_PROPERTY_PRICE:,.0f}")
    print(f"  Target Properties per Run: {config.TARGET_PROPERTIES_PER_RUN}")
    
    print("="*50 + "\n")

def main():
    """Main function to run the example"""
    print("Real Estate Investment Analysis Tool - Example")
    print("="*50)
    
    try:
        # Show configuration
        show_configuration()
        
        # Demonstrate financial calculations
        demonstrate_financial_calculations()
        
        # Run sample analysis
        results = run_sample_analysis()
        
        if results:
            print("✅ Sample analysis completed successfully!")
            print("📊 Check the 'output' directory for exported files")
            print("🌐 Run 'python dashboard.py' to view the interactive dashboard")
        else:
            print("❌ Sample analysis failed")
            return 1
            
    except Exception as e:
        logger.error(f"Error running example: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
