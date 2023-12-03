from fastapi import FastAPI, File, UploadFile
import pika
import json
# from connect import saveFile  #TODO import does not
import logging

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

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    logging.info("Upload file method called, recived file with name: ", file.filename)
    saveFile(file.file, "aa")
    return {"filename": file.filename}



# from minio import Minio
# from minio.error import S3Error
# from io import BytesIO


# def saveFile(file: BytesIO, taskID: str):
#     client = Minio(
#         endpoint="127.0.0.1:9000",
#         secure=False,
#         access_key="ROOTUSER",
#         secret_key="CHANGEME123",
#     )

#     bucketName = "user-input"
#     found = client.bucket_exists(bucketName)
#     if not found:
#         client.make_bucket(bucketName)


#     client.fput_object(bucketName, "taskID", file)