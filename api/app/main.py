from uuid import uuid4

from fastapi import FastAPI, UploadFile, File
import pika

from .logger import get_logger
from .id_genertor import get_uuid4
from .data.SharedVolumeRepo import SharedVolumeRepo

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    global connection, channel, logger, repo
    logger = get_logger()
    repo = SharedVolumeRepo()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='hello')


@app.on_event("shutdown")
def shutdown_event():
    connection.close()


@app.get("/")
async def read_root():
    properties = pika.BasicProperties(headers={'unique_id': f"{uuid4()}"})
    channel.basic_publish(exchange='',
                          properties=properties,
                          routing_key='hello',
                          body='Hello World!')
    return {"message": "Job enqueued"}


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    unique_id = get_uuid4()
    await repo.save_file(file, f"{unique_id}.tsv")
    properties = pika.BasicProperties(headers={'unique_id': unique_id})
    channel.basic_publish(exchange='',
                          properties=properties,
                          routing_key='hello',
                          body=bytes(unique_id, encoding='utf-8'))
    return {"message": "Job enqueued"}