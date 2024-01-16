import os.path

import pandas as pd
import pika

from logger import get_logger
from shared_utils.RedisHandle import RedisHandle
from shared_utils.TaskHandlerRedis import get_task_handler_redis, TasKHandler


def remove_other_columns(path: str):
    columns = ["Chr", "POS", "Ref", "Alt", "HGVS"]
    df = pd.read_csv(path, sep="\t")
    df = df[columns]
    df.to_csv(path, sep="\t", index=False)

def main(task_handler: TasKHandler = get_task_handler_redis(), logger=get_logger()):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='orchestrator')
    database = RedisHandle()

    def callback(ch, method, properties, body):
        unique_id = properties.headers['unique_id']
        all_algorithms = properties.headers['algorithms'].split(",")
        logger.info(f"Received {unique_id}")

        remove_other_columns(os.path.join("data", f"{unique_id}.tsv"))
        for algorithm in all_algorithms:
            alg_input_file_path = database.get_filtered_input_file_for_alg(unique_id, algorithm)
            logger.info(f"Created file without cached variants for {algorithm} - task: {unique_id}")
            channel.basic_publish(
                exchange='',
                routing_key=algorithm,
                body=b"",
                properties=pika.BasicProperties(
                    headers={
                        'unique_id': unique_id,
                        'alg_input_file_path': alg_input_file_path
                    }
                )
            )
            task_handler.update_task_field(unique_id, algorithm, "enqueued")
            logger.info(f"Enqueued annotating: {algorithm} - {unique_id}")

    channel.basic_consume(queue='orchestrator', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    main()
