import redis
import json
import hashlib
import httpx
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
# Initialize Redis client connection to local Redis server
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Define request model for post ID validation
class PostRequest(BaseModel):
    post_id: int
    
# Generate a hashed cache key to store/retrieve posts from Redis
def make_cache_key(post_id: int):
    """
    Creates a SHA256 hashed cache key based on post_id.
    Args:
        post_id: The ID of the post to fetch
    Returns:
        Hashed string used as Redis key
    """
    raw = f"external_api:post_{post_id}"
    return hashlib.sha256(raw.encode()).hexdigest()

# FastAPI endpoint to fetch a post with caching logic
@app.post('/get-post')
async def get_post(data: PostRequest):
    """
    Fetches a post from external API with Redis caching.
    Returns cached data if available, otherwise calls external API.
    """
    # Generate cache key for the requested post
    cache_key = make_cache_key(data.post_id)
    
    # Check if post data exists in Redis cache
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print('Served from Redis cache!')
        return json.loads(cached_data)
    
    # If not cached, fetch from external API
    print('Calling external API...')
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://jsonplaceholder.typicode.com/posts/{data.post_id}")
        
        # Handle failed API request
        if response.status_code != 200:
            return {'error': 'Post not found'}
        
        # Parse response and cache for 600 seconds (10 minutes)
        post_data = response.json()
        redis_client.setex(cache_key, 600, json.dumps(post_data))
        print('Fetched and stored in Cache')
        return post_data