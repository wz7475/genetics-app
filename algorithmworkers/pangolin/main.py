import pika

from app.logger import get_logger
from app.run_alg import run_alg
from app.data import get_path


def main(logger=get_logger()):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='pangolin')

    def callback(ch, method, properties, body):
        unique_id = properties.headers['unique_id']
        msg = f"{unique_id}: {body}"
        logger.info(msg)
        input = get_path(f"{unique_id}.csv")
        output = get_path(f"{unique_id}_out")

        # TODO: convert input to required format - tool inside container
        run_alg(input, output)
        output += ".csv"
        # TODO: convert output to required format - tool inside container
        logger.info(f"path to parsed file: {output}")
        channel.basic_publish(exchange='',
                              routing_key='parser',
                              body=bytes(output, 'utf-8'),
                              properties=pika.BasicProperties(
                                  headers={'unique_id': unique_id}
                              ))


    channel.basic_consume(queue='pangolin', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    main()
