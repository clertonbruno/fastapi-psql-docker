from datetime import datetime

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
        orm_mode = True


class CreateProduct(ProductBase):
    class Config:
        orm_mode = True