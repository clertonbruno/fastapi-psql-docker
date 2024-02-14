from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    sku: str
    quantity: int
    is_active: bool
    price: float
    category_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductCreate(ProductBase):
    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    quantity: Optional[str] = None
    is_active: Optional[bool] = None
    price: Optional[float] = None
    category_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
