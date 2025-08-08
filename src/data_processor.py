import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import os
from datetime import datetime
import logging
from src.financial_calculator import FinancialCalculator
import src.config as config

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self):
        self.calculator = FinancialCalculator()
        self.output_dir = config.OUTPUT_DIR
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def process_properties(self, properties: List[Dict]) -> pd.DataFrame:
        """Process properties and calculate financial metrics"""
        logger.info(f"Processing {len(properties)} properties...")
        
        processed_properties = []
        
        for i, prop in enumerate(properties):
            try:
                # Calculate financial metrics
                financial_metrics = self.calculator.calculate_total_return(prop)
                
                # Combine property data with financial metrics
                processed_prop = {
                    'address': prop.get('address', ''),
                    'price': prop.get('price', 0),
                    'sqft': prop.get('sqft', 0),
                    'beds': prop.get('beds', 0),
                    'baths': prop.get('baths', 0),
                    'year_built': prop.get('year_built', 0),
                    'property_type': prop.get('property_type', ''),
                    'estimated_rental_income': prop.get('estimated_rental_income', 0),
                    'source': prop.get('source', ''),
                    'listing_id': prop.get('listing_id', ''),
                    
                    # Financial metrics
                    'cash_on_cash_return': financial_metrics.get('cash_on_cash_return', 0),
                    'appreciation_return': financial_metrics.get('appreciation_return', 0),
                    'tax_savings_return': financial_metrics.get('tax_savings_return', 0),
                    'principal_paydown_return': financial_metrics.get('principal_paydown_return', 0),
                    'total_return': financial_metrics.get('total_return', 0),
                    'monthly_cash_flow': financial_metrics.get('monthly_cash_flow', 0),
                    'annual_cash_flow': financial_metrics.get('annual_cash_flow', 0),
                    'down_payment': financial_metrics.get('down_payment', 0),
                    'loan_amount': financial_metrics.get('loan_amount', 0),
                    'monthly_mortgage': financial_metrics.get('monthly_mortgage', 0),
                    'annual_expenses': financial_metrics.get('annual_expenses', 0),
                    'annual_rent': financial_metrics.get('annual_rent', 0)
                }
                
                processed_properties.append(processed_prop)
                
                if (i + 1) % 100 == 0:
                    logger.info(f"Processed {i + 1} properties...")
                    
            except Exception as e:
                logger.error(f"Error processing property {i}: {e}")
                continue
        
        # Convert to DataFrame
        df = pd.DataFrame(processed_properties)
        
        # Sort by total return (highest first)
        df = df.sort_values('total_return', ascending=False)
        
        logger.info(f"Successfully processed {len(df)} properties")
        return df
    
    def filter_properties(self, df: pd.DataFrame, min_total_return: float = 0) -> pd.DataFrame:
        """Filter properties based on criteria"""
        filtered_df = df.copy()
        
        # Filter by minimum total return
        if min_total_return > 0:
            filtered_df = filtered_df[filtered_df['total_return'] >= min_total_return]
        
        # Filter by price range
        filtered_df = filtered_df[
            (filtered_df['price'] >= config.MIN_PROPERTY_PRICE) &
            (filtered_df['price'] <= config.MAX_PROPERTY_PRICE)
        ]
        
        # Filter by positive cash flow
        filtered_df = filtered_df[filtered_df['monthly_cash_flow'] > 0]
        
        logger.info(f"Filtered to {len(filtered_df)} properties")
        return filtered_df
    
    def calculate_portfolio_summary(self, df: pd.DataFrame) -> Dict:
        """Calculate portfolio summary statistics"""
        if df.empty:
            return {}
        
        summary = {
            'total_properties': len(df),
            'total_investment': df['down_payment'].sum(),
            'total_annual_cash_flow': df['annual_cash_flow'].sum(),
            'total_annual_return': df['total_return'].sum(),
            'avg_total_return': df['total_return'].mean(),
            'avg_cash_on_cash': df['cash_on_cash_return'].mean(),
            'avg_appreciation': df['appreciation_return'].mean(),
            'avg_tax_savings': df['tax_savings_return'].mean(),
            'avg_principal_paydown': df['principal_paydown_return'].mean(),
            'avg_property_price': df['price'].mean(),
            'avg_monthly_cash_flow': df['monthly_cash_flow'].mean(),
            'portfolio_cash_on_cash': (df['annual_cash_flow'].sum() / df['down_payment'].sum() * 100) if df['down_payment'].sum() > 0 else 0,
            'properties_with_positive_cash_flow': len(df[df['monthly_cash_flow'] > 0]),
            'properties_with_10_plus_return': len(df[df['total_return'] >= 10]),
            'properties_with_15_plus_return': len(df[df['total_return'] >= 15]),
            'properties_with_20_plus_return': len(df[df['total_return'] >= 20])
        }
        
        return summary
    
    def export_to_csv(self, df: pd.DataFrame, filename: Optional[str] = None) -> str:
        """Export DataFrame to CSV"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"property_analysis_{timestamp}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        df.to_csv(filepath, index=False)
        logger.info(f"Exported {len(df)} properties to {filepath}")
        return filepath
    
    def export_to_excel(self, df: pd.DataFrame, summary: Dict, filename: Optional[str] = None) -> str:
        """Export DataFrame to Excel with multiple sheets"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"property_analysis_{timestamp}.xlsx"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Main properties sheet
            df.to_excel(writer, sheet_name='Properties', index=False)
            
            # Summary sheet
            summary_df = pd.DataFrame([summary])
            summary_df.to_excel(writer, sheet_name='Portfolio_Summary', index=False)
            
            # Top performers sheet
            top_performers = df.head(50)
            top_performers.to_excel(writer, sheet_name='Top_Performers', index=False)
            
            # Cash flow analysis sheet
            cash_flow_analysis = df[['address', 'price', 'monthly_cash_flow', 'annual_cash_flow', 
                                   'cash_on_cash_return', 'total_return']].copy()
            cash_flow_analysis = cash_flow_analysis.sort_values('monthly_cash_flow', ascending=False)
            cash_flow_analysis.to_excel(writer, sheet_name='Cash_Flow_Analysis', index=False)
        
        logger.info(f"Exported {len(df)} properties to {filepath}")
        return filepath
    
    def generate_analysis_report(self, df: pd.DataFrame, summary: Dict) -> str:
        """Generate a comprehensive analysis report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"analysis_report_{timestamp}.txt"
        report_path = os.path.join(self.output_dir, report_filename)
        
        with open(report_path, 'w') as f:
            f.write("REAL ESTATE INVESTMENT ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Properties Analyzed: {summary.get('total_properties', 0):,}\n")
            f.write(f"Total Investment Required: ${summary.get('total_investment', 0):,.2f}\n")
            f.write(f"Total Annual Cash Flow: ${summary.get('total_annual_cash_flow', 0):,.2f}\n")
            f.write(f"Portfolio Cash-on-Cash Return: {summary.get('portfolio_cash_on_cash', 0):.2f}%\n\n")
            
            f.write("RETURN METRICS SUMMARY\n")
            f.write("-" * 30 + "\n")
            f.write(f"Average Total Return: {summary.get('avg_total_return', 0):.2f}%\n")
            f.write(f"Average Cash-on-Cash Return: {summary.get('avg_cash_on_cash', 0):.2f}%\n")
            f.write(f"Average Appreciation Return: {summary.get('avg_appreciation', 0):.2f}%\n")
            f.write(f"Average Tax Savings Return: {summary.get('avg_tax_savings', 0):.2f}%\n")
            f.write(f"Average Principal Paydown Return: {summary.get('avg_principal_paydown', 0):.2f}%\n\n")
            
            f.write("PROPERTY DISTRIBUTION\n")
            f.write("-" * 30 + "\n")
            f.write(f"Properties with Positive Cash Flow: {summary.get('properties_with_positive_cash_flow', 0)}\n")
            f.write(f"Properties with 10%+ Total Return: {summary.get('properties_with_10_plus_return', 0)}\n")
            f.write(f"Properties with 15%+ Total Return: {summary.get('properties_with_15_plus_return', 0)}\n")
            f.write(f"Properties with 20%+ Total Return: {summary.get('properties_with_20_plus_return', 0)}\n\n")
            
            f.write("TOP 10 PROPERTIES BY TOTAL RETURN\n")
            f.write("-" * 40 + "\n")
            top_10 = df.head(10)
            for idx, row in top_10.iterrows():
                f.write(f"{row['address']} - Total Return: {row['total_return']:.2f}% - Price: ${row['price']:,.0f}\n")
        
        logger.info(f"Generated analysis report: {report_path}")
        return report_path
    
    def process_and_export(self, properties: List[Dict], output_format: str = 'xlsx', 
                          min_total_return: float = 0) -> Dict:
        """Complete processing and export workflow"""
        # Process properties
        df = self.process_properties(properties)
        
        # Filter properties
        filtered_df = self.filter_properties(df, min_total_return)
        
        # Calculate summary
        summary = self.calculate_portfolio_summary(filtered_df)
        
        # Export based on format
        export_files = {}
        
        if output_format.lower() == 'csv':
            csv_file = self.export_to_csv(filtered_df)
            export_files['csv'] = csv_file
        
        if output_format.lower() == 'xlsx':
            excel_file = self.export_to_excel(filtered_df, summary)
            export_files['excel'] = excel_file
        
        # Generate report
        report_file = self.generate_analysis_report(filtered_df, summary)
        export_files['report'] = report_file
        
        return {
            'dataframe': filtered_df,
            'summary': summary,
            'export_files': export_files
        }
