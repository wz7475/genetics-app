import os.path
from typing import Annotated
from uuid import uuid4

from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.responses import FileResponse
import pika

from shared_utils.logger import get_logger
from .data.SharedVolumeRepo import SharedVolumeRepo
from .utils import count_file_lines, get_uuid4
from shared_utils.RedisHandle import RedisHandle
from shared_utils.TaskHandler import TasKHandler
from shared_utils.TaskHandlerRedis import get_task_handler_redis

app = FastAPI()


@app.post("/uploadfile")
async def create_upload_file(
    task_handler: TasKHandler = Depends(get_task_handler_redis),
    file: UploadFile = File(...),
):
    unique_id = get_uuid4()
    await repo.save_file(file, f"{unique_id}.tsv")
    task_handler.create_task(unique_id, ["pangolin", "spip"])
    channel.basic_publish(
        exchange="",
        routing_key="orchestrator",
        body=b"",
        properties=pika.BasicProperties(
            headers={"unique_id": unique_id, "algorithms": "pangolin,spip"}
        ),
    )
    return {"message": f"Job enqueued, task id: {unique_id}"}


@app.on_event("startup")
async def startup_event():
    global connection, channel, logger, repo
    logger = get_logger()
    repo = SharedVolumeRepo()
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq", heartbeat=0)
    )
    channel = connection.channel()
    channel.queue_declare(queue="hello")
    con = RedisHandle()


@app.on_event("shutdown")
def shutdown_event():
    connection.close()


@app.get("/test")
async def read_root():
    return {"message": "Job enqueued"}


@app.get("/getResult")
async def get_result(task_id: str) -> File:
    file_path_out = str(await repo.get_file_path(task_id))
    file_path_in = file_path_out.replace("_out", "")  # fast mock of redis tasks for mvp
    if os.path.exists(file_path_out) and count_file_lines(
        file_path_out
    ) == count_file_lines(file_path_in):
        return FileResponse(file_path_out, filename="result.csv")
    # TODO: use redis to store tasks and check if task is in progress
    elif os.path.exists(file_path_in):
        return {"message": f"task: {task_id} is in progress"}
    return {"message": f"task {task_id} does not exist"}


@app.get("/redisRecord")
async def read_root(gene: str, chrom: int, pos: int, ref: str, alt: str):
    key = str(gene) + str(chrom) + str(pos) + str(ref) + str(alt)
    con = RedisHandle()
    return {"value": f"{con.get_data(key)}"}


@app.get("/redisRecordHard")
async def read_root(key: str):
    con = RedisHandle()
    return {"value": f"{con.get_data(key)}"}


@app.get("/createOuput")
async def read_root(id: str):
    con = RedisHandle()
    con.create_out_file(os.path.join("data", id))
    return {"state": "success"}
