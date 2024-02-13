from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schema
from database import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/", response_model=List[schema.ProductBase])
def read_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schema.ProductBase
)
def create_product(request: schema.ProductBase, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name,
        sku=request.sku,
        quantity=request.quantity,
        is_active=True,
        price=request.price,
        category_id=request.category_id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
