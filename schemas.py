
from typing import Optional

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(ge=0, allow_inf_nan=False)
    quantity: int = Field(ge=0)
    low_stock_threshold: int = Field(default=10, ge=0)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    price: Optional[float] = Field(
        default=None,
        ge=0,
        allow_inf_nan=False
    )
    quantity: Optional[int] = Field(default=None, ge=0)
    low_stock_threshold: Optional[int] = Field(default=None, ge=0)


class SaleCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
