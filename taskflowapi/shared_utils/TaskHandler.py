from abc import ABC, abstractmethod
from typing import List


class TasKHandler(ABC):

    @abstractmethod
    def create_task(self, task_id: str, selected_algorithms: List[str]):
        pass