from datetime import datetime

from sqlalchemy import (
    DECIMAL,
    TEXT,
    Boolean,
    Column,
    DateTime,
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
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, server_onupdate=text("CURRENT_TIMESTAMP")
    )


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    description = Column(TEXT, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, server_onupdate=text("CURRENT_TIMESTAMP")
    )
