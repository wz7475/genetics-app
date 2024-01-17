from typing import List

from TaskHandler import TasKHandler
import redis


class TaskHandlerRedis(TasKHandler):
    def __init__(self, client):
        self.client = client

    def create_task(self, task_id: str, selected_algorithms: List[str]) -> None:
        content = {"status": "pending"}
        for algorithm in selected_algorithms:
            content[algorithm] = "pending"
        self.client.hset(
            task_id,
            mapping=content,
        )

    def update_task_field(self, task_id: str, field: str, value: str) -> None:
        self.client.hset(task_id, field, value)

    def get_task_field(self, task_id, field: str) -> str:
        return self.client.hget(task_id, field)

    def check_if_field_exists(self, task_id: str, field: str) -> bool:
        return bool(self.client.hexists(task_id, field))


def get_task_handler_redis() -> TasKHandler:
    redis_host = "localhost"
    redis_port = 6379
    client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
    return TaskHandlerRedis(client)

if __name__ == "__main__":
    th = get_task_handler_redis()
    print(th.check_if_field_exists("a97af5e2-fa4d-428d-9b7b-97b2d6999372", "status"))