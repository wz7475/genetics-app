from abc import ABC, abstractmethod
from typing import List


class TasKHandler(ABC):
    @abstractmethod
    def create_task(self, task_id: str, selected_algorithms: List[str]) -> None:
        pass

    @abstractmethod
    def update_task_field(self, task_id: str, field: str, value: str) -> None:
        pass
