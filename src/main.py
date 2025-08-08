#!/usr/bin/env python3
"""
Real Estate Investment Analysis Tool
====================================

This tool analyzes real estate properties for investment opportunities by:
1. Collecting property data from multiple sources
2. Calculating four key return metrics: Cash on Cash, Appreciation, Tax Savings, Principal Paydown
3. Sorting properties by total return
4. Exporting results to CSV/XLSX format

Usage:
    python main.py --locations "Dallas, TX" "Austin, TX" --target-count 1000 --output-format xlsx
"""

import argparse
import logging
import sys
import time
from datetime import datetime
from typing import List, Dict
import os

from src.data_collector import PropertyDataCollector
from src.data_processor import DataProcessor
import src.config as config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('real_estate_analysis.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class RealEstateAnalyzer:
    def __init__(self):
        self.data_collector = PropertyDataCollector()
        self.data_processor = DataProcessor()
    
    def run_analysis(self, locations: List[str], target_count: int = 1000, 
                    output_format: str = 'xlsx', min_total_return: float = 0) -> Dict:
        """
        Run the complete real estate investment analysis
        
        Args:
            locations: List of locations to search for properties
            target_count: Number of properties to analyze
            output_format: 'csv' or 'xlsx'
            min_total_return: Minimum total return filter
            
        Returns:
            Dictionary containing analysis results and file paths
        """
        start_time = time.time()
        logger.info(f"Starting real estate analysis for {len(locations)} locations")
        logger.info(f"Target properties: {target_count}")
        logger.info(f"Output format: {output_format}")
        
        try:
            # Step 1: Collect property data
            logger.info("Step 1: Collecting property data...")
            properties = self.data_collector.collect_property_data(
                locations=locations,
                target_count=target_count
            )
            
            if not properties:
                logger.error("No properties collected. Exiting.")
                return {}
            
            logger.info(f"Collected {len(properties)} properties")
            
            # Step 2: Process and analyze properties
            logger.info("Step 2: Processing and analyzing properties...")
            results = self.data_processor.process_and_export(
                properties=properties,
                output_format=output_format,
                min_total_return=min_total_return
            )
            
            # Step 3: Generate summary
            logger.info("Step 3: Generating summary...")
            self._print_summary(results)
            
            # Step 4: Calculate execution time
            execution_time = time.time() - start_time
            logger.info(f"Analysis completed in {execution_time:.2f} seconds")
            
            return results
            
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            raise
    
    def _print_summary(self, results: Dict):
        """Print analysis summary to console"""
        if not results or 'summary' not in results:
            logger.warning("No results to summarize")
            return
        
        summary = results['summary']
        df = results.get('dataframe', None)
        
        print("\n" + "="*60)
        print("REAL ESTATE INVESTMENT ANALYSIS SUMMARY")
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
            print("\nTOP 5 PROPERTIES BY TOTAL RETURN:")
            top_5 = df.head(5)
            for idx, row in top_5.iterrows():
                print(f"  {row['address']} - {row['total_return']:.2f}% - ${row['price']:,.0f}")
        
        if 'export_files' in results:
            print("\nEXPORTED FILES:")
            for file_type, file_path in results['export_files'].items():
                print(f"  {file_type.upper()}: {file_path}")
        
        print("="*60 + "\n")

def main():
    """Main function to run the real estate analysis tool"""
    parser = argparse.ArgumentParser(
        description="Real Estate Investment Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --locations "Dallas, TX" "Austin, TX" --target-count 1000
  python main.py --locations "Miami, FL" --target-count 500 --output-format csv
  python main.py --locations "Phoenix, AZ" "Las Vegas, NV" --min-return 15
        """
    )
    
    parser.add_argument(
        '--locations',
        nargs='+',
        required=True,
        help='List of locations to search for properties (e.g., "Dallas, TX" "Austin, TX")'
    )
    
    parser.add_argument(
        '--target-count',
        type=int,
        default=config.TARGET_PROPERTIES_PER_RUN,
        help=f'Number of properties to analyze (default: {config.TARGET_PROPERTIES_PER_RUN})'
    )
    
    parser.add_argument(
        '--output-format',
        choices=['csv', 'xlsx', 'both'],
        default=config.DEFAULT_OUTPUT_FORMAT,
        help=f'Output format (default: {config.DEFAULT_OUTPUT_FORMAT})'
    )
    
    parser.add_argument(
        '--min-return',
        type=float,
        default=0,
        help='Minimum total return percentage to include in results (default: 0)'
    )
    
    parser.add_argument(
        '--config-file',
        help='Path to configuration file (optional)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.target_count < 100:
        logger.warning("Target count is very low. Consider increasing for better analysis.")
    
    if args.target_count > 5000:
        logger.warning("Target count is very high. This may take a long time to complete.")
    
    # Create analyzer and run analysis
    analyzer = RealEstateAnalyzer()
    
    try:
        results = analyzer.run_analysis(
            locations=args.locations,
            target_count=args.target_count,
            output_format=args.output_format,
            min_total_return=args.min_return
        )
        
        if results:
            logger.info("Analysis completed successfully!")
            return 0
        else:
            logger.error("Analysis failed to produce results")
            return 1
            
    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Analysis failed with error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
