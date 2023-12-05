from uuid import uuid4

import pika

from worker.app.PseudoRepoCassandra import get_cassandra_session
from worker.app.logger import get_logger


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
