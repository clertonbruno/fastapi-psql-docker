from sqlalchemy import (
    DECIMAL,
    TEXT,
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    text,
)

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    quantity = Column(Integer, nullable=False, server_default=text("'0'"))
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    price = Column(DECIMAL(10, 2), nullable=False, server_default=text("'0.00'"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_onupdate=text("now()"),
    )


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    description = Column(TEXT, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
