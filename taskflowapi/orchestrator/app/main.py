import pika

from logger import get_logger
from algorithms.config import ALL_ALGORITHMS
from shared_utils.RedisHandle import RedisHandle


def main(logger=get_logger()):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='orchestrator')
    database = RedisHandle()

    def callback(ch, method, properties, body):
        body = body.decode('utf-8')
        msg = f"received: {body}"
        logger.info(msg)

        # call algorithm worker eg pangolin with path to filtered file
        for algorithm in ALL_ALGORITHMS:
            input_file_path = database.get_input_file(body, algorithm)
            if not input_file_path:
                continue
            channel.basic_publish(exchange='',
                                  routing_key=algorithm,
                                  body=body,
                                  properties=pika.BasicProperties(
                                      headers={'unique_id': body,
                                               'input_file_path': input_file_path}
                                  ))

    channel.basic_consume(queue='orchestrator', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    main()
