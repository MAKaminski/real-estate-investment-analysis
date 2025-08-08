#!/usr/bin/env python3
"""
Test script for Georgia Property Scraper
========================================

This script tests the dedicated Georgia property scraper to ensure it can
collect real property data from Georgia cities.
"""

import sys
import os
import logging
from datetime import datetime

# Add the current directory to the path so we can import from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.georgia_scraper import GeorgiaPropertyScraper
from src.data_processor import DataProcessor
import src.config as config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_georgia_scraper():
    """Test the Georgia property scraper"""
    print("Testing Georgia Property Scraper")
    print("="*50)
    
    # Create scraper
    scraper = GeorgiaPropertyScraper()
    
    # Test cities
    test_cities = ["Atlanta", "Savannah", "Athens"]
    
    print(f"Testing cities: {test_cities}")
    print("This may take a few minutes...")
    
    # Scrape properties
    properties = scraper.scrape_georgia_properties(test_cities, target_count=50)
    
    print(f"\nCollected {len(properties)} properties")
    
    if properties:
        print("\nSample properties:")
        for i, prop in enumerate(properties[:5]):
            print(f"{i+1}. {prop.get('address', 'N/A')}")
            print(f"   Price: ${prop.get('price', 0):,}")
            print(f"   Beds: {prop.get('beds', 0)}, Baths: {prop.get('baths', 0)}")
            print(f"   Sqft: {prop.get('sqft', 0):,}")
            print(f"   Estimated Rent: ${prop.get('estimated_rental_income', 0):,.2f}")
            print(f"   Source: {prop.get('source', 'N/A')}")
            print()
        
        # Process properties
        processor = DataProcessor()
        results = processor.process_and_export(
            properties=properties,
            output_format='xlsx',
            min_total_return=0
        )
        
        if results and 'summary' in results:
            summary = results['summary']
            print("="*50)
            print("GEORGIA PROPERTY ANALYSIS RESULTS")
            print("="*50)
            
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
            
            if 'export_files' in results:
                print("\nEXPORTED FILES:")
                for file_type, file_path in results['export_files'].items():
                    print(f"  {file_type.upper()}: {file_path}")
            
            return True
        else:
            print("❌ Failed to process properties")
            return False
    else:
        print("❌ No properties collected")
        return False

def main():
    """Main function"""
    print("Georgia Property Scraper Test")
    print("="*50)
    
    try:
        success = test_georgia_scraper()
        
        if success:
            print("\n✅ Georgia scraper test completed successfully!")
            print("📊 Check the output directory for analysis files")
        else:
            print("\n❌ Georgia scraper test failed")
            return 1
            
    except Exception as e:
        logger.error(f"Error during Georgia scraper test: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
