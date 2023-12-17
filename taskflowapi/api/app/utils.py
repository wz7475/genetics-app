from uuid import uuid4


def count_file_lines(path: str) -> int:
    with open(rf"{path}", 'r') as fp:
        x = len(fp.readlines())
        return x


def get_uuid4() -> str:
    return str(uuid4())
