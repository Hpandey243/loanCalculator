# Loan Interest Calculator

A complete, production-ready Loan Interest Calculator web application built with a Python FastAPI backend and a Vanilla HTML/CSS/JavaScript frontend. It calculates EMI, total interest, total amount, and generates a detailed amortization schedule.

## Features

- **Accurate Calculations**: Computes standard EMI and provides month-by-month principal and interest breakdown.
- **Edge Cases Handled**: Fully supports 0% interest loans and high monetary volumes without floating-point errors.
- **Modern UI**: Clean, responsive, and mobile-friendly user interface styled with custom CSS (no frameworks).
- **Indian Rupee Formatting**: Formats all financial numbers according to the standard Indian numeric system (`₹1,23,456.78`).
- **Asynchronous Execution**: Uses Vanilla JavaScript Fetch API to perform calculations without page reloads.
- **Dockerized**: Fully containerized for easy deployment and setup anywhere.

## Architecture

- **Backend**: FastAPI (Python 3.12). Uses Pydantic for robust request validation and error handling.
- **Frontend**: HTML5, Vanilla CSS3, Vanilla JavaScript. Served statically directly via FastAPI's `Jinja2Templates` and `StaticFiles`.
- **Containerization**: Docker configuration uses the `python:3.12-slim` image to maintain a tiny, secure footprint.

## Project Structure

```text
loan-calculator/
├── app/
│   ├── main.py              # FastAPI application initialization & routing
│   ├── calculator.py        # Core financial calculation logic
│   ├── models.py            # Pydantic validation models
│   ├── templates/
│   │   └── index.html       # Frontend HTML view
│   └── static/
│       ├── style.css        # Custom responsive styling
│       └── script.js        # Vanilla JS logic for fetching data and updating DOM
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container build instructions
├── .dockerignore            # Ignored files for Docker context
└── README.md                # Project documentation
```

## API Documentation

### `POST /api/calculate`

Calculates the loan breakdown and amortization schedule.

**Request Body:**
```json
{
  "loan_amount": 500000,
  "interest_rate": 8.5,
  "tenure_years": 5
}
```

**Response (200 OK):**
```json
{
  "emi": 10258.23,
  "total_interest": 115493.80,
  "total_amount": 615493.80,
  "schedule": [
    {
      "month": 1,
      "emi": 10258.23,
      "principal": 6716.56,
      "interest": 3541.67,
      "balance": 493283.44
    },
    ...
  ]
}
```

**Validation Error (422 Unprocessable Entity):**
```json
{
  "detail": "Validation Error",
  "messages": [
    "interest_rate: Interest rate cannot be negative"
  ]
}
```

## Local Run Instructions (Without Docker)

1. **Ensure Python 3.10+ is installed.**
2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Uvicorn server:**
   ```bash
   uvicorn app.main:app --host 127.0.0.0 --port 8000 --reload
   ```
5. **Access the application** by navigating to [http://localhost:8000](http://localhost:8000).

## Docker Build Instructions

Make sure you have Docker installed. Run the following command in the root folder of the project:

```bash
docker build -t loan-calculator .
```

## Docker Run Instructions

Once built, start the container using:

```bash
docker run -p 8000:8000 loan-calculator
```

Access the application in your browser at [http://localhost:8000](http://localhost:8000).
