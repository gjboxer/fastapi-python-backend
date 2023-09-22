# FastAPI E-commerce Backend

This is the backend API for an e-commerce website built using FastAPI and MongoDB. It provides endpoints for managing products and orders.

## Features

- List available products
- Create new orders
- Fetch orders with pagination
- Fetch a specific order by ID
- Update product quantities

## Getting Started

These instructions will help you set up and run the FastAPI backend on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- MongoDB (You can use MongoDB Atlas for cloud-hosted MongoDB)

### Installation

```bash
git clone https://github.com/gjboxer/fastapi-python-backend
pip install -r requirements.txt
py testmdb.py
```
-Backend will get started at http://127.0.0.1:8000

### API Endpoints
- GET /products/: List all available products.
- POST /orders/: Create a new order.
- GET /orders/: Fetch all orders with pagination.
- GET /orders/{order_id}: Fetch a specific order by ID.
- PUT /products/{product_id}/update_quantity/: Update the available quantity for a product by ID.


### Here's a usage guide for the API endpoints with examples:

### List All Available Products
- Endpoint: GET /products/
- Description: Retrieves a list of all available products.
  ![Screenshot 2023-09-23 025119](https://github.com/gjboxer/fastapi-python-backend/assets/64975110/3b41db9f-9aa5-4fbd-8249-dd657fd29e70)

### Create a New Order
- Endpoint: POST /orders/
- Description: Creates a new order with selected products and quantities.
- json body 
  ```json
  {
    "items": [
          {
      "productId": "650dd22da15d0fa4b37eec2c",
      "boughtQuantity": 1
    }
    ],
    "total_amount": 0.0,
    "user_address": {
        "city": "City",
        "country": "Country",
        "zip_code": "12243236"
    }
}

![Screenshot 2023-09-23 025825](https://github.com/gjboxer/fastapi-python-backend/assets/64975110/836fffab-40d3-416b-8829-a989616c7df8)

### Fetch All Orders with Pagination
- Endpoint: GET /orders/?limit=2&offset=2
- Description: Retrieves a list of all orders with optional pagination.

![image](https://github.com/gjboxer/fastapi-python-backend/assets/64975110/9ca97b90-c545-4371-823b-5c33eec4abfc)

### Fetch a Specific Order by ID
- Endpoint: GET /orders/{order_id}
- Description: Retrieves a specific order by its ID.

![image](https://github.com/gjboxer/fastapi-python-backend/assets/64975110/94df79fb-68b8-4c94-8aa2-87bdd00fa859)

### Update Product Quantity
- Endpoint: PUT /products/{product_id}/update_quantity/?new_quantity=100
- Description: Update the available quantity of a product by providing its unique product ID.
![image](https://github.com/gjboxer/fastapi-python-backend/assets/64975110/d5895632-0293-4201-9354-c57e2461d261)



