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
        unique_id = properties.headers['unique_id']
        logger.info(f"Received {unique_id}")

        # call algorithm worker eg pangolin with path to filtered file
        for algorithm in ALL_ALGORITHMS:
            alg_input_file_path = database.get_filtered_input_file_for_alg(unique_id, algorithm)
            logger.info(f"Created file without cached variants for {algorithm} - task: {unique_id}")
            channel.basic_publish(
                exchange='',
                routing_key=algorithm,
                body=b"",
                properties=pika.BasicProperties(
                    headers={
                        'unique_id': unique_id,
                        'alg_input_file_path': alg_input_file_path
                    }
                )
            )
            logger.info(f"Enqueued annotating: {algorithm} - {unique_id}")

    channel.basic_consume(queue='orchestrator', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    main()
