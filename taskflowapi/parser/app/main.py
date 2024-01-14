import logging

import pika

from logger import get_logger
from shared_utils.RedisHandle import RedisHandle
from shared_utils.AbstractDB import AbstractDB
from shared_utils.TaskHandlerRedis import get_task_handler_redis, TasKHandler



def main(database: AbstractDB, logger: logging.Logger, task_handler: TasKHandler = get_task_handler_redis()):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='parser')


    def callback(ch, method, properties, body):
        output_file_path = properties.headers["output_file_path"]
        alg_name = properties.headers["algorithm"]
        unique_id = properties.headers["unique_id"]

        # database.save_annotation_from_file_to_db(output_file_path, alg_name)
        """
        - temporary skipping caching due to system format migration csv -> tsv
        - logs just to keep track of flow
        """
        task_handler.update_task_field(unique_id, alg_name, "annotated")
        logger.info(f"Saved {alg_name} annotations from: {output_file_path}")

    channel.basic_consume(queue='parser', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    main(RedisHandle(), get_logger(), get_task_handler_redis())
