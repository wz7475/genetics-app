from uuid import uuid4

from fastapi import FastAPI, UploadFile, File
import pika

from .logger import get_logger
from .config import data_path
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
    logger.info("Upload file method called, recived file with name: ", file.filename)
    await repo.save_file(file, file.filename)
    # TODO send message
    return {"filename": file.filename}
