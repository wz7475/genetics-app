import redis
from .logger import get_logger


class Redis_handle:
    def __init__(self):
        redis_host = 'redisalg'
        redis_port = 6379
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

    def get_data(self, key):
        """
        get value from data
        :param key:
        :return:
        """
        value = self.redis_client.get(key)
        get_logger().info(f"Read data from Redis: Key='{key}', Value='{value}'")
        if value is not None:
            return value
        else:
            return f"No data found for key: {key}"
