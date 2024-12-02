from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models import Product, Category
from schemas import ProductUpdate, ProductCreate, CategoryCreate, CategoryUpdate


def get_product(db: Session, product_id: int) -> Product:
    return db.query(Product).filter(Product.id == product_id).first()


def get_product_by_name(db: Session, name: str) -> Product:
    return db.query(Product).filter(Product.name == name).first()


def get_all_products(db: Session) -> list[Product]:
    return db.query(Product).all()


def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: ProductUpdate) -> Product:
    db_product = get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for field in product.model_dump():
        setattr(db_product, field, getattr(product, field))
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> Product:
    db_product = get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return db_product


def get_category(db: Session, category_id: int) -> Category:
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_name(db: Session, name: str) -> Category:
    return db.query(Category).filter(Category.name == name).first()


def get_all_categories(db: Session) -> list[Category]:
    return db.query(Category).all()


def create_category(db: Session, category: CategoryCreate) -> Category:
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(
    db: Session, category_id: int, category: CategoryUpdate
) -> Category:
    db_category = get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    for field in category.model_dump(exclude_unset=True):
        setattr(db_category, field, getattr(category, field))
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int) -> Category:
    db_category = get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return db_category
