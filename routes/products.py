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
def create_product(request: schema.ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product in the database.

    Args:
        request (schema.ProductCreate): The request object containing the product details.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        models.Product: The newly created product.
    """
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


@router.patch("/{product_id}", response_model=schema.ProductBase)
def update_product(
    product_id: int, request: schema.ProductUpdate, db: Session = Depends(get_db)
):
    """
    Update a product in the database.

    Args:
        product_id (int): The ID of the product to update.
        request (schema.ProductBase): The updated product data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        models.Product: The updated product.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=404, detail=f"Product with id {product_id} not found"
        )
    request_payload = request.model_dump()
    for key, value in request_payload.items():
        if value:
            setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product
