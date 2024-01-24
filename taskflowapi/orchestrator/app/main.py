import os.path


import pika

from logger import get_logger
from shared_utils.RedisHandle import RedisHandle
from shared_utils.TaskHandlerRedis import get_task_handler_redis, TasKHandler
from utils import remove_other_columns


def publish_message(channel, routing_key, headers):
    channel.basic_publish(
        exchange="",
        routing_key=routing_key,
        body=b"",
        properties=pika.BasicProperties(headers=headers),
    )


def main(task_handler: TasKHandler = get_task_handler_redis(), logger=get_logger()):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq", heartbeat=0)
    )
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
                headers = {
                    "unique_id": unique_id,
                    "alg_input_file_path": alg_input_file_path,
                }
                routing_key = algorithm
            else:
                routing_key = "merger"
                headers = {"unique_id": unique_id}
            # if all cached enqueue merge attempt, else enqueue annotation
            publish_message(channel, routing_key, headers)
            logger.info(f"Published message to {routing_key} - {algorithm} - {unique_id}")

            task_handler.update_task_field(unique_id, algorithm, "enqueued")
            logger.info(f"Enqueued annotating: {algorithm} - {unique_id}")

    channel.basic_consume(
        queue="orchestrator", on_message_callback=callback, auto_ack=True
    )

    channel.start_consuming()


if __name__ == "__main__":
    main()
