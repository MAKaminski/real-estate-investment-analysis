# Real Estate Investment Analysis Tool

A comprehensive tool for analyzing real estate investment opportunities by calculating four key return metrics: **Cash on Cash**, **Appreciation**, **Tax Savings**, and **Principal Paydown**.

## Features

### 🏠 Property Data Collection
- **Multiple Data Sources**: Collects property data from Realtor.com API and Zillow web scraping
- **Large Scale Analysis**: Designed to analyze 1,000+ properties per run
- **Automatic Rental Estimates**: Calculates estimated rental income based on property characteristics
- **Duplicate Removal**: Eliminates duplicate properties across data sources

### 📊 Financial Analysis
- **Cash on Cash Return**: Annual cash flow divided by total cash invested
- **Appreciation Return**: Expected annual property value appreciation
- **Tax Savings Return**: Tax benefits from depreciation deductions
- **Principal Paydown Return**: Loan principal reduction through mortgage payments
- **Total Return**: Sum of all four return components

### 📈 Investment Criteria
- **Target Budget**: $20M monthly deployment capacity
- **Property Price Range**: $100K - $300K per property
- **Yield Rate**: 5% of properties expected to fit buy box
- **Sorting**: Properties ranked by total return (highest first)

### 📋 Data Export
- **CSV Export**: Simple comma-separated values format
- **Excel Export**: Multi-sheet workbook with analysis and summary
- **Analysis Report**: Comprehensive text report with key metrics
- **Dashboard**: Interactive web-based visualization

## Project Structure

```
zillow-scrape/
├── src/                    # Source code and configuration
│   ├── main.py            # Main application logic
│   ├── data_collector.py  # Property data collection
│   ├── financial_calculator.py # Financial calculations
│   ├── data_processor.py  # Data processing and export
│   ├── dashboard.py       # Web dashboard
│   ├── config.py          # Configuration settings
│   ├── requirements.txt   # Dependencies
│   └── ...               # Other source files
├── output/                # Generated analysis files
├── .vscode/              # VS Code debug configurations
├── main.py               # Main entry point
├── run_example.py        # Example analysis entry point
├── test_installation.py  # Installation test entry point
├── dashboard.py          # Dashboard entry point
├── setup.py              # Setup entry point
└── README.md             # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Chrome browser (for web scraping)
- Internet connection

### Quick Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd zillow-scrape
```

2. **Run setup script**:
```bash
python setup.py
```

3. **Or install manually**:
```bash
pip install -r src/requirements.txt
```

4. **Set up environment variables** (optional):
Create a `.env` file in the project root:
```bash
# API Keys (optional - tool works without them)
RAPIDAPI_KEY=your_rapidapi_key_here
REALTOR_API_KEY=your_realtor_api_key_here
ZILLOW_API_KEY=your_zillow_api_key_here
OPENCAGE_API_KEY=your_opencage_api_key_here
```

## Usage

## Usage

### Quick Start Commands

```bash
# Test installation
python test_installation.py

# Run example analysis
python run_example.py

# Analyze real properties
python main.py --locations "Dallas, TX" "Austin, TX" --target-count 1000

# Launch web dashboard
python dashboard.py
```

### Command Line Interface

#### Basic Usage
```bash
python main.py --locations "Dallas, TX" "Austin, TX" --target-count 1000
```

#### Advanced Usage
```bash
python main.py \
  --locations "Phoenix, AZ" "Las Vegas, NV" "Miami, FL" \
  --target-count 1500 \
  --output-format xlsx \
  --min-return 15
```

#### Command Line Options
- `--locations`: List of locations to search (required)
- `--target-count`: Number of properties to analyze (default: 1000)
- `--output-format`: Export format - csv, xlsx, or both (default: xlsx)
- `--min-return`: Minimum total return percentage filter (default: 0)
- `--config-file`: Path to custom configuration file (optional)

### Web Dashboard

Launch the interactive dashboard:
```bash
python dashboard.py
```

Then open your browser to: `http://127.0.0.1:8050`

### VS Code Debugging

Use the provided `.vscode/launch.json` configurations:
- **Main Analysis Tool**: Run with default parameters
- **Run Example Analysis**: Execute sample analysis
- **Test Installation**: Verify installation
- **Launch Dashboard**: Start web dashboard
- **Debug Main with Custom Args**: Custom analysis parameters
- **Debug Individual Modules**: Debug specific components

## Output Files

### Excel Export (`property_analysis_YYYYMMDD_HHMMSS.xlsx`)
Contains multiple sheets:
- **Properties**: Complete property data with financial metrics
- **Portfolio_Summary**: Aggregate statistics and metrics
- **Top_Performers**: Top 50 properties by total return
- **Cash_Flow_Analysis**: Properties sorted by monthly cash flow

### CSV Export (`property_analysis_YYYYMMDD_HHMMSS.csv`)
Single file with all property data and financial metrics.

### Analysis Report (`analysis_report_YYYYMMDD_HHMMSS.txt`)
Comprehensive text report including:
- Portfolio summary statistics
- Return metrics breakdown
- Property distribution analysis
- Top 10 properties by total return

## Financial Calculations

### Cash on Cash Return
```
Cash on Cash = (Annual Rental Income - Annual Expenses - Annual Mortgage) / Down Payment
```

