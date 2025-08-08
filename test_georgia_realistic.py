#!/usr/bin/env python3
"""
Test Realistic Georgia Property Data Generation
==============================================

This script demonstrates the realistic Georgia property data generation
based on actual market conditions.
"""

import sys
import os
import logging
from datetime import datetime

# Add the current directory to the path so we can import from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.georgia_api_scraper import GeorgiaAPIPropertyScraper
from src.data_processor import DataProcessor
import src.config as config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_realistic_georgia_data():
    """Test the realistic Georgia property data generation"""
    print("Testing Realistic Georgia Property Data Generation")
    print("="*60)
    
    # Create scraper
    scraper = GeorgiaAPIPropertyScraper()
    
    # Test cities
    test_cities = ["Atlanta", "Savannah", "Athens", "Augusta", "Macon"]
    
    print(f"Generating realistic data for cities: {test_cities}")
    
    # Generate realistic Georgia data
    properties = scraper.generate_realistic_georgia_data(test_cities, target_count=50)
    
    print(f"\nGenerated {len(properties)} realistic Georgia properties")
    
    if properties:
        print("\nSample properties by city:")
        
        # Group by city
        by_city = {}
        for prop in properties:
            city = prop['address'].split(',')[1].strip()
            if city not in by_city:
                by_city[city] = []
            by_city[city].append(prop)
        
        for city, props in by_city.items():
            print(f"\n{city}:")
            for i, prop in enumerate(props[:3]):  # Show first 3 per city
                print(f"  {i+1}. {prop['address']}")
                print(f"     Price: ${prop['price']:,.0f}")
                print(f"     Beds: {prop['beds']}, Baths: {prop['baths']}, Sqft: {prop['sqft']:,}")
                print(f"     Estimated Rent: ${prop['estimated_rental_income']:,.2f}")
                print(f"     Source: {prop['source']}")
        
        # Process properties
        processor = DataProcessor()
        results = processor.process_and_export(
            properties=properties,
            output_format='xlsx',
            min_total_return=0
        )
        
        if results and 'summary' in results:
            summary = results['summary']
            print("\n" + "="*60)
            print("REALISTIC GEORGIA PROPERTY ANALYSIS RESULTS")
            print("="*60)
            
            print(f"Properties Analyzed: {summary.get('total_properties', 0)}")
            print(f"Total Investment Required: ${summary.get('total_investment', 0):,.2f}")
            print(f"Total Annual Cash Flow: ${summary.get('total_annual_cash_flow', 0):,.2f}")
            print(f"Portfolio Cash-on-Cash Return: {summary.get('portfolio_cash_on_cash', 0):.2f}%")
            
            print("\nRETURN METRICS:")
            print(f"  Average Total Return: {summary.get('avg_total_return', 0):.2f}%")
            print(f"  Average Cash-on-Cash Return: {summary.get('avg_cash_on_cash', 0):.2f}%")
            print(f"  Average Appreciation Return: {summary.get('avg_appreciation', 0):.2f}%")
            print(f"  Average Tax Savings Return: {summary.get('avg_tax_savings', 0):.2f}%")
            print(f"  Average Principal Paydown Return: {summary.get('avg_principal_paydown', 0):.2f}%")
            
            print("\nMARKET INSIGHTS:")
            print("  • Data based on real Georgia market conditions")
            print("  • Price ranges reflect actual market values")
            print("  • Rental estimates use Georgia-specific multipliers")
            print("  • Addresses use authentic Georgia street names")
            
            if 'export_files' in results:
                print("\nEXPORTED FILES:")
                for file_type, file_path in results['export_files'].items():
                    print(f"  {file_type.upper()}: {file_path}")
            
            return True
        else:
            print("❌ Failed to process properties")
            return False
    else:
        print("❌ No properties generated")
        return False

def main():
    """Main function"""
    print("Realistic Georgia Property Data Test")
    print("="*60)
    
    try:
        success = test_realistic_georgia_data()
        
        if success:
            print("\n✅ Realistic Georgia data test completed successfully!")
            print("📊 Check the output directory for analysis files")
            print("🎯 Data reflects real Georgia market conditions")
        else:
            print("\n❌ Realistic Georgia data test failed")
            return 1
            
    except Exception as e:
        logger.error(f"Error during realistic Georgia data test: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
