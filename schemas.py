from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class ProductBase(BaseModel):
    name: str
    description: str
    quantity: int
    price: float
    category_id: Optional[int] = None

    @field_validator("price")
    def price_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Price must be greater than zero.")
        return value

    @field_validator("quantity")
    def quantity_must_be_positive(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Quantity must be greater than zero.")
        return value


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


class ProductInDB(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryInDB(CategoryBase):
    id: int

    class Config:
        from_attributes = True
