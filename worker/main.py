import os
from uuid import uuid4

import pika

from app .PseudoRepoCassandra import get_cassandra_session
from .logger import get_logger
from .config import data_path
from .run_alg import run_alg
temp_file_path = os.path.join(data_path, "temp_file.txt")

def main(logger=get_logger()):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    cassandra_session = get_cassandra_session()

    def callback(ch, method, properties, body):
        msg = f"Received {body}"
        logger.info(msg)
        run_alg(temp_file_path, temp_file_path + f"{uuid4()}.txt")
        cassandra_session.execute("INSERT INTO hello_world (id, message) VALUES (%s, %s);", (uuid4(), msg))

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    os.system("touch " + temp_file_path)
    main()
