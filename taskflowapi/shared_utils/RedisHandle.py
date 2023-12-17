import redis
import csv
from .logger import get_logger
from .AbstractDB import AbstractDB


class RedisHandle(AbstractDB):
    def __init__(self):
        redis_host = 'redisalg'
        redis_port = 6379
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

    def get_data(self, key):
        value = self.redis_client.get(key)
        get_logger().info(f"Read data from Redis: Key='{key}', Value='{value}'")
        if value is not None:
            return value
        else:
            return f"No data found for key: {key}"

    def input_data(self, key, value):
        # Set a key-value pair in Redis
        self.redis_client.set(key, value)
        get_logger().info(f"Stored data in Redis: Key='{key}', Value='{value}'")

    def input_file(self, filepath):
        """
        for now only csv files, after demo handle all sorts of files with fileparser or sth like that
        :param filepath: path to file that is adnotated to be calculated
        :return:
        """
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                key = "".join(tuple(row.values())[:-1])
                value = row['Pangolin']
                self.input_data(key, value)
