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
        self.redis_client.set(key, value)

    def save_annotation_from_file_to_db(self, filepath, alg_name):
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                key = "".join(tuple(row.values())[:-1])
                key += alg_name
                value = row[alg_name]
                self.input_data(key, value)

    def get_filtered_input_file_for_alg(self, task_id, algorythm):
        """
        functions creates new filtered file for annotation specific algorythm

        :param task_id:
        :param algorythm:
        :return:
        """
        in_filepath = os.path.join("data", f"{task_id}.tsv")
        out_filepath = os.path.join("data", f"{task_id}_{algorythm}.tsv")

        with open(in_filepath) as in_file, \
                open(out_filepath, 'w') as out_file:
            out_file.write(in_file.readline()) # copy header
            source = csv.DictReader(in_file, delimiter="\t")

            for row in source:
                line = in_file.readline()
                key = self.get_key_from_tsv(row)
                if not self.get_data(key):
                    out_file.write(line)

        get_logger().info(f"Created new out file without annotated variants for {algorythm}, {task_id}")
        return out_filepath

    def create_out_file(self, task_id):
        in_filepath = f"{task_id}.csv"
        out_filepath = f"{task_id}_out.csv"
        with open(in_filepath) as in_file, \
                open(out_filepath, 'w') as out_file:
            out_file.write(f"{in_file.readline()[:-1]},RESULT\n")
            for line in in_file.readlines():
                key = line.replace(",", "")[:-1]
                value = self.get_data(key)
                out_file.write(f'{line[:-1]},{value}\n')
        get_logger().info(f"Created out file for user")

    def read_keys_tsv(self, input_file):
        """
        Should it be in this class? probably not
        :param input_file:
        :return:
        """
        source = csv.DictReader(input_file, delimiter="\t")
        keys = []
        for row in source:
            chromosome = row["Chr"][3:]
            position = row["POS"]
            reference = row["Ref"]
            alternative = row["Alt"]
            key = f"{chromosome},{position},{reference},{alternative}"
            keys.append(key)
        return keys

    def get_key_from_tsv(self, row) -> str:
        chromosome = row["Chr"][3:]
        position = row["POS"]
        reference = row["Ref"]
        alternative = row["Alt"]
        return f"{chromosome},{position},{reference},{alternative}"