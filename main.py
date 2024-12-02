from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db import models
from db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.get("/products/{product_id}", response_model=schemas.ProductInDB)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.get("/products/", response_model=list[schemas.ProductInDB])
def read_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@app.post("/products/", response_model=schemas.ProductInDB)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = (
        db.query(models.Product).filter(models.Product.name == product.name).first()
    )
    if db_product:
        raise HTTPException(status_code=400, detail="Product already registered")
    return crud.create_product(db=db, product=product)


@app.put("/products/{product_id}", response_model=schemas.ProductInDB)
def update_product(
    product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)
):
    return crud.update_product(db=db, product_id=product_id, product=product)


@app.delete("/products/{product_id}", response_model=schemas.ProductInDB)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return crud.delete_product(db=db, product_id=product_id)


@app.get("/categories/{category_id}", response_model=schemas.CategoryInDB)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = (
        db.query(models.Category).filter(models.Category.id == category_id).first()
    )
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@app.get("/categories/", response_model=list[schemas.CategoryInDB])
def read_all_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories


@app.post("/categories/", response_model=schemas.CategoryInDB)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = (
        db.query(models.Category).filter(models.Category.name == category.name).first()
    )
    if db_category:
        raise HTTPException(status_code=400, detail="Category already registered")
    return crud.create_category(db=db, category=category)


@app.put("/categories/{category_id}", response_model=schemas.CategoryInDB)
def update_category(
    category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db)
):
    return crud.update_category(db=db, category_id=category_id, category=category)


@app.delete("/categories/{category_id}", response_model=schemas.CategoryInDB)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return crud.delete_category(db=db, category_id=category_id)
