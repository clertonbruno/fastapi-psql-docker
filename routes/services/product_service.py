from typing import List

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import schema


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_if_exists_conflict(
        self, product_name: str, product_sku: str
    ) -> bool:
        """
        Checks if a product with the given name or SKU already exists.

        Args:
            product_name (str): The name of the product to check.
            product_sku (str): The SKU of the product to check.

        Returns:
            bool: True if a product with the same name or SKU exists, False otherwise.
        """
        statement = select(models.Product).where(
            or_(models.Product.name == product_name, models.Product.sku == product_sku)
        )
        result = await self.db.execute(statement)
        product = result.scalars().first()
        return bool(product)

    async def list_products(self) -> List[models.Product]:
        """
        Retrieve all products.

        Returns:
          List[models.Product]: A list of all products.
        """
        result = await self.db.execute(select(models.Product))
        return result.scalars().all()

    async def get_product(self, product_id: int) -> models.Product:
        """
        Retrieve a product by its ID.

        Args:
          product_id (int): The ID of the product to retrieve.

        Returns:
          models.Product: The retrieved product.

        Raises:
          HTTPException: If the product with the specified ID is not found.
        """
        product = await self.db.execute(
            select(models.Product).where(models.Product.id == product_id)
        )
        product = product.scalars().first()
        if not product:
            raise HTTPException(
                status_code=404, detail=f"Product with id {product_id} not found"
            )
        return product

    async def create_product(
        self, product_create: schema.ProductCreate
    ) -> models.Product:
        """
        Create a new product.

        Args:
          product_create (schema.ProductCreate): The data required to create a new product.

        Returns:
          models.Product: The newly created product.

        Raises:
          HTTPException: If a product with the same name or SKU already exists or if a database error occurs.
        """
        try:
            product_exists = await self.check_if_exists_conflict(
                product_create.name.strip(), product_create.sku.strip().lower()
            )
            if product_exists:
                raise HTTPException(
                    status_code=400,
                    detail="A product with the same name or SKU already exists",
                )

            new_product = models.Product(
                name=product_create.name.strip(),
                sku=product_create.sku.strip().lower(),
                quantity=product_create.quantity,
                price=product_create.price,
                is_active=True,
                category_id=product_create.category_id,
            )

            self.db.add(new_product)
            await self.db.commit()
            await self.db.refresh(new_product)
            return new_product
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="A database error occurred while adding the product.",
            ) from e

    async def update_product(
        self, product_id: int, product_update: schema.ProductUpdate
    ) -> models.Product:
        """
        Update a product by its ID.

        Args:
          product_id (int): The ID of the product to update.
          product_update (schema.ProductUpdate): The data required to update the product.

        Returns:
          models.Product: The updated product.

        Raises:
          HTTPException: If the product with the specified ID is not found or if a database error occurs.
        """
        try:
            product = await self.get_product(product_id)
            request_payload = product_update.model_dump()
            for key, value in request_payload.items():
                if value:
                    if key == "name":
                        setattr(product, key, value.strip())
                    elif key == "sku":
                        setattr(product, key, value.strip().lower())
                    setattr(product, key, value)
            await self.db.commit()
            await self.db.refresh(product)
            return product
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="A database error occurred while updating the product.",
            ) from e

    async def delete_product(self, product_id: int) -> models.Product:
        """
        Delete a product by its ID.

        Args:
          product_id (int): The ID of the product to delete.

        Returns:
          models.Product: The deleted product.

        Raises:
          HTTPException: If the product with the specified ID is not found or if a database error occurs.
        """
        try:
            product = await self.get_product(product_id)
            await self.db.delete(product)
            await self.db.commit()
            return product
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="A database error occurred while deleting the product.",
            ) from e
