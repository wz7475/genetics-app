from abc import ABC, abstractmethod
from typing import List


class TasKHandler(ABC):
    @abstractmethod
    def create_task(self, task_id: str, selected_algorithms: List[str]) -> None:
        pass

    @abstractmethod
    def update_task_field(self, task_id: str, field: str, value: str) -> None:
        pass

    @abstractmethod
    def get_task_field(self, task_id, field: str) -> str:
        pass

    def check_if_field_exists(self, task_id: str, field: str) -> bool:
        pass

    def get_task_and_subtasks_progress(self, task_id: str) -> dict:
        pass

    def create_subtask(self, task_id: str, algorithm: str, batches_ids: List[str]) -> None:
        pass

    def update_subtask_as_done(self, task_id: str, algorithm: str, batch_id: str) -> None:
        pass

    def check_if_all_subtasks_for_alg_done(self, task_id: str, algorithms: str) -> bool:
        pass
