# FastAPI E-commerce Application

## Description
This is a RESTful API for managing products and categories in an e-commerce system. It uses **FastAPI** for building the API, **SQLAlchemy** for database operations, and **SQLite** as the default database. Testing is implemented with **pytest**.

## Features
- **Products**:
  - Create a product.
  - Retrieve one or all products.
  - Update a product.
  - Delete a product.
- **Categories**:
  - Create a category.
  - Retrieve one or all categories.
  - Update a category.
  - Delete a category.

## Requirements
- Python 3.12
- FastAPI
- SQLAlchemy
- pytest
- Uvicorn (for running the server)

## Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:yashkunn/mentor_test.git
    ```
2. Create a virtual environment:
   ```bash
    python -m venv venv
    source venv/bin/activate    # For Linux/MacOS
    venv\Scripts\activate       # For Windows
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
1. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
2. The API will be available at:
    ```
    http://127.0.0.1:8000
    ```
3. Access API documentation:
    ```
   - Swagger UI: http://127.0.0.1:8000/docs
   - Redoc: http://127.0.0.1:8000/redoc
    ```
   
## Testing
1. Ensure the server is not running.
2. Run the tests:
   ```bash
   pytest
   ```