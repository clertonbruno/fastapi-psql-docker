from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

import schema
from database import get_async_db
from routes.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


# Dependency to get product service
def get_product_service(db: AsyncSession = Depends(get_async_db)) -> ProductService:
    return ProductService(db)


@router.get("/", response_model=List[schema.ProductBase])
async def read_products(service: ProductService = Depends(get_product_service)):
    """
    Retrieve a list of products.

    Returns:
        List[schema.ProductBase]: A list of product objects.
    """
    return await service.list_products()


@router.get("/{id}", response_model=schema.ProductBase)
async def get_product(id: str, service: ProductService = Depends(get_product_service)):
    """
    Retrieve a product by its ID.

    Args:
        id (str): The ID of the product to retrieve.
        service (ProductService, optional): The product service dependency. Defaults to Depends(get_product_service).

    Returns:
        schema.ProductBase: The retrieved product.

    Raises:
        HTTPException: If the product with the specified ID is not found.
    """
    return await service.get_product(int(id))


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schema.ProductBase
)
async def create_product(
    request: schema.ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    """
    Create a new product.

    Args:
        request (schema.ProductCreate): The product data to be created.
        service (ProductService, optional): The product service dependency. Defaults to Depends(get_product_service).

    Returns:
        schema.ProductBase: The created product.
    """
    return await service.create_product(request)


@router.patch("/{id}", response_model=schema.ProductBase)
async def update_product(
    id: int,
    request: schema.ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    """
    Update a product by its ID.

    Args:
        id (int): The ID of the product to be updated.
        request (schema.ProductUpdate): The product data to be updated.
        service (ProductService, optional): The product service dependency. Defaults to Depends(get_product_service).

    Returns:
        schema.ProductBase: The updated product.

    Raises:
        HTTPException: If the product with the specified ID is not found.
    """
    return await service.update_product(id, request)


@router.delete("/{id}", response_model=schema.ProductBase)
async def delete_product(
    id: str, service: ProductService = Depends(get_product_service)
):
    """
    Delete a product by its ID.

    Args:
        id (str): The ID of the product to be deleted.
        service (ProductService, optional): The product service dependency. Defaults to Depends(get_product_service).

    Returns:
        schema.ProductBase: The deleted product.

    Raises:
        HTTPException: If the product with the specified ID is not found.
    """
    return await service.delete_product(int(id))
