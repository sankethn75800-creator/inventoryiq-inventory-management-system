# InventoryIQ – Inventory Intelligence Platform

**A full-stack inventory management and demand intelligence platform built with Python, FastAPI, PostgreSQL, and Streamlit.**

InventoryIQ helps businesses manage products, track sales, monitor stock levels, analyze revenue, and make data-driven inventory decisions through demand forecasting and automated reorder recommendations.

## Key Features

- **Inventory Management:** Add, view, update, search, and delete products.
- **Sales Management:** Record sales transactions with automatic stock deduction.
- **Interactive Dashboard:** Monitor inventory value, available stock, sales revenue, and product performance.
- **Low-Stock Alerts:** Identify products approaching or reaching their stock thresholds.
- **Demand Forecasting:** Estimate future inventory requirements using historical sales averages.
- **Reorder Recommendations:** Calculate suggested replenishment quantities based on demand, stock levels, and supplier lead times.
- **REST API:** Access inventory and sales operations through documented FastAPI endpoints.

## Technology Stack

| Component | Technologies |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Database | PostgreSQL (Neon), SQLite |
| ORM | SQLAlchemy |
| Frontend | Streamlit |
| Data Analysis | Pandas |
| Data Visualization | Plotly |
| API Testing | Swagger UI, Pytest |
| Deployment | Render, Streamlit Community Cloud |

## System Architecture

```text
           Streamlit Dashboard
                   |
               REST API
                   |
             FastAPI Backend
                   |
               SQLAlchemy
                   |
           Neon PostgreSQL
                   |
        Inventory & Sales Data
                   |
        Demand Forecasting Logic
                   |
         Reorder Recommendations
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API status |
| POST | `/products` | Create a product |
| GET | `/products` | List and search products |
| GET | `/products/{product_id}` | Retrieve product details |
| PUT | `/products/{product_id}` | Update product |
| DELETE | `/products/{product_id}` | Delete product |
| GET | `/products/low-stock` | Retrieve low-stock products |
| POST | `/sales` | Record a sale |
| GET | `/sales` | Retrieve sales history |
| GET | `/dashboard` | Retrieve inventory and revenue metrics |
| GET | `/forecast/{product_id}` | Generate a demand forecast |
| GET | `/recommendations` | Retrieve reorder recommendations |

## Demand Forecasting

InventoryIQ uses historical sales data to estimate demand.

**Average Daily Demand**

```text
Average Daily Demand = Units Sold / Historical Days
```

**Predicted Demand**

```text
Predicted Demand = Average Daily Demand × Forecast Days
```

**Recommended Reorder Quantity**

```text
Reorder Quantity = max(
    0,
    Lead Time Demand + Safety Stock - Current Stock
)
```

The forecasting system uses a statistical historical