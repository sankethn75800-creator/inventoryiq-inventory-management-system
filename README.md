
# AI-Enhanced Inventory Management System

A Python-based inventory management REST API built using FastAPI, SQLAlchemy, and SQLite.

## Overview

This application helps businesses manage products, track sales, monitor stock levels, analyze inventory performance, and estimate future product demand.

## Features

- Product creation, viewing, updating, and deletion
- Product search
- Sales recording and stock deduction
- Low-stock alerts
- Inventory analytics dashboard API
- Historical sales-based demand forecasting
- Stockout risk assessment
- Intelligent reorder recommendations
- Interactive API documentation using Swagger UI

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

## Installation

Clone the repository and open its folder.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m uvicorn main:app --reload
```

## API Documentation

Open:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | API status |
| POST | /products | Create product |
| GET | /products | List/search products |
| GET | /products/{product_id} | View product |
| PUT | /products/{product_id} | Update product |
| DELETE | /products/{product_id} | Delete product |
| GET | /products/low-stock | Low-stock alerts |
| POST | /sales | Record sale |
| GET | /sales | Sales history |
| GET | /dashboard | Inventory analytics |
| GET | /forecast/{product_id} | Demand forecast |
| GET | /recommendations | Reorder recommendations |

## Demand Forecasting

The forecasting feature uses historical sales to estimate average daily demand.

Average Daily Demand = Units Sold / Historical Days

Forecast Demand = Average Daily Demand × Forecast Days

Reorder recommendations use estimated demand during supplier lead time and the configured low-stock threshold.

This is a statistical forecasting approach, not a trained machine-learning model.

## Database

The application uses SQLite. The database file is automatically created when the application starts.

## Future Improvements

- User authentication and role-based access
- Interactive frontend dashboard
- Advanced machine-learning forecasting
- CSV export and reporting
- Cloud deployment
