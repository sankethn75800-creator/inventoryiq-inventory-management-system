
import os
import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from main import app, get_db


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    engine.dispose()


def sample_product():
    return {
        "name": "Dell Laptop",
        "price": 55000,
        "quantity": 15,
        "low_stock_threshold": 5
    }


def create_product(client):
    response = client.post(
        "/products",
        json=sample_product()
    )
    assert response.status_code == 201
    return response.json()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_create_product(client):
    product = create_product(client)
    assert product["name"] == "Dell Laptop"
    assert product["quantity"] == 15


def test_get_products(client):
    create_product(client)
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_product_by_id(client):
    product = create_product(client)

    response = client.get(
        f"/products/{product['id']}"
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Dell Laptop"


def test_update_product(client):
    product = create_product(client)

    response = client.put(
        f"/products/{product['id']}",
        json={"price": 50000}
    )

    assert response.status_code == 200
    assert response.json()["price"] == 50000


def test_delete_product(client):
    product = create_product(client)

    response = client.delete(
        f"/products/{product['id']}"
    )

    assert response.status_code == 200

    missing = client.get(
        f"/products/{product['id']}"
    )
    assert missing.status_code == 404


def test_low_stock(client):
    product = sample_product()
    product["quantity"] = 2

    client.post("/products", json=product)

    response = client.get("/products/low-stock")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_record_sale(client):
    product = create_product(client)

    response = client.post(
        "/sales",
        json={
            "product_id": product["id"],
            "quantity": 3
        }
    )

    assert response.status_code == 201
    assert response.json()["remaining_stock"] == 12
    assert response.json()["total_amount"] == 165000


def test_insufficient_stock(client):
    product = create_product(client)

    response = client.post(
        "/sales",
        json={
            "product_id": product["id"],
            "quantity": 100
        }
    )

    assert response.status_code == 400


def test_dashboard(client):
    create_product(client)

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert response.json()["total_products"] == 1
    assert response.json()["total_stock_units"] == 15


def test_forecast(client):
    product = create_product(client)

    response = client.get(
        f"/forecast/{product['id']}"
    )

    assert response.status_code == 200
    assert "predicted_units_needed" in response.json()
    assert "stockout_risk" in response.json()


def test_recommendations(client):
    create_product(client)

    response = client.get("/recommendations")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_invalid_product_price(client):
    product = sample_product()
    product["price"] = -100

    response = client.post("/products", json=product)

    assert response.status_code == 422


def test_delete_product_with_sales(client):
    product = create_product(client)

    client.post(
        "/sales",
        json={
            "product_id": product["id"],
            "quantity": 2
        }
    )

    response = client.delete(
        f"/products/{product['id']}"
    )

    assert response.status_code == 409
