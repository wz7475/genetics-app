import os.path

from fastapi import FastAPI, UploadFile, File, Depends, Body
from fastapi.responses import FileResponse
import pika

from shared_utils.logger import get_logger
from .data.SharedVolumeRepo import SharedVolumeRepo
from .utils import get_uuid4
from shared_utils.RedisHandle import RedisHandle
from shared_utils.TaskHandler import TasKHandler
from shared_utils.TaskHandlerRedis import get_task_handler_redis

app = FastAPI()


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
    RedisHandle()  # con = ...


@app.on_event("shutdown")
def shutdown_event():
    connection.close()


@app.post("/uploadFile")
async def create_upload_file(
        task_handler: TasKHandler = Depends(get_task_handler_redis),
        file: UploadFile = File(...),
):
    unique_id = get_uuid4()
    await repo.save_file(file, f"{unique_id}.tsv")
    task_handler.create_task(unique_id, ["spip"]) # TODO add pangolin
    channel.basic_publish(
        exchange="",
        routing_key="orchestrator",
        body=b"",
        properties=pika.BasicProperties(
            headers={"unique_id": unique_id, "algorithms": "spip"} # TODO add pangolin
        ),
    )
    return {"message": "success", "id": unique_id}


@app.post("/getResult")
async def get_result(
        task_id: str = Body(default=None),
        task_handler: TasKHandler = Depends(get_task_handler_redis),
) -> File:
    if task_handler.get_task_field(task_id, "status") == "ready":
        path = os.path.join("data", f"{task_id}_out.tsv")
        return FileResponse(path, filename="result.tsv")

    if task_handler.check_if_field_exists(task_id, "status"):
        return {"message": f"task: {task_id} is in progress"}

    return {"message": f"task {task_id} does not exist"}


@app.post("/getStatus")
async def get_status(
        task_id: str = Body(default=None),
        task_handler: TasKHandler = Depends(get_task_handler_redis)
) -> dict:
    if task_handler.check_if_field_exists(str(task_id), "status"):
        status = task_handler.get_task_field(task_id, "status")
        return {"status": str(status)}

    return {"status": "expired"}


@app.post("/getRedisValue")
async def get_redis_val(
        key=Body(default=None),
        task_handler: TasKHandler = Depends(get_task_handler_redis)
) -> dict:
    db = RedisHandle()
    return {"result": str(db.get_data(str(key)))}
