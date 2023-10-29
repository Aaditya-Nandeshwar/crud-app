from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Get DB environment variables
DB_NAME = os.getenv("DB_NAME")
DB_SERVER = os.getenv("DB_SERVER")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")


# Database connection
def db_conn():
    conn = psycopg2.connect(database=DB_NAME, host=DB_SERVER, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
    return conn


conn = db_conn()
cur = conn.cursor()
create_table_query = """
    CREATE TABLE IF NOT EXISTS courses (
        id serial PRIMARY KEY,
        name varchar(100),
        fees integer,
        duration integer
    )
"""
# Execute the SQL command to create the table
cur.execute(create_table_query)
conn.commit()


@app.route("/")
def index():
    return "<h1>Hello!</h1>"


# Retrieve records from the database
@app.route('/api/records', methods=['GET'])
def get_records():
    conn = db_conn()
    cur = conn.cursor()
    # Implement code to fetch records from the database
    # Use cur.execute() and cur.fetchall() to retrieve records
    select_query = """
         SELECT *
         FROM courses
     """
    try:
        cur.execute(select_query)
        records = cur.fetchall()
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)})


# Create a new record in the database
@app.route('/api/create', methods=['POST'])
def create_record():
    conn = db_conn()
    cur = conn.cursor()
    data = request.json
    # print(data)
    # Implement code to insert a new record into the database
    # Use cur.execute() to insert the data
    insert_query = """
        INSERT INTO courses (name, fees, duration)
        VALUES (%s, %s, %s)
    """
    try:
        cur.execute(insert_query, (data['name'], data['fees'], data['duration']))
        conn.commit()
        return jsonify({"message": "Record created successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)})


# Update a record in the database
@app.route('/api/update/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    conn = db_conn()
    cur = conn.cursor()
    data = request.json
    # Implement code to update the record in the database
    # Use cur.execute() to update the data
    update_query = """
        UPDATE courses
        SET name = %s, fees = %s, duration = %s
        WHERE id = %s
    """
    try:
        cur.execute(update_query, (data['name'], data['fees'], data['duration'], record_id))
        conn.commit()
        return jsonify({"message": "Record updated successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)})


@app.route('/api/delete/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    conn = db_conn()
    cur = conn.cursor()
    data = request.json

    delete_query = """
        DELETE FROM courses
        WHERE id = %s
    """
    try:
        cur.execute(delete_query, (record_id,))
        conn.commit()
        return jsonify({"message": "Record deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
