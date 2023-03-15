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
pip3 install -r requirements.txt
```

Note : Set up your Oracle Database and Redis connections in the app.py Python file.

### Run the Flask app:
```
python3 app.py
```

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

## Test Case - Simulating cache expiration of Redis and performing reads from Oracle

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

Read the order (should be read from Redis):
```
curl -X GET http://localhost:5000/orders/1
```

Flush Redis data to simulate cache expiration:
```
redis-cli FLUSHALL
```

Read the order again (should be read from Oracle now):
```
curl -X GET http://localhost:5000/orders/1
```

## Practical Example of Using this Solution for a Shopping Cart Microservice

In an e-commerce website, the shopping cart microservice is responsible for managing customers' shopping carts, such as adding items to the cart, updating item quantities, and removing items. We can use this code to simulate an e-commerce website taking orders using this Flask app

The code consists of a Flask application that exposes a RESTful API for managing orders (or shopping carts). It uses Redis as a cache and Oracle Database as the primary, persistent data store.

 ### Writing orders (shopping carts): 
 The API allows you to create new orders (shopping carts) and save them to Redis, Oracle, or both. Saving the data to Redis provides faster access to frequently used data, while saving the data to Oracle ensures persistence and consistency.

### Reading orders (shopping carts): 
When reading an order (shopping cart), the application first tries to fetch the data from Redis. If the data is available in Redis, it returns the data immediately, providing a fast response. If the data is not available in Redis, it fetches the data from the Oracle Database and returns it. In the provided code, it also caches the fetched data in Redis for future requests if the order was initially written to both databases.

This code demonstrates a two-layer data storage approach for an e-commerce website's shopping cart microservice. It uses Redis as a fast cache for frequently accessed data and Oracle as the main, persistent data storage. This setup allows the application to achieve high performance and low latency for read operations while maintaining data persistence and consistency.

To adapt this code for a shopping cart microservice, you would need to modify the table schema, API endpoints, and data manipulation logic to handle shopping cart data instead of orders.
