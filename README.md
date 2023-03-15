# Python Oracle DB with Redis
## Order Management with Redis and Oracle

This repository contains an example project that demonstrates how to use Redis as a cache for an Oracle database. The project is a simple RESTful API for managing orders. The API allows you to write orders to Redis, Oracle, or both, and read orders from either Redis or Oracle, depending on whether the data is available in Redis.

## Architecture
```
Client (Curl)  --->  Flask API  --->  Redis (Cache)
                            |
                            +--->  Oracle Database (Persistent storage)
```

## Setup

Install dependencies:

```
pip install -r requirements.txt
```

Set up your Oracle Database and Redis connections in the app.py Python file.

Run the Flask app:

python3 app.py

## API Usage
### Write an order

#### Write an order to both Redis and Oracle (default behavior):

```
curl -X POST -H "Content-Type: application/json" -d '{
  "order_id": 1,
  "customer_id": 123,
  "product_id": 456,
  "product_description": "Sample product",
  "order_delivery_address": "123 Example St.",
  "order_date_taken": "2023-03-15 15:00:00",
  "order_misc_notes": "Notes about the order"
}' http://localhost:5000/orders
```

#### Write an order to Redis only:

```
curl -X POST -H "Content-Type: application/json" -d '{
  "order_id": 2,
  "customer_id": 123,
  "product_id": 456,
  "product_description": "Sample product",
  "order_delivery_address": "123 Example St.",
  "order_date_taken": "2023-03-15 15:00:00",
  "order_misc_notes": "Notes about the order"
}' "http://localhost:5000/orders?target=redis"
```
    
#### Write an order to Oracle only:

```
curl -X POST -H "Content-Type: application/json" -d '{
  "order_id": 3,
  "customer_id": 123,
  "product_id": 456,
  "product_description": "Sample product",
  "order_delivery_address": "123 Example St.",
  "order_date_taken": "2023-03-15 15:00:00",
  "order_misc_notes": "Notes about the order"
}' "http://localhost:5000/orders?target=oracle"
```

### Read an order

#### Read an order by ID:

```
curl -X GET http://localhost:5000/orders/1

curl -X GET http://localhost:5000/orders/2

curl -X GET http://localhost:5000/orders/3
```
