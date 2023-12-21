import pika

from app.logger import get_logger
from app.run_alg import run_alg
from app.data import get_path
from app.config import alg_name


def main(logger=get_logger()):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='pangolin')

    def callback(ch, method, properties, body):
        unique_id = properties.headers['unique_id']
        # TODO ffs I'm veeery dumb, use get_path insted of creating path in db
        input_file_path = properties.headers['input_file_path']
        msg = f"{unique_id}: {body}, \n file path: {input_file_path}"
        logger.info(msg)
        output = get_path(f"{unique_id}_{alg_name}_out")

        # TODO: convert input to required format - tool inside container
        run_alg(input_file_path, output)
        output += ".csv"
        # TODO: convert output to required format - tool inside container
        logger.info(f"path to parsed file: {output}")
        channel.basic_publish(exchange='',
                              routing_key='parser',
                              body=bytes(output, 'utf-8'),
                              properties=pika.BasicProperties(
                                  headers={'unique_id': unique_id, "algorithm": alg_name}
                              ))


    channel.basic_consume(queue='pangolin', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    main()
