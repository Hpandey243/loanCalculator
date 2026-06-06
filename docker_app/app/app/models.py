from pydantic import BaseModel, Field
from typing import List

class CalculateRequest(BaseModel):
    """
    Request model for the loan calculation API.
    Validates that inputs are positive and properly typed.
    """
    loan_amount: float = Field(..., gt=0, description="Loan amount must be strictly greater than 0")
    interest_rate: float = Field(..., ge=0, description="Annual interest rate cannot be negative")
    tenure_years: float = Field(..., gt=0, description="Tenure in years must be strictly greater than 0")


class ScheduleItem(BaseModel):
    """
    Model representing a single month's data in the amortization schedule.
    """
    month: int
    emi: float
    principal: float
    interest: float
    balance: float


class CalculateResponse(BaseModel):
    """
    Response model containing overall summary and detailed amortization schedule.
    """
    emi: float
    total_interest: float
    total_amount: float
    schedule: List[ScheduleItem]
