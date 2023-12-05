import os
from fastapi import File, UploadFile
from .AbractRepo import AbstractRepo
from ..config import data_path
class SharedVolumeRepo(AbstractRepo):

    def save_file(file: UploadFile) -> None:
        pass
        # save file om data_path