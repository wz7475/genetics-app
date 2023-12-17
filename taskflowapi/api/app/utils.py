def count_file_lines(path: str) -> int:
    with open(rf"{path}", 'r') as fp:
        x = len(fp.readlines())
        return x