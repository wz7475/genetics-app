import os.path

from fastapi import FastAPI, UploadFile, File, Depends, Body
from fastapi.responses import FileResponse
import pika
from pydantic import BaseModel

from shared_utils.logger import get_logger

from .repositories.SharedVolumeRepo import SharedVolumeRepo
from .utils import get_uuid4, validate_input_file, MissingColumnException
from shared_utils.RedisHandle import RedisHandle
from shared_utils.TaskHandler import TasKHandler
from shared_utils.TaskHandlerRedis import get_task_handler_redis
from available_algorithms import ALL_ALGORITHMS

app = FastAPI()


class UploadFileBody(BaseModel):
    algorithms: list[str] = ["pangolin", "spip"]


class BodyTaskId(BaseModel):
    task_id: str = None


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
        algorithms: UploadFileBody = UploadFileBody()
):

    try:
        validate_input_file(file.file, algorithms.algorithms)
    except MissingColumnException as missing_column_name:
        return {"message": "failed", "reason": f"Input file missing '{missing_column_name}' column."}
    except ValueError as reason:
        return {"message": "failed", "reason": f"{reason}"}

    main_task_id = get_uuid4()
    file.file.seek(0)
    await repo.save_file(file, f"{main_task_id}.tsv")

    # create task to track progress
    task_handler.create_task(main_task_id, algorithms.algorithms)

    # send msg - initialize annotation pipeline for input file
    channel.basic_publish(
        exchange="",
        routing_key="orchestrator",
        body=b"",
        properties=pika.BasicProperties(
            headers={"unique_id": main_task_id, "algorithms": ','.join(algorithms)}
        ),
    )
    return {"message": "success", "id": main_task_id}


@app.post("/getResult")
async def get_result(
    task_id: BodyTaskId,
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
    task_id: BodyTaskId,
    task_handler: TasKHandler = Depends(get_task_handler_redis),
) -> dict:
    if task_handler.check_if_field_exists(str(task_id), "status"):
        status = task_handler.get_task_field(task_id, "status")
        return {"status": str(status)}

    return {"status": "expired"}


@app.get("/availableAlgorithms")
async def get_available_algorithms() -> dict:
    return {"algorithms": ALL_ALGORITHMS}


@app.post("/getDetailedStatus")
async def get_detailed_status(
    task_id: BodyTaskId,
    task_handler: TasKHandler = Depends(get_task_handler_redis),
) -> dict:
    if task_handler.check_if_field_exists(str(task_id), "status"):
        status = task_handler.get_task_and_subtasks_progress(task_id)
        return status

    return {"status": "expired"}


@app.post("/getRedisValue")
async def get_redis_val(
    key=Body(default=None), task_handler: TasKHandler = Depends(get_task_handler_redis)
) -> dict:
    db = RedisHandle()
    return {"result": str(db.get_data(str(key)))}
