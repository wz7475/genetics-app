import redis
from .logger import get_logger


class Redis_handle:
    def __init__(self):
        redis_host = 'redisalg'
        redis_port = 6379
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

    def input_data(self, key, value):
        # Set a key-value pair in Redis
        self.redis_client.set(key, value)
        get_logger().info(f"Stored data in Redis: Key='{key}', Value='{value}'")
