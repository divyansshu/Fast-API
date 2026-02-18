from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json
import hashlib
import sqlite3

app = FastAPI()

# Initialize Redis client connection
redis_client = redis.Redis(host = "localhost", port=6379, db = 0)

# Establish database connection
def get_db_connection():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database with sample data
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create users table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL,
                   age INTEGER
                   )
    """)
    # check if users table is empty before inserting
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Insert sample user records
        cursor.execute("INSERT INTO users (id, name, age) VALUES (1, 'Michael', 45)")
        cursor.execute("INSERT INTO users (id, name, age) VALUES (2, 'Jordan', 52)")
        cursor.execute("INSERT INTO users (id, name, age) VALUES (3, 'Phillips', 29)")
    print('Database initialized with sample data')
    conn.commit()
    conn.close()

init_db()

# Pydantic model for user query request
class UserQuery(BaseModel):
    user_id: int

# Generate SHA256 hash key for caching
def make_cache_key(user_id: int):
    raw = f"user:{user_id}"
    return hashlib.sha256(raw.encode()).hexdigest()

# Endpoint to fetch user data with Redis caching
@app.post('/get-user')
def get_user(query: UserQuery):
    cache_key = make_cache_key(query.user_id)
    # Check if data exists in Redis cache
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print('Serving from Redis Cache')
        return json.loads(cached_data)
    
    # Fetch from database if cache miss
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (query.user_id,))
    row = cursor.fetchone()
    conn.close()
    
    # Return error if user not found
    if row is None:
        return {'message': 'User not found.'}
    
    # Format result and cache it for 1 hour (3600 seconds)
    result = {'id': row['id'], 'name': row['name'], 'age': row['age']}
    redis_client.setex(cache_key, 3600, json.dumps(result))
    print('fetched from Db and cached')
    
    return result
