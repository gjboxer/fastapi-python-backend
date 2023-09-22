from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from pydantic import BaseModel, validator
from typing import List
from datetime import datetime
import uuid
from bson import ObjectId

app = FastAPI()

# Connect to MongoDB Atlas using the connection string
mongo_uri = "mongodb+srv://gj:5ryACheDhtHjHoVb@cluster0.jqfdzcu.mongodb.net/data?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)
db = client.get_database()
# MongoDB collections for products and orders
products_collection = db.get_collection("products")
# print(products_collection)
orders_collection = db.get_collection("orders")

# Pydantic model for product schema
class Product(BaseModel):
    _id: ObjectId
    product_name: str
    product_price: float
    product_quantity: int

# Pydantic model for order item schema
class OrderItem(BaseModel):
    productId: str
    boughtQuantity: int

# Pydantic model for user address schema
class UserAddress(BaseModel):
    city: str
    country: str
    zip_code: str

# Pydantic model for order schema
class Order(BaseModel):
    order_id: str =str(uuid.uuid4())
    timestamp: datetime = datetime.now()
    items: List[OrderItem]
    total_amount: float
    user_address: UserAddress

# Home Route
@app.get("/")
def Home():
    return "Hello World"

# API to list all available products
@app.get("/products/", response_model=List[Product])
def get_all_products():
     # Retrieve all products from the MongoDB collection
    products = list(products_collection.find({}))
    print(products)
    # Create a list of Product objects with product IDs
    products_with_id = [
        Product(
            product_name=product["product_name"],
            product_price=product["product_price"],
            product_quantity=product["product_quantity"],
             _id=product["_id"]
            
        )
        for product in products
        
    ]

    return products_with_id

# API to create a new order
@app.post("/orders/", response_model=Order)
def create_new_order(order: Order):
    # data=list(products_collection.find({}))
    # Check if the requested products are available in sufficient quantity
    for item in order.items:
        product = products_collection.find_one({"_id":ObjectId(item.productId)})
        if not product:
            raise HTTPException(status_code=400, detail=f"Product with ID {item.productId} not found.")
        if item.boughtQuantity > product["product_quantity"]:
            raise HTTPException(status_code=400, detail=f"Insufficient quantity for product with ID {item.productId}.")

    # Calculate the total amount for the order
    total_amount = sum(
        product["product_price"] * item.boughtQuantity
        for item in order.items
        for product in products_collection.find({"_id": ObjectId(item.productId)})
    )

    # Reduce the available quantity of the products after a successful purchase
    for item in order.items:
        product = products_collection.find_one({"_id":ObjectId(item.productId)})
        new_quantity = product["product_quantity"] - item.boughtQuantity
        products_collection.update_one({"_id":ObjectId(item.productId)}, {"$set": {"product_quantity": new_quantity}})

    # Add the order to the orders collection
    order.total_amount = total_amount
    orders_collection.insert_one(order.dict())
    # order_id =str(uuid.uuid4())
    # order.timestamp=datetime()
    # order.orderid = order_id
    return order

# API to fetch all orders with pagination
@app.get("/orders/", response_model=List[Order])
def get_all_orders(limit: int = Query(10, description="Number of orders to retrieve", ge=1), offset: int = Query(0, description="Offset for pagination", ge=0)):
    orders = list(orders_collection.find({}).skip(offset).limit(limit))
    return orders


# API to fetch order with order_id
@app.get("/orders/{order_id}", response_model=Order)
def get_order_by_id(order_id: str):
    order = orders_collection.find_one({"order_id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# API to update the available quantity for a product by ID
@app.put("/products/{product_id}/update_quantity/", response_model=Product)
def update_product_quantity(product_id: str, new_quantity: int):
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
    
    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity should be non-negative.")
    
    products_collection.update_one({"_id":  ObjectId(product_id)}, {"$set": {"product_quantity": new_quantity}})
    product = products_collection.find_one({"_id":  ObjectId(product_id)})
    
    return product

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
