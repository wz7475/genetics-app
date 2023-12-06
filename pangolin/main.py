import os
from uuid import uuid4

import pika

from app.logger import get_logger
from app.config import data_path
from app.run_alg import run_alg
from app.data import get_path
from app.redis_conn import Redis_handle


def main(logger=get_logger()):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    redis = Redis_handle()

    def callback(ch, method, properties, body):
        unique_id = properties.headers['unique_id']
        msg = f"{unique_id}: {body}"
        logger.info(msg)
        input = get_path(f"{unique_id}.csv")
        output = get_path(f"{unique_id}_out")
        # later use run_alg and use quee to inform about finishing the process
        run_alg(input, output)
        # read properties headers
        redis.input_data("lastId", f"{unique_id}")

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    main()
