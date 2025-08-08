#!/usr/bin/env python3
"""
Test script to verify installation and basic functionality
========================================================

This script tests that all dependencies are installed and the basic
components of the real estate analysis tool work correctly.
"""

import sys
import os
import importlib
import traceback

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    required_modules = [
        'requests',
        'pandas',
        'numpy',
        'openpyxl',
        'beautifulsoup4',
        'selenium',
        'lxml',
        'matplotlib',
        'seaborn',
        'plotly',
        'dash',
        'dash_bootstrap_components',
        'python-dotenv',
        'schedule',
        'webdriver-manager',
        'fake-useragent',
        'timeout-decorator',
        'retrying'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            # Handle modules with different import names
            if module == 'beautifulsoup4':
                importlib.import_module('bs4')
            elif module == 'python-dotenv':
                importlib.import_module('dotenv')
            elif module == 'webdriver-manager':
                importlib.import_module('webdriver_manager')
            elif module == 'fake-useragent':
                importlib.import_module('fake_useragent')
            elif module == 'timeout-decorator':
                importlib.import_module('timeout_decorator')
            else:
                importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import {len(failed_imports)} modules:")
        for module in failed_imports:
            print(f"    - {module}")
        return False
    else:
        print("\n✅ All imports successful!")
        return True

def test_local_modules():
    """Test that our local modules can be imported"""
    print("\nTesting local modules...")
    
    local_modules = [
        'src.config',
        'src.data_collector',
        'src.data_processor', 
        'src.financial_calculator'
    ]
    
    failed_imports = []
    
    for module in local_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import {len(failed_imports)} local modules:")
        for module in failed_imports:
            print(f"    - {module}")
        return False
    else:
        print("\n✅ All local modules imported successfully!")
        return True

def test_financial_calculator():
    """Test the financial calculator with sample data"""
    print("\nTesting financial calculator...")
    
    try:
        from src.financial_calculator import FinancialCalculator
        
        calculator = FinancialCalculator()
        
        # Test property
        test_property = {
            'price': 250000,
            'estimated_rental_income': 2200,
            'sqft': 1800,
            'beds': 3,
            'baths': 2
        }
        
        # Calculate returns
        results = calculator.calculate_total_return(test_property)
        
        # Verify results
        required_keys = [
            'cash_on_cash_return',
            'appreciation_return', 
            'tax_savings_return',
            'principal_paydown_return',
            'total_return'
        ]
        
        missing_keys = []
        for key in required_keys:
            if key not in results:
                missing_keys.append(key)
        
        if missing_keys:
            print(f"  ❌ Missing keys in results: {missing_keys}")
            return False
        
        print(f"  ✅ Cash on Cash Return: {results['cash_on_cash_return']:.2f}%")
        print(f"  ✅ Appreciation Return: {results['appreciation_return']:.2f}%")
        print(f"  ✅ Tax Savings Return: {results['tax_savings_return']:.2f}%")
        print(f"  ✅ Principal Paydown Return: {results['principal_paydown_return']:.2f}%")
        print(f"  ✅ Total Return: {results['total_return']:.2f}%")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Financial calculator test failed: {e}")
        traceback.print_exc()
        return False

def test_data_processor():
    """Test the data processor with sample data"""
    print("\nTesting data processor...")
    
    try:
        from src.data_processor import DataProcessor
        
        processor = DataProcessor()
        
        # Create sample properties
        sample_properties = [
            {
                'address': '123 Main St, Dallas, TX',
                'price': 250000,
                'sqft': 1800,
                'beds': 3,
                'baths': 2,
                'year_built': 2010,
                'property_type': 'Single Family',
                'estimated_rental_income': 2200,
                'source': 'test',
                'listing_id': 'test_1'
            },
            {
                'address': '456 Oak Ave, Austin, TX',
                'price': 300000,
                'sqft': 2200,
                'beds': 4,
                'baths': 3,
                'year_built': 2015,
                'property_type': 'Single Family',
                'estimated_rental_income': 2800,
                'source': 'test',
                'listing_id': 'test_2'
            }
        ]
        
        # Process properties
        df = processor.process_properties(sample_properties)
        
        if df.empty:
            print("  ❌ No data processed")
            return False
        
        print(f"  ✅ Processed {len(df)} properties")
        print(f"  ✅ DataFrame shape: {df.shape}")
        
        # Check for required columns
        required_columns = [
            'address', 'price', 'total_return', 'cash_on_cash_return',
            'appreciation_return', 'tax_savings_return', 'principal_paydown_return'
        ]
        
        missing_columns = []
        for col in required_columns:
            if col not in df.columns:
                missing_columns.append(col)
        
        if missing_columns:
            print(f"  ❌ Missing columns: {missing_columns}")
            return False
        
        print("  ✅ All required columns present")
        return True
        
    except Exception as e:
        print(f"  ❌ Data processor test failed: {e}")
        traceback.print_exc()
        return False

def test_config():
    """Test that configuration is loaded correctly"""
    print("\nTesting configuration...")
    
    try:
        import src.config as config
        
        # Check that key configuration values exist
        required_configs = [
            'DEFAULT_DOWN_PAYMENT_PCT',
            'DEFAULT_INTEREST_RATE',
            'DEFAULT_LOAN_TERM',
            'DEFAULT_APPRECIATION_RATE',
            'TARGET_PROPERTIES_PER_RUN',
            'MIN_PROPERTY_PRICE',
            'MAX_PROPERTY_PRICE',
            'MONTHLY_INVESTMENT_BUDGET'
        ]
        
        missing_configs = []
        for config_name in required_configs:
            if not hasattr(config, config_name):
                missing_configs.append(config_name)
        
        if missing_configs:
            print(f"  ❌ Missing configuration values: {missing_configs}")
            return False
        
        print(f"  ✅ Down Payment: {config.DEFAULT_DOWN_PAYMENT_PCT * 100}%")
        print(f"  ✅ Interest Rate: {config.DEFAULT_INTEREST_RATE * 100}%")
        print(f"  ✅ Loan Term: {config.DEFAULT_LOAN_TERM} years")
        print(f"  ✅ Target Properties: {config.TARGET_PROPERTIES_PER_RUN}")
        print(f"  ✅ Monthly Budget: ${config.MONTHLY_INVESTMENT_BUDGET:,.0f}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration test failed: {e}")
        traceback.print_exc()
        return False

def test_output_directory():
    """Test that output directory can be created"""
    print("\nTesting output directory...")
    
    try:
        import src.config as config
        
        output_dir = config.OUTPUT_DIR
        
        # Create directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"  ✅ Created output directory: {output_dir}")
        else:
            print(f"  ✅ Output directory exists: {output_dir}")
        
        # Test that we can write to it
        test_file = os.path.join(output_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        
        os.remove(test_file)
        print("  ✅ Write permissions verified")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Output directory test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Real Estate Investment Analysis Tool - Installation Test")
    print("="*60)
    
    tests = [
        ("Import Dependencies", test_imports),
        ("Local Modules", test_local_modules),
        ("Configuration", test_config),
        ("Output Directory", test_output_directory),
        ("Financial Calculator", test_financial_calculator),
        ("Data Processor", test_data_processor)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "="*60)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! Installation is complete.")
        print("\nNext steps:")
        print("1. Run 'python run_example.py' to see a sample analysis")
        print("2. Run 'python main.py --locations \"Dallas, TX\" --target-count 100' to analyze real properties")
        print("3. Run 'python dashboard.py' to launch the web dashboard")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check that all Python files are in the same directory")
        print("3. Verify Python version is 3.8 or higher")
        return 1

if __name__ == "__main__":
    sys.exit(main())
