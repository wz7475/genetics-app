import os.path
from uuid import uuid4

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import pika

from shared_utils.logger import get_logger
from .id_genertor import get_uuid4
from .data.SharedVolumeRepo import SharedVolumeRepo
from .utils import count_file_lines
from shared_utils.RedisHandle import RedisHandle

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
    await repo.save_file(file, f"{unique_id}.csv")
    properties = pika.BasicProperties(headers={'unique_id': unique_id})
    channel.basic_publish(exchange='',
                          properties=properties,
                          routing_key='hello',
                          body=bytes(unique_id, encoding='utf-8'))
    return {"message": f"Job enqueued, task id: {unique_id}"}


@app.get("/getResult")
async def get_result(task_id: str) -> File:
    file_path_out = str(await repo.get_file_path(task_id))
    file_path_in = file_path_out.replace("_out", "")  # fast mock of redis tasks for mvp
    if os.path.exists(file_path_out) and count_file_lines(file_path_out) == count_file_lines(file_path_in):
        return FileResponse(file_path_out, filename="result.csv")
    elif os.path.exists(file_path_in):
        return {"message": f"task: {task_id} is in progress"}
    return {"message": f"task {task_id} does not exist"}


# @app.get("/redisRecord")
# async def read_root(key):
#     con = RedisHandle()
#     con.get_data(key)
#     return {"value": f"{con.get_data(key)}"}


@app.get("/redisRecord")
async def read_root(gene: str, chrom: int, pos: int, ref: str, alt: str):
    key = str(gene) + str(chrom) + str(pos) + str(ref) + str(alt)
    con = RedisHandle()
    return {"value": f"{con.get_data(key)}"}

