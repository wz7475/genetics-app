import logging

import pika

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
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue="parser")
    channel.queue_declare(queue="merger")

    # callback - for caching results to db
    def parse_callback(ch, method, properties, body):
        logger.info("Stated listening on parser")
        output_file_path = properties.headers["output_file_path"]
        alg_name = properties.headers["algorithm"]
        unique_id = properties.headers["unique_id"]
        main_task_id = unique_id.split("_")[0]

        database.save_annotation_from_file_to_db(output_file_path, alg_name, unique_id)
        task_handler.update_subtask_as_done(task_id=main_task_id, algorithm=alg_name, batch_id=unique_id)
        logger.info(f"Saved {alg_name} annotations from: {output_file_path}")

        channel.basic_publish(
            exchange="",
            routing_key="merger",
            body=b"",
            properties=pika.BasicProperties(headers={"unique_id": main_task_id, "algorithm": alg_name}),
        )
        logger.info(f"Enqueued conditional merge for: {main_task_id}")

    # callback - for checking if all done and if ready merging results
    def merge_callback(ch, method, properties, body):
        # TODO: checking if all subtasks done
        logger.info("Stated listening on merger")
        main_task_id = properties.headers["unique_id"]
        alg_name = properties.headers["algorithm"]
        all_requested_algorithms = {}

        # get status of all algorithms
        for algorithm_name in ALL_ALGORITHMS:
            algorithm_status = task_handler.get_task_field(main_task_id, algorithm_name)
            if algorithm_status is not None:
                all_requested_algorithms[algorithm_name] = algorithm_status

        # stop if any not annotated yet
        for algorithm_name in all_requested_algorithms:
            if all_requested_algorithms[algorithm_name] != "annotated":
                alg_subtask_done = task_handler.check_if_all_subtasks_for_alg_done(main_task_id, algorithm_name)
                if not alg_subtask_done:
                    logger.info(f"{main_task_id} at least {algorithm_name} not annotated")
                    return
                task_handler.update_task_field(main_task_id, algorithm_name, "annotated")

        # if all annotated
        database.create_out_file(main_task_id, all_requested_algorithms.keys())
        task_handler.update_task_field(main_task_id, "status", "ready")

    channel.basic_consume(queue="merger", on_message_callback=merge_callback, auto_ack=True)
    channel.basic_consume(queue="parser", on_message_callback=parse_callback, auto_ack=True)
    channel.start_consuming()


if __name__ == "__main__":
    main(RedisHandle(), get_logger(), get_task_handler_redis())
