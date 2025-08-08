import numpy as np
import pandas as pd
from typing import Dict, List
import src.config as config
import logging

logger = logging.getLogger(__name__)

class FinancialCalculator:
    def __init__(self):
        self.down_payment_pct = config.DEFAULT_DOWN_PAYMENT_PCT
        self.interest_rate = config.DEFAULT_INTEREST_RATE
        self.loan_term = config.DEFAULT_LOAN_TERM
        self.appreciation_rate = config.DEFAULT_APPRECIATION_RATE
        self.tax_rate = config.DEFAULT_TAX_RATE
        self.depreciation_rate = config.DEFAULT_DEPRECIATION_RATE
        self.property_management_fee = config.DEFAULT_PROPERTY_MANAGEMENT_FEE
        self.insurance_rate = config.DEFAULT_INSURANCE_RATE
        self.maintenance_rate = config.DEFAULT_MAINTENANCE_RATE
        self.vacancy_rate = config.DEFAULT_VACANCY_RATE
    
    def calculate_monthly_mortgage_payment(self, loan_amount: float) -> float:
        """Calculate monthly mortgage payment using the standard formula"""
        if loan_amount <= 0:
            return 0
        
        monthly_rate = self.interest_rate / 12
        num_payments = self.loan_term * 12
        
        if monthly_rate == 0:
            return loan_amount / num_payments
        
        # Standard mortgage payment formula
        payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
        return payment
    
    def calculate_loan_amortization(self, loan_amount: float, num_years: int = 1) -> Dict:
        """Calculate loan amortization for the first year"""
        monthly_payment = self.calculate_monthly_mortgage_payment(loan_amount)
        monthly_rate = self.interest_rate / 12
        remaining_balance = loan_amount
        
        total_interest = 0
        total_principal = 0
        
        for month in range(1, min(num_years * 12 + 1, 13)):  # First year only
            interest_payment = remaining_balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            
            total_interest += interest_payment
            total_principal += principal_payment
            remaining_balance -= principal_payment
        
        return {
            'monthly_payment': monthly_payment,
            'annual_interest': total_interest,
            'annual_principal': total_principal,
            'remaining_balance': remaining_balance
        }
    
    def calculate_cash_on_cash_return(self, property_data: Dict) -> float:
        """Calculate cash on cash return"""
        try:
            purchase_price = property_data.get('price', 0)
            down_payment = purchase_price * self.down_payment_pct
            loan_amount = purchase_price - down_payment
            
            # Calculate annual rental income
            monthly_rent = property_data.get('estimated_rental_income', 0)
            annual_rent = monthly_rent * 12
            
            # Calculate annual expenses
            annual_expenses = self._calculate_annual_expenses(property_data)
            
            # Calculate annual mortgage payments
            amortization = self.calculate_loan_amortization(loan_amount)
            annual_mortgage_payment = amortization['monthly_payment'] * 12
            
            # Calculate annual cash flow
            annual_cash_flow = annual_rent - annual_expenses - annual_mortgage_payment
            
            # Cash on cash return
            if down_payment > 0:
                cash_on_cash = annual_cash_flow / down_payment
                return round(cash_on_cash * 100, 2)  # Return as percentage
            else:
                return 0
                
        except Exception as e:
            logger.error(f"Error calculating cash on cash return: {e}")
            return 0
    
    def calculate_appreciation_return(self, property_data: Dict) -> float:
        """Calculate annual appreciation return"""
        try:
            purchase_price = property_data.get('price', 0)
            annual_appreciation = purchase_price * self.appreciation_rate
            down_payment = purchase_price * self.down_payment_pct
            
            if down_payment > 0:
                appreciation_return = annual_appreciation / down_payment
                return round(appreciation_return * 100, 2)  # Return as percentage
            else:
                return 0
                
        except Exception as e:
            logger.error(f"Error calculating appreciation return: {e}")
            return 0
    
    def calculate_tax_savings_return(self, property_data: Dict) -> float:
        """Calculate tax savings return from depreciation"""
        try:
            purchase_price = property_data.get('price', 0)
            down_payment = purchase_price * self.down_payment_pct
            
            # Calculate annual depreciation (excluding land value)
            # Assume 80% of property value is depreciable (building)
            depreciable_value = purchase_price * 0.8
            annual_depreciation = depreciable_value / 27.5  # 27.5 years straight-line
            
            # Calculate tax savings
            annual_tax_savings = annual_depreciation * self.tax_rate
            
            if down_payment > 0:
                tax_savings_return = annual_tax_savings / down_payment
                return round(tax_savings_return * 100, 2)  # Return as percentage
            else:
                return 0
                
        except Exception as e:
            logger.error(f"Error calculating tax savings return: {e}")
            return 0
    
    def calculate_principal_paydown_return(self, property_data: Dict) -> float:
        """Calculate principal paydown return"""
        try:
            purchase_price = property_data.get('price', 0)
            down_payment = purchase_price * self.down_payment_pct
            loan_amount = purchase_price - down_payment
            
            # Calculate annual principal paydown
            amortization = self.calculate_loan_amortization(loan_amount)
            annual_principal_paydown = amortization['annual_principal']
            
            if down_payment > 0:
                principal_paydown_return = annual_principal_paydown / down_payment
                return round(principal_paydown_return * 100, 2)  # Return as percentage
            else:
                return 0
                
        except Exception as e:
            logger.error(f"Error calculating principal paydown return: {e}")
            return 0
    
    def _calculate_annual_expenses(self, property_data: Dict) -> float:
        """Calculate annual operating expenses"""
        purchase_price = property_data.get('price', 0)
        monthly_rent = property_data.get('estimated_rental_income', 0)
        
        # Property management fees
        property_management = monthly_rent * 12 * self.property_management_fee
        
        # Insurance
        insurance = purchase_price * self.insurance_rate
        
        # Maintenance
        maintenance = purchase_price * self.maintenance_rate
        
        # Vacancy loss
        vacancy_loss = monthly_rent * 12 * self.vacancy_rate
        
        # Property taxes (estimate 1.2% of property value)
        property_taxes = purchase_price * 0.012
        
        # Utilities (estimate $200/month)
        utilities = 200 * 12
        
        # HOA fees (if applicable, estimate $300/month)
        hoa_fees = 300 * 12
        
        total_expenses = (
            property_management + 
            insurance + 
            maintenance + 
            vacancy_loss + 
            property_taxes + 
            utilities + 
            hoa_fees
        )
        
        return total_expenses
    
    def calculate_total_return(self, property_data: Dict) -> Dict:
        """Calculate all four return metrics for a property"""
        try:
            # Calculate individual returns
            cash_on_cash = self.calculate_cash_on_cash_return(property_data)
            appreciation = self.calculate_appreciation_return(property_data)
            tax_savings = self.calculate_tax_savings_return(property_data)
            principal_paydown = self.calculate_principal_paydown_return(property_data)
            
            # Calculate total return
            total_return = cash_on_cash + appreciation + tax_savings + principal_paydown
            
            # Calculate additional financial metrics
            purchase_price = property_data.get('price', 0)
            down_payment = purchase_price * self.down_payment_pct
            monthly_rent = property_data.get('estimated_rental_income', 0)
            annual_rent = monthly_rent * 12
            
            # Calculate monthly cash flow
            loan_amount = purchase_price - down_payment
            amortization = self.calculate_loan_amortization(loan_amount)
            monthly_mortgage = amortization['monthly_payment']
            annual_expenses = self._calculate_annual_expenses(property_data)
            monthly_expenses = annual_expenses / 12
            monthly_cash_flow = monthly_rent - monthly_expenses - monthly_mortgage
            
            return {
                'cash_on_cash_return': cash_on_cash,
                'appreciation_return': appreciation,
                'tax_savings_return': tax_savings,
                'principal_paydown_return': principal_paydown,
                'total_return': total_return,
                'monthly_cash_flow': monthly_cash_flow,
                'annual_cash_flow': monthly_cash_flow * 12,
                'down_payment': down_payment,
                'loan_amount': loan_amount,
                'monthly_mortgage': monthly_mortgage,
                'annual_expenses': annual_expenses,
                'annual_rent': annual_rent
            }
            
        except Exception as e:
            logger.error(f"Error calculating total return: {e}")
            return {
                'cash_on_cash_return': 0,
                'appreciation_return': 0,
                'tax_savings_return': 0,
                'principal_paydown_return': 0,
                'total_return': 0,
                'monthly_cash_flow': 0,
                'annual_cash_flow': 0,
                'down_payment': 0,
                'loan_amount': 0,
                'monthly_mortgage': 0,
                'annual_expenses': 0,
                'annual_rent': 0
            }
    
    def calculate_portfolio_metrics(self, properties: List[Dict]) -> Dict:
        """Calculate portfolio-level metrics"""
        if not properties:
            return {}
        
        total_properties = len(properties)
        total_investment = sum(prop.get('financial_metrics', {}).get('down_payment', 0) for prop in properties)
        total_annual_cash_flow = sum(prop.get('financial_metrics', {}).get('annual_cash_flow', 0) for prop in properties)
        total_annual_return = sum(prop.get('financial_metrics', {}).get('total_return', 0) for prop in properties)
        
        # Calculate average metrics
        avg_total_return = total_annual_return / total_properties if total_properties > 0 else 0
        avg_cash_on_cash = sum(prop.get('financial_metrics', {}).get('cash_on_cash_return', 0) for prop in properties) / total_properties if total_properties > 0 else 0
        avg_appreciation = sum(prop.get('financial_metrics', {}).get('appreciation_return', 0) for prop in properties) / total_properties if total_properties > 0 else 0
        avg_tax_savings = sum(prop.get('financial_metrics', {}).get('tax_savings_return', 0) for prop in properties) / total_properties if total_properties > 0 else 0
        avg_principal_paydown = sum(prop.get('financial_metrics', {}).get('principal_paydown_return', 0) for prop in properties) / total_properties if total_properties > 0 else 0
        
        return {
            'total_properties': total_properties,
            'total_investment': total_investment,
            'total_annual_cash_flow': total_annual_cash_flow,
            'total_annual_return': total_annual_return,
            'avg_total_return': avg_total_return,
            'avg_cash_on_cash': avg_cash_on_cash,
            'avg_appreciation': avg_appreciation,
            'avg_tax_savings': avg_tax_savings,
            'avg_principal_paydown': avg_principal_paydown,
            'portfolio_cash_on_cash': (total_annual_cash_flow / total_investment * 100) if total_investment > 0 else 0
        }
