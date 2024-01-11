import redis
import os
import csv
from .logger import get_logger
from .AbstractDB import AbstractDB


class RedisHandle(AbstractDB):
    def __init__(self):
        redis_host = 'redisalg'
        redis_port = 6379
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

    def _check_if_key_exists(self, key: str) -> bool:
        if self.redis_client.get(key) is None:
            return False
        return True

    def get_data(self, key) -> str:
        value = self.redis_client.get(key)
        get_logger().info(f"Read data from Redis: Key='{key}', Value='{value}'")
        if value is not None:
            return value
        else:
            return False

    def input_data(self, key, value):
        # Set a key-value pair in Redis
        self.redis_client.set(key, value)
        # get_logger().info(f"Stored data in Redis: Key='{key}', Value='{value}'")

    def save_annotation_from_file_to_db(self, filepath):
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
        get_logger().info(f"Stored data in Redis from file: {filepath}")

    def get_filtered_input_file_for_alg(self, task_id, algorythm):
        """
        @TODO please make many func out of this, I know its bad, just for demo "muliple in one"

        :param task_id:
        :param algorythm:
        :return:
        """
        in_filepath = os.path.join("data", f"{task_id}.csv")
        out_filepath = os.path.join("data", f"{task_id}_{algorythm}.csv")
        with open(in_filepath) as in_file, \
                open(out_filepath, 'w') as out_file:
            out_file.write(in_file.readline())
            for line in in_file.readlines():
                key = line.replace(",", "")[:-1]  # new line at the end
                if not self.get_data(key):
                    out_file.write(line)
                    get_logger().info(f"No data for key: '{key}'")
                    # pass
        get_logger().info(f"Created new out file without annotated variants")
        return out_filepath

    def create_out_file(self, task_id):
        # in_filepath = os.path.join("data", f"{task_id}.csv")
        in_filepath = f"{task_id}.csv"
        # out_filepath = os.path.join("data", f"{task_id}_out.csv")
        out_filepath = f"{task_id}_out.csv"
        with open(in_filepath) as in_file, \
                open(out_filepath, 'w') as out_file:
            out_file.write(f"{in_file.readline()[:-1]},RESULT\n")
            for line in in_file.readlines():
                key = line.replace(",", "")[:-1]
                value = self.get_data(key)
                out_file.write(f'{line[:-1]},{value}\n')
        get_logger().info(f"Created out file for user")
