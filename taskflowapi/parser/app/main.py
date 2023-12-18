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
        path = body.decode('utf-8')
        msg = f"received: {body}"
        logger.info(path)
        database.input_file(path)

    channel.basic_consume(queue='parser', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    main(get_logger(), RedisHandle())
