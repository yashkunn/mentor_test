import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from db.models import Base
from schemas import ProductCreate, CategoryCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_product():
    product_data = {
        "name": "Test Product",
        "description": "A test product",
        "price": 10.5,
        "quantity": 5,
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"


def test_read_all_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_product():
    product_data = {
        "name": "Read Test",
        "description": "Product for testing read",
        "price": 15.0,
        "quantity": 10,
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Read Test"


def test_update_product():
    product_data = {
        "name": "Update Test",
        "description": "Before update",
        "price": 20.0,
        "quantity": 15,
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    updated_data = {
        "name": "Updated Product",
        "description": "After update",
        "price": 25.0,
        "quantity": 20,
    }
    update_response = client.put(f"/products/{product_id}", json=updated_data)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Product"


def test_create_product_with_negative_quantity():
    product_data = {
        "name": "Invalid Quantity Product",
        "description": "Product with negative quantity",
        "price": 10.0,
        "quantity": -5,
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 422
    assert "Quantity must be greater than zero." in response.json()["detail"][0]["msg"]


def test_create_product_with_negative_price():
    product_data = {
        "name": "Invalid Price Product",
        "description": "Product with negative price",
        "price": -10.0,
        "quantity": 5,
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 422
    assert "Price must be greater than zero." in response.json()["detail"][0]["msg"]


def test_delete_product():
    product_data = {
        "name": "Delete Test",
        "description": "To be deleted",
        "price": 30.0,
        "quantity": 25,
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    delete_response = client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["name"] == "Delete Test"

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404
