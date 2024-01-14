import logging
import os.path

import pika
import pandas as pd

from logger import get_logger
from shared_utils.RedisHandle import RedisHandle
from shared_utils.AbstractDB import AbstractDB
from shared_utils.TaskHandlerRedis import get_task_handler_redis, TasKHandler
from available_algorithms import ALL_ALGORITHMS  # algs available for user


def main(
    database: AbstractDB,
    logger: logging.Logger,
    task_handler: TasKHandler = get_task_handler_redis(),
):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq", heartbeat=0)
    )
    channel = connection.channel()
    channel.queue_declare(queue="parser")
    channel.queue_declare(queue="merger")

    def parse_callback(ch, method, properties, body):
        logger.info("Stated listening on parser")
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

        channel.basic_publish(
            exchange="",
            routing_key="merger",
            body=b"",
            properties=pika.BasicProperties(headers={"unique_id": unique_id}),
        )
        logger.info(f"Enqueued conditional merge for: {unique_id}")

    def merge_callback(ch, method, properties, body):
        logger.info("Stated listening on merger")
        unique_id = properties.headers["unique_id"]
        all_requested_algorithms = {}

        # get status of all algorithms
        for algorithm_name in ALL_ALGORITHMS:
            algorithm_status = task_handler.get_task_field(unique_id, algorithm_name)
            logger.warning(f"{algorithm_name} status: {algorithm_status} task: {unique_id}")
            if algorithm_status is not None:
                all_requested_algorithms[algorithm_name] = algorithm_status

        logger.warning(all_requested_algorithms)
        # stop if any not annotated yet
        for algorithm_name in all_requested_algorithms:
            if all_requested_algorithms[algorithm_name] != "annotated":
                logger.info(f"{unique_id} at least {algorithm_name} not annotated")
                return

        # if all annotated
        input_file_path = os.path.join("data", f"{unique_id}.tsv")
        output_file_path = os.path.join("data", f"{unique_id}_out.tsv")
        algorithms_output_paths = []
        for algorithm_name in all_requested_algorithms:
            path = os.path.join("data", f"{unique_id}_{algorithm_name}_out.tsv")
            algorithms_output_paths.append(path)

        input_df = pd.read_csv(input_file_path, sep="\t")
        for path in algorithms_output_paths:
            algorithm_df = pd.read_csv(path, sep="\t")
            input_df = pd.concat([input_df, algorithm_df], axis=1)
            logger.info(algorithm_df.columns)
            logger.info(algorithm_df.columns[0] in list(input_df.columns))
        logger.info(input_df.columns[-3:])
        input_df.to_csv(output_file_path, sep="\t", index=False)
        logger.info(f"{unique_id} merged")
        task_handler.update_task_field(unique_id, "status", "ready")

    channel.basic_consume(
        queue="merger", on_message_callback=merge_callback, auto_ack=True
    )
    channel.basic_consume(
        queue="parser", on_message_callback=parse_callback, auto_ack=True
    )
    channel.start_consuming()


if __name__ == "__main__":
    main(RedisHandle(), get_logger(), get_task_handler_redis())
