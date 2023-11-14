from uuid import uuid4

import pika


import logging

# Create or get the logger
logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)  # Set the logging level

# Create handler that logs to stdout
stream_handler = logging.StreamHandler()

# Create formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(stream_handler)

# Example usage
logger.info('This is an info message')

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=0))
    print(1)
    channel = connection.channel()
    print(2)
    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        # with open(f"{uuid4()}.txt", "w") as f:
        #     f.write(body)
        logger.info(f" [x] Received {body}")
        print(f" [x] Received {body}")

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    print("started")
    main()
