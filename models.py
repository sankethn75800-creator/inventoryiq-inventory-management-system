
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=10)


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
        index=True
    )
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    sold_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
