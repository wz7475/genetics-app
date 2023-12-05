from uuid import uuid4

import pika


import logging

from cassandra.cluster import Cluster


def get_logger():
    logger = logging.getLogger('MyLogger')
    logger.setLevel(logging.INFO)  # Set the logging level
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_cassandra_session():
    cluster = Cluster(['cassandra'])
    session = cluster.connect()
    session.execute(
        "CREATE KEYSPACE IF NOT EXISTS example WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};")
    session.execute("USE example;")
    return session

def main(logger=get_logger()):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    cassandra_session = get_cassandra_session()

    def callback(ch, method, properties, body):
        msg = f" [x] Received {body}"
        logger.info(msg)
        cassandra_session.execute("INSERT INTO hello_world (id, message) VALUES (%s, %s);", (uuid4(), msg))
        print(f" [x] Received {body}")

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    print("started")
    main()
