from uuid import uuid4
from io import IOBase

from config import LIST_OF_COLUMNS_PANGOLIN, LIST_OF_COLUMNS_SPIP


def count_file_lines(path: str) -> int:
    with open(rf"{path}", 'r') as fp:
        x = len(fp.readlines())
        return x


def get_uuid4() -> str:
    return str(uuid4())


def validate_input_file(input_file: IOBase, algorithms: list[str]) -> None:
    list_of_obligatory_columns = []
    if 'pangolin' in algorithms:
        list_of_obligatory_columns.extend(LIST_OF_COLUMNS_PANGOLIN)
    if 'spip' in algorithms:
        list_of_obligatory_columns.extend(LIST_OF_COLUMNS_SPIP)

    num_columns = len(list_of_obligatory_columns)
    columns_string = input_file.readlines(1)[0].replace('\n', '')

    for obligatory_column in list_of_obligatory_columns:
        if obligatory_column not in columns_string.split('\t'):
            raise AttributeError(obligatory_column)

    number_of_tabulators_in_row = columns_string.count('\t')
    if any([delimiter in columns_string for delimiter in [' ', ',', ', ']]) or number_of_tabulators_in_row < num_columns - 1:
        raise ValueError("Input file should only have tabulators as delimiters")

    for row in input_file.readlines():
        if row.count('\t') != number_of_tabulators_in_row:
            raise ValueError("Input file should have tabulators as delimiters, " +
                             "and all rows should have same amount of columns")
