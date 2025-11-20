import hashlib

import redis
import os

CACHE_TTL = 3600

class RedisManager:
    """
    - Connection pooling
    """

    def __init__(self):
        self.redis_client = None
        self.redis_available = False
        # Create connection pool for better performance
        try:
            self.redis_pool = redis.ConnectionPool(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=int(os.getenv('REDIS_DB', 0)),
                password=os.getenv('REDIS_PASSWORD', None),
                decode_responses=True,
                max_connections=20,  # Connection pool size
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )
            self.redis_client = redis.Redis(connection_pool=self.redis_pool)

            # Test connection
            self.redis_client.ping()
            self.redis_available = True
            print("✓ Redis cache connected successfully")
        except (redis.ConnectionError, redis.TimeoutError) as e:
            print(f"Redis unavailable: {e}")

    def setup_redis_connection(self):
        try:
            # Create Redis client from pool
            redis_client = redis.Redis(connection_pool=self.redis_pool)
            return redis_client

        except (redis.ConnectionError, redis.TimeoutError) as e:
            print(f"Redis unavailable: {e}")



    def get_cache_key(prefix: str, *args) -> str:
        """Generate cache key from arguments"""
        key_data = f"{prefix}:{'|'.join(str(arg) for arg in args)}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def get_cache_value(self, location: str) -> str:
        """"Get the data from the cache"""

        redis_client = self.setup_redis_connection()
        cache_key = self.get_cache_key("weather", location)
        cached = redis_client.get(cache_key)
        return cached

    def set_cache_value(self, location: str, weather: str):
        redis_client = self.setup_redis_connection()
        cache_key = self.get_cache_key("weather", location)
        redis_client.setex(cache_key, CACHE_TTL, weather)
