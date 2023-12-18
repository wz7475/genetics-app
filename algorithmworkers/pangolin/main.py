import pika

from app.logger import get_logger
from app.run_alg import run_alg
from app.data import get_path
from shared_utils.RedisHandle import RedisHandle


def main(logger=get_logger()):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='pangolin')

    redis = RedisHandle()

    def callback(ch, method, properties, body):
        unique_id = properties.headers['unique_id']
        msg = f"{unique_id}: {body}"
        logger.info(msg)
        input = get_path(f"{unique_id}.csv")
        output = get_path(f"{unique_id}_out")
        # later use run_alg and use quee to inform about finishing the process

        # TODO: convert input to required format - tool inside container
        run_alg(input, output)
        # TODO: convert output to required format - tool inside container
        # read properties headers
        # TODO: enqueue task to parser and checker if all subtasks are done
        redis.input_file(f"{output}.csv")

    channel.basic_consume(queue='pangolin', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    main()
