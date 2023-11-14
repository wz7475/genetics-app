from fastapi import FastAPI
import pika
import json

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    global connection, channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='hello')


@app.on_event("shutdown")
def shutdown_event():
    connection.close()


@app.get("/")
async def read_root():
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body='Hello World!')
    return {"message": "Job enqueued"}
