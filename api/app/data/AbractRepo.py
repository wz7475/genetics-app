from abc import ABC, abstractmethod
from fastapi import UploadFile


class AbstractRepo(ABC):
    @abstractmethod
    async def save_file(self, file: UploadFile, filename: str) -> None:
        pass
