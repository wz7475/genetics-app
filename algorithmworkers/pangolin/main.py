import pika

from app.logger import get_logger
from app.run_alg import run_alg
from app.data import get_path
from app.config import alg_name
from app.converter import convert_rename_annotation_column


def main(logger=get_logger()):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='pangolin')

    def callback(ch, method, properties, body):
        unique_id = properties.headers['unique_id']

        input_file_path = properties.headers['alg_input_file_path']
        output_file_path = get_path(f"{unique_id}_{alg_name}_out")

        # TODO: convert input to required format - tool inside container
        run_alg(input_file_path, output_file_path)
        output_file_path += ".csv"

        convert_rename_annotation_column(output_file_path)
        logger.info(f"Converted file {output_file_path}")
        # TODO: convert output to required format - more robust tool than function above

        channel.basic_publish(
            exchange='',
            routing_key='parser',
            body=b"",
            properties=pika.BasicProperties(
                headers={
                    'unique_id': unique_id,
                    "algorithm": alg_name,
                    "output_file_path": output_file_path
                }
            )
        )
        logger.info(f"Enqueued parsing: {unique_id}")

    channel.basic_consume(queue='pangolin', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    main()
