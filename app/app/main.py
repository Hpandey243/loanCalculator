import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError

from .models import CalculateRequest, CalculateResponse
from .calculator import calculate_loan

app = FastAPI(
    title="Loan Interest Calculator",
    description="An API and Web UI to calculate EMI and amortization schedules.",
    version="1.0.0"
)

# Setup directories for static files and templates
base_dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors from Pydantic and return a clean JSON response 
    for the frontend to display.
    """
    errors = []
    for error in exc.errors():
        field_name = error['loc'][-1] if error['loc'] else "Field"
        errors.append(f"{field_name}: {error['msg']}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation Error", "messages": errors},
    )

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    """
    Serve the main HTML frontend.
    """
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/calculate", response_model=CalculateResponse)
async def api_calculate_loan(request: CalculateRequest):
    """
    Calculate the loan EMI, total interest, and amortization schedule.
    """
    try:
        result = calculate_loan(
            loan_amount=request.loan_amount,
            annual_interest_rate=request.interest_rate,
            tenure_years=request.tenure_years
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
