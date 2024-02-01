import logging
import os.path
from math import ceil
from uuid import uuid4

import pika

from config import ALG_BATCH_SIZE
from logger import get_logger
from shared_utils.RedisHandle import RedisHandle
from shared_utils.TaskHandlerRedis import get_task_handler_redis, TasKHandler
from utils import remove_other_columns, split_file_into_batches

PATH_PREFIX = os.path.join("/code", "data")


def publish_message(channel, routing_key, headers):
    channel.basic_publish(
        exchange="",
        routing_key=routing_key,
        body=b"",
        properties=pika.BasicProperties(headers=headers),
    )


def process_non_empty_alg_input(
    total_records_in_file: int,
    algorithm: str,
    main_task_id: str,
    alg_input_file_path: str,
    channel: pika.adapters.blocking_connection.BlockingChannel,
    task_handler: TasKHandler,
    logger: logging.Logger,
):
    # create batches
    num_of_batches = ceil(total_records_in_file / ALG_BATCH_SIZE[algorithm])
    batch_ids = [str(uuid4()) for _ in range(num_of_batches)]
    task_id_batch_ids = [f"{main_task_id}_{batch_id}" for batch_id in batch_ids]
    split_file_into_batches(alg_input_file_path, PATH_PREFIX, batch_ids, main_task_id)

    # enqueue batches
    for batch_id in batch_ids:
        headers = {
            "unique_id": f"{main_task_id}_{batch_id}",
            "alg_input_file_path": os.path.join(PATH_PREFIX, f"{main_task_id}_{batch_id}.tsv"),
        }
        publish_message(channel, routing_key=algorithm, headers=headers)
        logger.info(f"Enqueued {algorithm} batch - {batch_id}")

    # update task status
    task_handler.create_subtask(main_task_id, algorithm, task_id_batch_ids)
    task_handler.update_task_field(main_task_id, algorithm, "processing")
    task_handler.update_task_field(main_task_id, "status", "processing")


def process_empty_alg_input(
    channel: pika.adapters.blocking_connection.BlockingChannel,
    algorithm: str,
    main_task_id: str,
    logger: logging.Logger,
):
    publish_message(channel, routing_key="merger", headers={"unique_id": main_task_id})
    logger.info(f"No records for {algorithm}")


def main(task_handler: TasKHandler = get_task_handler_redis(), logger=get_logger()):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue="orchestrator")
    database = RedisHandle()

    def callback(ch, method, properties, body):
        main_task_id = properties.headers["unique_id"]
        all_algorithms = properties.headers["algorithms"].split(",")
        logger.info(f"Received {main_task_id}")

        remove_other_columns(os.path.join("..", "data", f"{main_task_id}.tsv"))
        for algorithm in all_algorithms:
            alg_input_file_path, total_records_in_file = database.get_filtered_input_file_for_alg(
                main_task_id,
                algorithm,
            )
            if total_records_in_file > 0:
                process_non_empty_alg_input(
                    total_records_in_file,
                    algorithm,
                    main_task_id,
                    alg_input_file_path,
                    channel,
                    task_handler,
                    logger,
                )
            else:
                process_empty_alg_input(channel, algorithm, main_task_id, logger)

    channel.basic_consume(queue="orchestrator", on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == "__main__":
    main()
