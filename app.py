from flask import Flask, request, jsonify
import os
import oracledb 
import redis
import json
from datetime import datetime

# Environment Variables for Oracle Database Connectivity
user = os.environ['ORACLE_USER']
password = os.environ['ORACLE_PASSWORD']
dsn = os.environ['ORACLE_DSN']

# Environment Variables for Redis Connectivity
redishost = os.environ['REDIS_HOST']
redispwd  = os.environ['REDIS_PASSWORD']
redisport = os.environ['REDIS_PORT']

# Connect to Oracle database
oracle_connection = oracledb.connect(user=user, password=password, dsn=dsn)
oracle_cursor = oracle_connection.cursor()

# Connect to Redis server
redis_client = redis.Redis(host=redishost,password=redispwd,port=redisport)

# Flask App
app = Flask(__name__)

@app.route('/orders', methods=['POST'])
def write_order():
    order = request.json
    target_db = request.args.get('target', 'both')  # Get the target database from query parameter (default: both)

    if target_db in ['redis', 'both']:
        # Serialize the order to JSON
        order_json = json.dumps(order)

        # Write to Redis
        redis_client.set(order['order_id'], order_json)

    if target_db in ['oracle', 'both']:
        # Convert the order_date_taken string to a datetime object
        order_date_taken = datetime.strptime(order['order_date_taken'], '%Y-%m-%d %H:%M:%S')

        # Write to Oracle
        insert_query = """
        INSERT INTO orders (
            order_id,
            customer_id,
            product_id,
            product_description,
            order_delivery_address,
            order_date_taken,
            order_misc_notes
        ) VALUES (
            :1, :2, :3, :4, :5, :6, :7
        )"""

        # Replace the original order_date_taken string with the datetime object
        order_values = list(order.values())
        order_values[5] = order_date_taken

        oracle_cursor.execute(insert_query, tuple(order_values))
        oracle_connection.commit()

    return jsonify({"status": "success", "message": f"Order written to {target_db}"}), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def read_order(order_id):
    # Try to read from Redis
    order_json = redis_client.get(order_id)

    if order_json:
        print("Read from Redis")
        return jsonify({"order": json.loads(order_json), "source": "Redis"})
    else:
        # Read from Oracle if not found in Redis
        select_query = "SELECT * FROM orders WHERE order_id = :1"
        oracle_cursor.execute(select_query, (order_id,))
        result = oracle_cursor.fetchone()

        if result:
            print("Read from Oracle")
            columns = [column[0] for column in oracle_cursor.description]
            order = dict(zip(columns, result))

            # Save the read order to Redis for future requests ONLY if it was written to Redis initially
            if 'both' in request.args.getlist('target'):
                redis_client.set(order_id, json.dumps(order))

            return jsonify({"order": order, "source": "Oracle"})
        else:
            return jsonify({"status": "error", "message": "Order not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)

