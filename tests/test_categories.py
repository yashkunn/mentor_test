import pytest
from fastapi.testclient import TestClient
from main import app
from db.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_category():
    category_data = {
        "name": "Test Category",
        "description": "A test category",
    }
    response = client.post("/categories/", json=category_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Category"


def test_read_all_categories():
    response = client.get("/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_category():
    category_data = {
        "name": "Read Test Category",
        "description": "Category for testing read",
    }
    create_response = client.post("/categories/", json=category_data)
    category_id = create_response.json()["id"]

    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Read Test Category"
