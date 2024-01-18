import pika
import os
import tempfile
from abc import ABC, abstractmethod

from .logger import get_logger


class Algorithm(ABC):
    def __init__(self, name):
        self.connection = None
        self.channel = None

        self.name = name

        self.data_path = "/code/data"

        self.logger = get_logger(self.name)

    def main(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq", heartbeat=0)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.name)

        self.channel.basic_consume(
            queue=self.name, on_message_callback=self.task_callback, auto_ack=True
        )

        self.channel.start_consuming()

    def task_callback(self, ch, method, properties, body):
        unique_id = properties.headers["unique_id"]

        input_file_path = properties.headers["alg_input_file_path"]
        output_file_path = os.path.join(
            self.data_path, f"{unique_id}_{self.name}_out.tsv"
        )

        self.process_task(input_file_path, output_file_path)

        self.channel.basic_publish(
            exchange="",
            routing_key="parser",
            body=b"",
            properties=pika.BasicProperties(
                headers={
                    "unique_id": unique_id,
                    "algorithm": self.name,
                    "output_file_path": output_file_path,
                }
            ),
        )
        self.logger.info(f"Enqueued parsing: {unique_id}")

    def process_task(self, input_file_path, output_file_path):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            self.tmp_dir_name = tmp_dir_name
            self.prepare_input(input_file_path)
            self.logger.info(f"Prepared input file {input_file_path}")

            return_code = self.run()

            self.logger.info(
                f"{self.name} DONE for {input_file_path}, ret code: {return_code}"
            )
            self.logger.info(f"prepering output for file: {output_file_path}")
            self.prepare_output(output_file_path)

        self.tmp_dir_name = None

        self.logger.info(f"Converted file {output_file_path}")

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def prepare_input(self, input_file_path):
        pass

    @abstractmethod
    def prepare_output(self, output_file_path):
        pass
