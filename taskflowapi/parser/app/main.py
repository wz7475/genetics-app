import logging

import pika

from logger import get_logger
from shared_utils.RedisHandle import RedisHandle
from shared_utils.AbstractDB import AbstractDB


def main(logger: logging.Logger, database: AbstractDB):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='parser')


    def callback(ch, method, properties, body):
        output_file_path = properties.headers["output_file_path"]
        alg_name = properties.headers["algorithm"]

        database.save_annotation_from_file_to_db(output_file_path, alg_name)
        logger.info(f"Saved {alg_name} annotations from: {output_file_path}")

    channel.basic_consume(queue='parser', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    main(get_logger(), RedisHandle())
