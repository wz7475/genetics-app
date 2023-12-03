import os
from uuid import uuid4

import pika

from app.PseudoRepoCassandra import get_cassandra_session
from app.logger import get_logger
from app.config import data_path
from app.run_alg import run_alg
from app.data import get_path


def main(logger=get_logger()):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    cassandra_session = get_cassandra_session()

    def callback(ch, method, properties, body):
        unique_id = properties.headers['unique_id']
        msg = f"{unique_id}: {body}"
        logger.info(msg)
        input = get_path(f"{unique_id}.tsv")
        output = get_path(f"{unique_id}_out.tsv")
        run_alg(input, output)
        # read properties headers
        cassandra_session.execute("INSERT INTO hello_world (id, message) VALUES (%s, %s);", (uuid4(), msg))

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    get_logger().info(os.listdir())
    main()
