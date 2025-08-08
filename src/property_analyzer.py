#!/usr/bin/env python3
"""
Property Analyzer - Detailed P&L Analysis
=========================================

Comprehensive property analysis with full P&L statements, tax implications,
and worst-case scenario recommendations.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
import src.config as config

class PropertyAnalyzer:
    def __init__(self):
        self.tax_rates = {
            'federal': 0.25,  # 25% federal tax rate
            'state': 0.05,    # 5% state tax rate (varies by state)
            'local': 0.02     # 2% local tax rate
        }
        
        # Tax deduction rates for real estate
        self.deduction_rates = {
            'mortgage_interest': 1.0,  # 100% deductible
            'property_tax': 1.0,       # 100% deductible (up to $10K SALT cap)
            'insurance': 0.0,           # Not deductible for personal use
            'maintenance': 0.0,         # Not deductible for personal use
            'depreciation': 1.0,        # 100% deductible (27.5 year straight line)
            'property_management': 1.0,  # 100% deductible
            'utilities': 0.0,           # Not deductible
            'hoa_fees': 0.0,            # Not deductible
            'vacancy_loss': 0.0         # Not deductible
        }
    
    def calculate_detailed_pl(self, property_data: Dict) -> Dict:
        """Calculate detailed P&L statement for a property"""
        
        # Extract property data
        price = property_data.get('price', 0)
        estimated_rent = property_data.get('estimated_rental_income', 0)
        sqft = property_data.get('sqft', 1500)
        year_built = property_data.get('year_built', 2000)
        
        # Calculate loan details
        down_payment = price * config.DOWN_PAYMENT_RATE
        loan_amount = price - down_payment
        monthly_payment = self._calculate_monthly_payment(loan_amount)
        annual_payment = monthly_payment * 12
        
        # Calculate monthly P&L
        monthly_pl = self._calculate_monthly_pl(property_data, estimated_rent, monthly_payment)
        
        # Calculate annual P&L
        annual_pl = self._calculate_annual_pl(monthly_pl, property_data)
        
        # Calculate tax implications
        tax_analysis = self._calculate_tax_implications(annual_pl, property_data)
        
        # Calculate worst-case scenario
        worst_case = self._calculate_worst_case_scenario(property_data, annual_pl)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(annual_pl, worst_case, property_data)
        
        return {
            'property_data': property_data,
            'monthly_pl': monthly_pl,
            'annual_pl': annual_pl,
            'tax_analysis': tax_analysis,
            'worst_case': worst_case,
            'recommendation': recommendation,
            'summary': self._create_summary(annual_pl, worst_case, recommendation)
        }
    
    def _calculate_monthly_payment(self, loan_amount: float) -> float:
        """Calculate monthly mortgage payment"""
        monthly_rate = config.INTEREST_RATE / 12 / 100
        num_payments = config.LOAN_TERM * 12
        
        if monthly_rate == 0:
            return loan_amount / num_payments
        
        payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
        return payment
    
    def _calculate_monthly_pl(self, property_data: Dict, monthly_rent: float, monthly_payment: float) -> Dict:
        """Calculate monthly P&L statement"""
        
        # Revenue
        gross_rental_income = monthly_rent
        
        # Operating Expenses
        property_tax = property_data.get('price', 0) * config.PROPERTY_TAX_RATE / 12
        insurance = property_data.get('price', 0) * config.INSURANCE_RATE / 12
        maintenance = property_data.get('price', 0) * config.MAINTENANCE_RATE / 12
        property_management = gross_rental_income * config.PROPERTY_MANAGEMENT_RATE
        utilities = 0  # Typically paid by tenant
        hoa_fees = 0   # Varies by property
        vacancy_loss = gross_rental_income * config.VACANCY_RATE
        
        # Total Operating Expenses
        total_operating_expenses = (
            property_tax + insurance + maintenance + 
            property_management + utilities + hoa_fees + vacancy_loss
        )
        
        # Net Operating Income
        net_operating_income = gross_rental_income - total_operating_expenses
        
        # Debt Service
        principal_payment = monthly_payment * 0.3  # Approximate principal portion
        interest_payment = monthly_payment * 0.7   # Approximate interest portion
        
        # Net Income
        net_income = net_operating_income - monthly_payment
        
        return {
            'revenue': {
                'gross_rental_income': gross_rental_income
            },
            'operating_expenses': {
                'property_tax': property_tax,
                'insurance': insurance,
                'maintenance': maintenance,
                'property_management': property_management,
                'utilities': utilities,
                'hoa_fees': hoa_fees,
                'vacancy_loss': vacancy_loss,
                'total': total_operating_expenses
            },
            'debt_service': {
                'principal_payment': principal_payment,
                'interest_payment': interest_payment,
                'total_payment': monthly_payment
            },
            'net_operating_income': net_operating_income,
            'net_income': net_income
        }
    
    def _calculate_annual_pl(self, monthly_pl: Dict, property_data: Dict) -> Dict:
        """Calculate annual P&L statement"""
        
        # Annualize monthly figures
        annual_revenue = {k: v * 12 for k, v in monthly_pl['revenue'].items()}
        annual_operating_expenses = {k: v * 12 for k, v in monthly_pl['operating_expenses'].items()}
        annual_debt_service = {k: v * 12 for k, v in monthly_pl['debt_service'].items()}
        
        # Calculate depreciation
        property_value = property_data.get('price', 0)
        land_value = property_value * 0.2  # Assume 20% is land
        building_value = property_value - land_value
        annual_depreciation = building_value / 27.5  # 27.5 year straight line
        
        # Calculate cash flow metrics
        annual_net_operating_income = monthly_pl['net_operating_income'] * 12
        annual_net_income = monthly_pl['net_income'] * 12
        
        # Calculate returns
        down_payment = property_data.get('price', 0) * config.DOWN_PAYMENT_RATE
        cash_on_cash_return = (annual_net_income / down_payment * 100) if down_payment > 0 else 0
        
        return {
            'revenue': annual_revenue,
            'operating_expenses': annual_operating_expenses,
            'debt_service': annual_debt_service,
            'depreciation': annual_depreciation,
            'net_operating_income': annual_net_operating_income,
            'net_income': annual_net_income,
            'cash_on_cash_return': cash_on_cash_return,
            'down_payment': down_payment
        }
    
    def _calculate_tax_implications(self, annual_pl: Dict, property_data: Dict) -> Dict:
        """Calculate tax implications for W2 earners"""
        
        # Deductible expenses
        deductible_expenses = {
            'mortgage_interest': annual_pl['debt_service']['interest_payment'],
            'property_tax': annual_pl['operating_expenses']['property_tax'],
            'depreciation': annual_pl['depreciation'],
            'property_management': annual_pl['operating_expenses']['property_management'],
            'maintenance': annual_pl['operating_expenses']['maintenance'],
            'insurance': annual_pl['operating_expenses']['insurance']
        }
        
        # Apply deduction rates
        total_deductions = sum(
            deductible_expenses[expense] * self.deduction_rates[expense]
            for expense in deductible_expenses
        )
        
        # Calculate tax savings
        federal_tax_savings = total_deductions * self.tax_rates['federal']
        state_tax_savings = total_deductions * self.tax_rates['state']
        local_tax_savings = total_deductions * self.tax_rates['local']
        total_tax_savings = federal_tax_savings + state_tax_savings + local_tax_savings
        
        # Adjusted net income (including tax savings)
        adjusted_net_income = annual_pl['net_income'] + total_tax_savings
        adjusted_cash_on_cash = (adjusted_net_income / annual_pl['down_payment'] * 100) if annual_pl['down_payment'] > 0 else 0
        
        return {
            'deductible_expenses': deductible_expenses,
            'total_deductions': total_deductions,
            'tax_savings': {
                'federal': federal_tax_savings,
                'state': state_tax_savings,
                'local': local_tax_savings,
                'total': total_tax_savings
            },
            'adjusted_net_income': adjusted_net_income,
            'adjusted_cash_on_cash_return': adjusted_cash_on_cash
        }
    
    def _calculate_worst_case_scenario(self, property_data: Dict, annual_pl: Dict) -> Dict:
        """Calculate worst-case scenario analysis"""
        
        # Worst-case assumptions
        vacancy_rate_worst = 0.15  # 15% vacancy
        rent_decrease = 0.10       # 10% rent decrease
        expense_increase = 0.20    # 20% expense increase
        interest_rate_increase = 0.02  # 2% interest rate increase
        
        # Calculate worst-case revenue
        worst_case_rent = property_data.get('estimated_rental_income', 0) * (1 - rent_decrease)
        worst_case_vacancy = worst_case_rent * vacancy_rate_worst
        worst_case_gross_income = worst_case_rent - worst_case_vacancy
        
        # Calculate worst-case expenses
        worst_case_expenses = annual_pl['operating_expenses']['total'] * (1 + expense_increase)
        
        # Calculate worst-case debt service
        loan_amount = property_data.get('price', 0) * (1 - config.DOWN_PAYMENT_RATE)
        worst_case_rate = config.INTEREST_RATE + (interest_rate_increase * 100)
        worst_case_payment = self._calculate_monthly_payment_with_rate(loan_amount, worst_case_rate) * 12
        
        # Worst-case net income
        worst_case_net_income = worst_case_gross_income - worst_case_expenses - worst_case_payment
        
        # Worst-case returns
        down_payment = annual_pl['down_payment']
        worst_case_cash_on_cash = (worst_case_net_income / down_payment * 100) if down_payment > 0 else 0
        
        return {
            'assumptions': {
                'vacancy_rate': vacancy_rate_worst,
                'rent_decrease': rent_decrease,
                'expense_increase': expense_increase,
                'interest_rate_increase': interest_rate_increase
            },
            'revenue': {
                'original_rent': property_data.get('estimated_rental_income', 0),
                'worst_case_rent': worst_case_rent,
                'vacancy_loss': worst_case_vacancy,
                'gross_income': worst_case_gross_income
            },
            'expenses': {
                'original_expenses': annual_pl['operating_expenses']['total'],
                'worst_case_expenses': worst_case_expenses
            },
            'debt_service': {
                'original_payment': annual_pl['debt_service']['total_payment'],
                'worst_case_payment': worst_case_payment
            },
            'net_income': {
                'original': annual_pl['net_income'],
                'worst_case': worst_case_net_income
            },
            'returns': {
                'original_cash_on_cash': annual_pl['cash_on_cash_return'],
                'worst_case_cash_on_cash': worst_case_cash_on_cash
            }
        }
    
    def _calculate_monthly_payment_with_rate(self, loan_amount: float, annual_rate: float) -> float:
        """Calculate monthly payment with specific interest rate"""
        monthly_rate = annual_rate / 12 / 100
        num_payments = config.LOAN_TERM * 12
        
        if monthly_rate == 0:
            return loan_amount / num_payments
        
        payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
        return payment
    
    def _generate_recommendation(self, annual_pl: Dict, worst_case: Dict, property_data: Dict) -> Dict:
        """Generate investment recommendation"""
        
        # Define criteria
        min_cash_on_cash = 6.0  # Minimum 6% cash-on-cash return
        min_worst_case_cash_on_cash = 2.0  # Minimum 2% in worst case
        max_price = 300000  # Maximum property price
        min_sqft = 1000     # Minimum square footage
        
        # Evaluate property
        price = property_data.get('price', 0)
        sqft = property_data.get('sqft', 0)
        cash_on_cash = annual_pl['cash_on_cash_return']
        worst_case_cash_on_cash = worst_case['returns']['worst_case_cash_on_cash']
        
        # Scoring system
        score = 0
        reasons = []
        
        # Price evaluation
        if price <= max_price:
            score += 25
            reasons.append("✅ Price within target range")
        else:
            reasons.append("❌ Price exceeds target range")
        
        # Size evaluation
        if sqft >= min_sqft:
            score += 15
            reasons.append("✅ Adequate square footage")
        else:
            reasons.append("❌ Below minimum square footage")
        
        # Cash-on-cash return evaluation
        if cash_on_cash >= min_cash_on_cash:
            score += 30
            reasons.append("✅ Strong cash-on-cash return")
        elif cash_on_cash >= min_cash_on_cash * 0.8:
            score += 20
            reasons.append("⚠️ Acceptable cash-on-cash return")
        else:
            reasons.append("❌ Below minimum cash-on-cash return")
        
        # Worst-case evaluation
        if worst_case_cash_on_cash >= min_worst_case_cash_on_cash:
            score += 30
            reasons.append("✅ Resilient in worst-case scenario")
        elif worst_case_cash_on_cash >= 0:
            score += 15
            reasons.append("⚠️ Breaks even in worst-case scenario")
        else:
            reasons.append("❌ Negative cash flow in worst-case scenario")
        
        # Generate recommendation
        if score >= 80:
            recommendation = "STRONG BUY"
            confidence = "High"
        elif score >= 60:
            recommendation = "BUY"
            confidence = "Medium"
        elif score >= 40:
            recommendation = "HOLD"
            confidence = "Low"
        else:
            recommendation = "PASS"
            confidence = "None"
        
        return {
            'score': score,
            'recommendation': recommendation,
            'confidence': confidence,
            'reasons': reasons,
            'criteria': {
                'min_cash_on_cash': min_cash_on_cash,
                'min_worst_case_cash_on_cash': min_worst_case_cash_on_cash,
                'max_price': max_price,
                'min_sqft': min_sqft
            }
        }
    
    def _create_summary(self, annual_pl: Dict, worst_case: Dict, recommendation: Dict) -> Dict:
        """Create executive summary"""
        
        return {
            'key_metrics': {
                'cash_on_cash_return': f"{annual_pl['cash_on_cash_return']:.2f}%",
                'worst_case_cash_on_cash': f"{worst_case['returns']['worst_case_cash_on_cash']:.2f}%",
                'annual_cash_flow': f"${annual_pl['net_income']:,.0f}",
                'worst_case_cash_flow': f"${worst_case['net_income']['worst_case']:,.0f}",
                'down_payment': f"${annual_pl['down_payment']:,.0f}"
            },
            'recommendation': {
                'action': recommendation['recommendation'],
                'confidence': recommendation['confidence'],
                'score': f"{recommendation['score']}/100"
            },
            'risk_assessment': {
                'rent_decrease_impact': f"${worst_case['revenue']['original_rent'] - worst_case['revenue']['worst_case_rent']:,.0f}",
                'expense_increase_impact': f"${worst_case['expenses']['worst_case_expenses'] - worst_case['expenses']['original_expenses']:,.0f}",
                'interest_rate_impact': f"${worst_case['debt_service']['worst_case_payment'] - worst_case['debt_service']['original_payment']:,.0f}"
            }
        }
    
    def analyze_properties(self, properties: List[Dict]) -> List[Dict]:
        """Analyze multiple properties and rank them"""
        
        analyses = []
        for prop in properties:
            analysis = self.calculate_detailed_pl(prop)
            analyses.append(analysis)
        
        # Sort by recommendation score (highest first)
        analyses.sort(key=lambda x: x['recommendation']['score'], reverse=True)
        
        return analyses
