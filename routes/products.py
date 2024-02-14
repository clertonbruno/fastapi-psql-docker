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
    stripped_name = request.name.strip()
    parsed_sku = request.sku.strip().lower()
    existing_product = (
        db.query(models.Product)
        .filter(
            models.Product.name == stripped_name or models.Product.sku == parsed_sku
        )
        .first()
    )
    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="A product with the same name or SKU already exists",
        )
    new_product = models.Product(
        name=stripped_name,
        sku=parsed_sku,
        quantity=request.quantity,
        is_active=True,
        price=request.price,
        category_id=request.category_id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.patch("/{id}", response_model=schema.ProductBase)
def update_product(
    id: int, request: schema.ProductUpdate, db: Session = Depends(get_db)
):
    """
    Update a product in the database.

    Args:
        id (int): The ID of the product to update.
        request (schema.ProductBase): The updated product data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        models.Product: The updated product.
    """
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {id} not found")
    request_payload = request.model_dump()
    for key, value in request_payload.items():
        if value:
            if key == "name":
                setattr(product, key, value.strip())
            elif key == "sku":
                setattr(product, key, value.strip().lower())
            setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{id}", response_model=schema.ProductBase)
def get_product(id: str, db: Session = Depends(get_db)):
    """
    Get a product from the database.

    Args:
        id (str): The ID of the product to retrieve. Because Pydantic automatically
        treats path parameter as a string, we use str instead of int.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        models.Product: The product.
    """
    product = db.query(models.Product).filter(models.Product.id == int(id)).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {id} not found")
    return product


@router.delete("/{id}", response_model=schema.ProductBase)
def delete_product(id: str, db: Session = Depends(get_db)):
    """
    Delete a product from the database.

    Args:
        id (str): The ID of the product to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        models.Product: The deleted product.
    """
    product = db.query(models.Product).filter(models.Product.id == int(id)).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {id} not found")
    db.delete(product)
    db.commit()
    return product
