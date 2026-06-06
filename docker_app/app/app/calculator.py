from typing import List, Dict, Any
from .models import ScheduleItem

def calculate_loan(loan_amount: float, annual_interest_rate: float, tenure_years: float) -> Dict[str, Any]:
    """
    Calculates the EMI, total interest, total amount, and generates an amortization schedule.
    
    Args:
        loan_amount (float): The principal loan amount.
        annual_interest_rate (float): The annual interest rate in percentage.
        tenure_years (float): The loan duration in years.
        
    Returns:
        Dict[str, Any]: A dictionary containing emi, total_interest, total_amount, and the schedule.
    """
    months = int(round(tenure_years * 12))
    
    # Handle the edge case of 0% interest loan
    if annual_interest_rate == 0:
        emi = loan_amount / months if months > 0 else 0
        total_amount = loan_amount
        total_interest = 0.0
    else:
        monthly_interest_rate = (annual_interest_rate / 12) / 100
        # Standard EMI Formula
        emi = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** months) / (((1 + monthly_interest_rate) ** months) - 1)
        total_amount = emi * months
        total_interest = total_amount - loan_amount

    schedule: List[ScheduleItem] = []
    balance = loan_amount
    
    for month in range(1, months + 1):
        if annual_interest_rate == 0:
            interest_payment = 0.0
            principal_payment = emi
        else:
            interest_payment = balance * monthly_interest_rate
            principal_payment = emi - interest_payment
            
        # Adjust for the final month to avoid floating point issues
        if month == months or balance - principal_payment < 0:
            principal_payment = balance
            actual_emi = principal_payment + interest_payment
            balance = 0.0
        else:
            actual_emi = emi
            balance -= principal_payment

        schedule.append(ScheduleItem(
            month=month,
            emi=round(actual_emi, 2),
            principal=round(principal_payment, 2),
            interest=round(interest_payment, 2),
            balance=round(balance, 2)
        ))

    return {
        "emi": round(emi, 2),
        "total_interest": round(total_interest, 2),
        "total_amount": round(total_amount, 2),
        "schedule": schedule
    }
