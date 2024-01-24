import os.path
from uuid import uuid4

import pika

from logger import get_logger
from shared_utils.RedisHandle import RedisHandle
from shared_utils.TaskHandlerRedis import get_task_handler_redis, TasKHandler
from utils import remove_other_columns, split_file_into_batches
from math import ceil
from config import ALG_BATCH_SIZE

PATH_PREFIX = os.path.join("/code", "data")


def publish_message(channel, routing_key, headers):
    channel.basic_publish(
        exchange="",
        routing_key=routing_key,
        body=b"",
        properties=pika.BasicProperties(headers=headers),
    )


def main(task_handler: TasKHandler = get_task_handler_redis(), logger=get_logger()):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue="orchestrator")
    database = RedisHandle()

    def callback(ch, method, properties, body):
        unique_id = properties.headers["unique_id"]
        all_algorithms = properties.headers["algorithms"].split(",")
        logger.info(f"Received {unique_id}")

        remove_other_columns(os.path.join("..", "data", f"{unique_id}.tsv"))
        for algorithm in all_algorithms:
            (
                alg_input_file_path,
                total_records_in_file,
            ) = database.get_filtered_input_file_for_alg(unique_id, algorithm)
            if total_records_in_file > 0:
                num_of_batches = ceil(total_records_in_file / ALG_BATCH_SIZE[algorithm])
                batch_ids = [str(uuid4()) for _ in range(num_of_batches)]
                split_file_into_batches(alg_input_file_path, PATH_PREFIX, batch_ids, unique_id)
                for batch_id in batch_ids:
                    headers = {
                        "unique_id": f"{unique_id}_{batch_id}",
                        "alg_input_file_path": os.path.join(PATH_PREFIX, f"{unique_id}_{batch_id}.tsv")
                    }
                    publish_message(channel, routing_key=algorithm, headers=headers)
                    logger.info(f"Enqueued {algorithm} batch - {batch_id}")
                # TODO update alg field with list containing task_id_batch_id's
                # task_handler.update_task_field(unique_id, algorithm, [hdyz, hydż])
            else:
                publish_message(channel, routing_key="merger", headers={"unique_id": unique_id})
                logger.info(f"No records for {algorithm}")


    channel.basic_consume(queue="orchestrator", on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == "__main__":
    main()
