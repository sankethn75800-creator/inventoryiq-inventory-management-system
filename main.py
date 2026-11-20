
from datetime import datetime, timedelta, timezone
from math import ceil

from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

import models
import schemas

from database import engine, Base, SessionLocal


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Enhanced Inventory Management System",
    description=(
        "Inventory REST API with sales analytics, "
        "stock alerts, demand forecasting and reorder recommendations."
    ),
    version="2.0.1"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def find_product(product_id: int, db: Session):
    product = (
        db.query(models.Product)
        .filter(models.Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@app.get("/")
def home():
    return {
        "message": "AI-Enhanced Inventory Management System",
        "status": "running",
        "documentation": "/docs"
    }


# -------------------------------
# PRODUCT MANAGEMENT
# -------------------------------

@app.post(
    "/products",
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = models.Product(**product.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get("/products")
def get_products(
    search: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)

    if search:
        query = query.filter(
            models.Product.name.ilike(f"%{search}%")
        )

    return query.order_by(models.Product.id).all()


@app.get("/products/low-stock")
def get_low_stock(db: Session = Depends(get_db)):
    return (
        db.query(models.Product)
        .filter(
            models.Product.quantity <=
            models.Product.low_stock_threshold
        )
        .order_by(models.Product.quantity)
        .all()
    )


@app.get("/products/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return find_product(product_id, db)


@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    updates: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    try:
        product = find_product(product_id, db)

        changes = updates.model_dump(exclude_unset=True)

        for field, value in changes.items():
            if value is None:
                raise HTTPException(
                    status_code=422,
                    detail=f"{field} cannot be null"
                )

            setattr(product, field, value)

        db.commit()
        db.refresh(product)

        return product

    except Exception:
        db.rollback()
        raise


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    try:
        product = find_product(product_id, db)

        existing_sales = (
            db.query(models.Sale)
            .filter(models.Sale.product_id == product_id)
            .first()
        )

        if existing_sales:
            raise HTTPException(
                status_code=409,
                detail=(
                    "Product has sales history and cannot "
                    "be deleted."
                )
            )

        db.delete(product)
        db.commit()

        return {
            "message": "Product deleted successfully"
        }

    except Exception:
        db.rollback()
        raise


# -------------------------------
# SALES MANAGEMENT
# -------------------------------

@app.post(
    "/sales",
    status_code=status.HTTP_201_CREATED
)
def record_sale(
    sale: schemas.SaleCreate,
    db: Session = Depends(get_db)
):
    try:
        dialect = db.get_bind().dialect.name

        if dialect == "sqlite":
            # SQLite requires a write transaction to
            # serialize stock changes.
            db.connection().exec_driver_sql(
                "BEGIN IMMEDIATE"
            )

            product = find_product(
                sale.product_id,
                db
            )

        else:
            # PostgreSQL row-level lock prevents
            # concurrent sales from overselling stock.
            product = (
                db.query(models.Product)
                .filter(
                    models.Product.id == sale.product_id
                )
                .with_for_update()
                .first()
            )

            if product is None:
                raise HTTPException(
                    status_code=404,
                    detail="Product not found"
                )

        if sale.quantity <= 0:
            raise HTTPException(
                status_code=422,
                detail="Sale quantity must be greater than zero"
            )

        if product.quantity < sale.quantity:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock"
            )

        product.quantity -= sale.quantity

        new_sale = models.Sale(
            product_id=product.id,
            quantity=sale.quantity,
            total_amount=round(
                product.price * sale.quantity,
                2
            )
        )

        db.add(new_sale)
        db.commit()

        db.refresh(new_sale)
        db.refresh(product)

        return {
            "message": "Sale recorded successfully",
            "sale_id": new_sale.id,
            "product_id": product.id,
            "quantity_sold": new_sale.quantity,
            "total_amount": new_sale.total_amount,
            "remaining_stock": product.quantity
        }

    except Exception:
        db.rollback()
        raise


@app.get("/sales")
def get_sales(db: Session = Depends(get_db)):
    return (
        db.query(models.Sale)
        .order_by(models.Sale.sold_at.desc())
        .all()
    )


# -------------------------------
# INVENTORY DASHBOARD
# -------------------------------

@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()

    total_sales = db.query(
        func.coalesce(
            func.sum(models.Sale.total_amount),
            0
        )
    ).scalar()

    total_units_sold = db.query(
        func.coalesce(
            func.sum(models.Sale.quantity),
            0
        )
    ).scalar()

    low_stock_products = [
        product
        for product in products
        if product.quantity <= product.low_stock_threshold
    ]

    return {
        "total_products": len(products),

        "total_stock_units": sum(
            product.quantity
            for product in products
        ),

        "inventory_value": round(
            sum(
                product.price * product.quantity
                for product in products
            ),
            2
        ),

        "total_sales_revenue": round(
            float(total_sales),
            2
        ),

        "total_units_sold": int(total_units_sold),

        "low_stock_count": len(low_stock_products),

        "low_stock_products": [
            {
                "id": product.id,
                "name": product.name,
                "quantity": product.quantity,
                "threshold": product.low_stock_threshold
            }
            for product in low_stock_products
        ]
    }


# -------------------------------
# DEMAND FORECASTING
# -------------------------------

def calculate_forecast(
    product: models.Product,
    db: Session,
    history_days: int = 30,
    forecast_days: int = 7,
    lead_time_days: int = 3
):
    now = datetime.now(timezone.utc).replace(
        tzinfo=None
    )

    cutoff = now - timedelta(days=history_days)

    sales = (
        db.query(models.Sale)
        .filter(
            models.Sale.product_id == product.id,
            models.Sale.sold_at >= cutoff,
            models.Sale.sold_at <= now
        )
        .all()
    )

    total_sold = sum(
        sale.quantity
        for sale in sales
    )

    average_daily_demand = (
        total_sold / history_days
    )

    predicted_demand = ceil(
        average_daily_demand * forecast_days
    )

    lead_time_demand = ceil(
        average_daily_demand * lead_time_days
    )

    target_stock = (
        lead_time_demand +
        product.low_stock_threshold
    )

    reorder_quantity = max(
        0,
        target_stock - product.quantity
    )

    if average_daily_demand > 0:
        days_until_stockout = round(
            product.quantity / average_daily_demand,
            1
        )
    else:
        days_until_stockout = None

    if product.quantity == 0:
        risk = "OUT_OF_STOCK"

    elif product.quantity <= product.low_stock_threshold:
        risk = "HIGH"

    elif (
        average_daily_demand > 0
        and product.quantity <= lead_time_demand
    ):
        risk = "HIGH"

    elif predicted_demand >= product.quantity:
        risk = "MEDIUM"

    else:
        risk = "LOW"

    return {
        "product_id": product.id,
        "product_name": product.name,
        "current_stock": product.quantity,
        "history_days": history_days,
        "historical_units_sold": total_sold,
        "average_daily_demand": round(
            average_daily_demand,
            2
        ),
        "forecast_days": forecast_days,
        "predicted_units_needed": predicted_demand,
        "estimated_days_until_stockout": days_until_stockout,
        "stockout_risk": risk,
        "recommended_reorder_quantity": reorder_quantity,
        "forecast_method": "Historical daily average",
        "note": (
            "Forecast based on historical sales. "
            "This is a statistical estimate, not "
            "a trained machine-learning model."
        )
    }


@app.get("/forecast/{product_id}")
def forecast_product(
    product_id: int,
    history_days: int = Query(
        default=30,
        ge=1,
        le=365
    ),
    forecast_days: int = Query(
        default=7,
        ge=1,
        le=365
    ),
    lead_time_days: int = Query(
        default=3,
        ge=1,
        le=365
    ),
    db: Session = Depends(get_db)
):
    product = find_product(product_id, db)

    return calculate_forecast(
        product,
        db,
        history_days,
        forecast_days,
        lead_time_days
    )


@app.get("/recommendations")
def recommendations(
    db: Session = Depends(get_db)
):
    products = db.query(models.Product).all()

    results = [
        calculate_forecast(product, db)
        for product in products
    ]

    risk_order = {
        "OUT_OF_STOCK": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3
    }

    return sorted(
        results,
        key=lambda item: risk_order[
            item["stockout_risk"]
        ]
    )
