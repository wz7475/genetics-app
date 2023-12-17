import pika

from logger import get_logger



def main(logger=get_logger()):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='orchestrator')


    def callback(ch, method, properties, body):
        msg = f"received: {body}"
        logger.info(msg)

        # call algorithm worker eg pangolin


    channel.basic_consume(queue='orchestrator', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    main()
