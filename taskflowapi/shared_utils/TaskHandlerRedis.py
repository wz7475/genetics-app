from typing import List

import redis

from .TaskHandler import TasKHandler


class TaskHandlerRedis(TasKHandler):
    def __init__(self, client):
        self.client = client
        self._ready_status = "ready"

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

    def create_subtask(
        self, task_id: str, algorithm: str, batches_ids: List[str]
    ) -> None:
        subtask_link = self._get_subtask_link(task_id, algorithm)
        mapping = {}
        for batch_id in batches_ids:
            mapping[batch_id] = "pending"
        self.client.hset(subtask_link, mapping=mapping)  # subtask object

    def update_subtask_as_done(
        self, task_id: str, algorithm: str, batch_id: str
    ) -> None:
        subtask_link = self._get_subtask_link(task_id, algorithm)
        self.client.hset(subtask_link, batch_id, self._ready_status)

    def check_if_all_subtasks_for_alg_done(self, task_id: str, algorithm: str) -> bool:
        subtask_link = self._get_subtask_link(task_id, algorithm)
        subtask = self.client.hgetall(subtask_link)
        for batch_id in subtask:
            if subtask[batch_id] != self._ready_status:
                return False
        return True

    def get_task_and_subtasks_progress(self, task_id: str) -> dict:
        task = self.client.hgetall(task_id)
        tasks = [key for key in task if key != "status"]
        subtasks = {}
        for algorithm in tasks:
            subtask_link = self._get_subtask_link(task_id, algorithm)
            if self.client.exists(subtask_link):
                algorithm_substask = self.client.hgetall(subtask_link)
                done = 0
                for subtask in algorithm_substask:
                    done += (
                        1 if algorithm_substask[subtask] == self._ready_status else 0
                    )
                # subtasks[algorithm] = f"{done}/{len(algorithm_substask)}"
                subtasks[algorithm] = {
                    "completed": done,
                    "total": len(algorithm_substask),
                }
            else:
                subtasks[algorithm] = "pending"
        return {"status": task, "subtasks": subtasks}

    def _get_subtask_link(self, task_id: str, algorithm: str) -> str:
        return f"{task_id}_{algorithm}"


def get_task_handler_redis() -> TasKHandler:
    redis_host = "redisalg"
    redis_port = 6379
    client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
    return TaskHandlerRedis(client)
