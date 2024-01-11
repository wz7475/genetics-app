import os

from .config import data_path


def get_path(filename: str) -> str:
    return os.path.join(data_path, filename)