### Appreciation Return
```
Appreciation = (Property Price × Annual Appreciation Rate) / Down Payment
```

### Tax Savings Return
```
Tax Savings = (Depreciable Value / 27.5 years × Tax Rate) / Down Payment
```

### Principal Paydown Return
```
Principal Paydown = Annual Principal Reduction / Down Payment
```

### Total Return
```
Total Return = Cash on Cash + Appreciation + Tax Savings + Principal Paydown
```

## Configuration

### Financial Assumptions (config.py)
- **Down Payment**: 20% of property value
- **Interest Rate**: 6.5% (30-year fixed)
- **Appreciation Rate**: 3% annually
- **Tax Rate**: 25%
- **Property Management**: 8% of rental income
- **Insurance**: 0.5% of property value annually
- **Maintenance**: 1% of property value annually
- **Vacancy Rate**: 5%

### Investment Criteria
- **Monthly Budget**: $20,000,000
- **Target Properties**: 100 properties per month
- **Property Price Range**: $100,000 - $300,000
- **Minimum Analysis**: 1,000 properties per run

## Data Sources

### Realtor.com API
- Property listings and details
- Price, square footage, beds/baths
- Property type and year built

### Zillow Web Scraping
- Property listings and pricing
- Address and property details
- Rental estimates

### Rental Income Estimation
- Base rate: $1 per square foot
- Location multipliers (CA: 1.5x, NY: 1.8x, TX: 0.8x)
- Property type adjustments
- Random variation for realism

## Example Output

```
============================================================
REAL ESTATE INVESTMENT ANALYSIS SUMMARY
============================================================
Analysis Date: 2024-01-15 14:30:25
Properties Analyzed: 1,247
Total Investment Required: $49,880,000.00
Total Annual Cash Flow: $3,741,000.00
Portfolio Cash-on-Cash Return: 7.50%

RETURN METRICS:
  Average Total Return: 18.45%
  Average Cash-on-Cash Return: 7.50%
  Average Appreciation Return: 3.00%
  Average Tax Savings Return: 2.75%
  Average Principal Paydown Return: 5.20%

PROPERTY DISTRIBUTION:
  Properties with Positive Cash Flow: 1,180
  Properties with 10%+ Total Return: 1,156
  Properties with 15%+ Total Return: 892
  Properties with 20%+ Total Return: 445

TOP 5 PROPERTIES BY TOTAL RETURN:
  123 Main St, Dallas, TX - 28.5% - $245,000
  456 Oak Ave, Austin, TX - 27.2% - $198,000
  789 Pine Rd, Phoenix, AZ - 26.8% - $267,000
  321 Elm St, Miami, FL - 26.1% - $289,000
  654 Maple Dr, Las Vegas, NV - 25.9% - $223,000

EXPORTED FILES:
  EXCEL: output/property_analysis_20240115_143025.xlsx
  REPORT: output/analysis_report_20240115_143025.txt
============================================================
```

## Troubleshooting

### Common Issues

1. **No properties collected**:
   - The tool will automatically generate sample data if external sources fail
   - Check internet connection for API access
   - Verify location names are correct
   - Try different locations

2. **Web scraping errors**:
   - Selenium WebDriver issues are automatically handled
   - The tool continues with other data sources when scraping fails
   - Ensure Chrome browser is installed for web scraping
   - Check if target websites are accessible

3. **API rate limiting**:
   - Add delays between requests
   - Use API keys for higher limits
   - Reduce target property count
   - The tool will fall back to sample data if APIs are unavailable

4. **Selenium compatibility**:
   - Updated to use new Service-based Chrome driver initialization
   - Compatible with Selenium 4.10.0+
   - Automatic fallback when web scraping fails

### Logs
Check `real_estate_analysis.log` for detailed error messages and debugging information.

### Fallback Mechanism
The tool includes robust fallback mechanisms:
- If web scraping fails, it continues with API data
- If no external data is available, it generates realistic sample data
- All financial calculations work with any data source
- The tool never fails completely - it always produces results

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Development Rules

### Code Organization
- All source code goes in `src/` directory
- Root level contains only entry points and documentation
- Use relative imports from `src/` for all internal modules
- Maintain the four return metrics structure (Cash on Cash, Appreciation, Tax Savings, Principal Paydown)

### Financial Calculations
- All calculations must use `src/config.py` for assumptions
- Preserve the $20M monthly budget and 5% yield rate requirements
- Maintain property price range of $100K-$300K
- Keep the 1,000+ properties per run capability

### Data Processing
- Always sort properties by total return (highest first)
- Export to both CSV and Excel formats when possible
- Generate comprehensive analysis reports
- Include all four return metrics in outputs

### Debugging
- Use VS Code launch configurations in `.vscode/launch.json`
- Test installation with `python test_installation.py`
- Run examples with `python run_example.py`
- Debug individual modules as needed

### File Structure
- Keep entry points in root directory for easy access
- Store all source code in `src/` directory
- Output files go to `output/` directory
- Configuration in `src/config.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and analysis purposes only. Always consult with qualified real estate professionals, accountants, and legal advisors before making investment decisions. The financial calculations are estimates and may not reflect actual market conditions or tax implications.
