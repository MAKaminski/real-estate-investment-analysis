import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
REALTOR_API_KEY = os.getenv('REALTOR_API_KEY', '')
ZILLOW_API_KEY = os.getenv('ZILLOW_API_KEY', '')
OPENCAGE_API_KEY = os.getenv('OPENCAGE_API_KEY', '')

# Financial Assumptions
DEFAULT_DOWN_PAYMENT_PCT = 0.20  # 20% down payment
DEFAULT_INTEREST_RATE = 0.065    # 6.5% interest rate
DEFAULT_LOAN_TERM = 30           # 30-year loan
DEFAULT_APPRECIATION_RATE = 0.03 # 3% annual appreciation
DEFAULT_TAX_RATE = 0.25          # 25% tax rate
DEFAULT_DEPRECIATION_RATE = 0.0275  # 27.5 years straight-line depreciation
DEFAULT_PROPERTY_MANAGEMENT_FEE = 0.08  # 8% of rental income
DEFAULT_INSURANCE_RATE = 0.005   # 0.5% of property value annually
DEFAULT_MAINTENANCE_RATE = 0.01  # 1% of property value annually
DEFAULT_VACANCY_RATE = 0.05      # 5% vacancy rate

# Property Search Settings
MIN_PROPERTIES_PER_RUN = 1000
MAX_PROPERTIES_PER_RUN = 2000
TARGET_PROPERTIES_PER_RUN = 1000

# Investment Criteria
MAX_PROPERTY_PRICE = 300000      # Maximum property price to consider
MIN_PROPERTY_PRICE = 100000      # Minimum property price to consider
TARGET_PROPERTY_PRICE = 200000   # Target property price
MONTHLY_INVESTMENT_BUDGET = 20000000  # $20M monthly budget

# Data Sources
DATA_SOURCES = {
    'realtor': {
        'base_url': 'https://realtor.p.rapidapi.com',
        'headers': {
            'X-RapidAPI-Key': os.getenv('RAPIDAPI_KEY', ''),
            'X-RapidAPI-Host': 'realtor.p.rapidapi.com'
        }
    },
    'zillow': {
        'base_url': 'https://zillow56.p.rapidapi.com',
        'headers': {
            'X-RapidAPI-Key': os.getenv('RAPIDAPI_KEY', ''),
            'X-RapidAPI-Host': 'zillow56.p.rapidapi.com'
        }
    }
}

# Output Settings
OUTPUT_FORMATS = ['csv', 'xlsx']
DEFAULT_OUTPUT_FORMAT = 'xlsx'
OUTPUT_DIR = 'output'
