import itertools
from typing import Tuple

import redis
import os
import csv
from .logger import get_logger
from .AbstractDB import AbstractDB

PATH_PREFIX = os.path.join("/code", "data")


class RedisHandle(AbstractDB):
    def __init__(self):
        redis_host = 'redisalg'
        redis_port = 6379
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
        self.fildnames = ["Chr", "POS", "Ref", "Alt", "HGVS"]

    def _check_if_key_exists(self, key: str) -> bool:
        if self.redis_client.get(key) is None:
            return False
        return True

    def get_data(self, key) -> str:
        value = self.redis_client.get(key)
        if value is not None:
            return value
        else:
            return False

    def input_data(self, key, value):
        self.redis_client.set(key, value)

    def save_annotation_from_file_to_db(self, filepath, alg_name, task_id):
        """
        enters records from file into db

        :param filepath:
        :param alg_name:
        :param task_id:
        :return:
        """
        original_file = os.path.join(PATH_PREFIX, f"{task_id}.tsv")
        with open(original_file, newline='') as tsvfile, \
                open(filepath) as out_file:
            source = csv.DictReader(tsvfile, delimiter="\t", fieldnames=self.fildnames)
            out_file.readline()  # read header
            for row in itertools.islice(source, 1, None):
                key = self.get_key_from_tsv(row, alg_name)
                value = out_file.readline()
                self.input_data(key, value[:-1])  # cut out \n

    def get_filtered_input_file_for_alg(self, task_id, algorythm) -> Tuple[str, int]:
        """
        functions creates new filtered file for annotation specific algorythm

        :param task_id:
        :param algorythm:
        :return:
        """
        in_filepath = os.path.join(PATH_PREFIX, f"{task_id}.tsv")
        out_filepath = os.path.join(PATH_PREFIX, f"{task_id}_{algorythm}.tsv")
        total_records_in_file = 0

        with open(in_filepath) as in_file, \
                open(out_filepath, 'w') as out_file:
            source = csv.DictReader(in_file, delimiter="\t", fieldnames=self.fildnames)

            first_line = "\t".join(source.fieldnames) + "\n"
            out_file.write(first_line)

            for row in itertools.islice(source, 1, None):
                row: dict
                key = self.get_key_from_tsv(row, algorythm)
                if not self.get_data(key):
                    out_file.write("\t".join(row.values()) + "\n")
                    total_records_in_file += 1

        get_logger().info(f"Created new out file without annotated variants for {algorythm}, {task_id}")
        return out_filepath, total_records_in_file

    def create_out_file(self, task_id, algorithms):
        """
        creates output file for user based on algorithms and task id

        :param task_id:
        :param algorithms:
        :return:
        """
        in_filepath = os.path.join(PATH_PREFIX, f"{task_id}.tsv")
        out_filepath = os.path.join(PATH_PREFIX, f"{task_id}_out.tsv")

        alg_names = "\t".join(algorithms)
        with open(in_filepath) as in_file, \
                open(out_filepath, 'w') as out_file:
            source = csv.DictReader(in_file, delimiter="\t", fieldnames=self.fildnames)
            first_line = "\t".join(source.fieldnames) + f"\t{alg_names}\n"
            out_file.write(first_line)
            in_file.readline()  # read headers

            for row in source:
                row: dict
                values = ""
                for algorythm in algorithms:
                    key = self.get_key_from_tsv(row, algorythm)
                    values += f"{self.get_data(key)}\t"
                    # get_logger().warn(f"{algorythm}, {key}, {values}")
                out_file.write("\t".join(row.values()) + f'\t{values}\n')
        get_logger().info(f"Created out file for task: {task_id}")

    def get_key_from_tsv(self, row: dict, algorythm: str) -> str:
        # get_logger().info(row.keys())
        chromosome = row["Chr"][3:]
        position = row["POS"]
        reference = row["Ref"]
        alternative = row["Alt"]
        return f"{algorythm},{chromosome},{position},{reference},{alternative}"
