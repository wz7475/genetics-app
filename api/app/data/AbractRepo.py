from abc import ABC, abstractmethod
from fastapi import UploadFile


class AbstractRepo(ABC):
    @abstractmethod
    async def save_file(self, file: UploadFile, filename: str) -> None:
        pass

    @abstractmethod
    async def get_file_path(self, task_id: str) -> str:
        """
        gets task id and returns the filepath if file exists
        :param task_id:
        :return: filepath
        """
        pass
