import os
from fastapi import File, UploadFile
from .AbractRepo import AbstractRepo
from ..config import data_path


class SharedVolumeRepo(AbstractRepo):

    async def save_file(self, file: UploadFile, filename: str) -> None:
        with open(f"{data_path}/{filename}", "wb") as buffer:
            buffer.write(await file.read())
