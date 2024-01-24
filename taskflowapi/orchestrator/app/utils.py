import os.path
from math import ceil
from typing import List

import pandas as pd


def remove_other_columns(path: str):
    columns = ["Chr", "POS", "Ref", "Alt", "HGVS"]
    df = pd.read_csv(path, sep="\t")
    df = df[columns]
    df.to_csv(path, sep="\t", index=False)


def split_file_into_batches(input_file_path: str, output_dir_path: str, batch_ids: List[str], task_id: str):
    num_of_batches = len(batch_ids)
    with open(input_file_path) as input_fp:
        input_lines = input_fp.readlines()
        header, records = [input_lines[0]], input_lines[1:]
        batch_size = ceil(len(records) / num_of_batches)
        for batch_idx, batch_id in enumerate(batch_ids):
            batch_file = os.path.join(output_dir_path, f"{task_id}_{batch_id}.tsv")
            with open(batch_file, "w") as batch_fp:
                records_start_offset = batch_idx * batch_size
                records_end_offset = batch_idx * batch_size + batch_size
                records_end_offset = len(records) if records_end_offset > len(records) else records_end_offset
                batch_input = header + records[records_start_offset:records_end_offset]
                batch_fp.writelines(batch_input)

if __name__ == "__main__":
    input = "taskflowapi/data/2rec.tsv"
    output = "docs"
    bath_ids = ["1", "2"]
    task_id = "abc"
    split_file_into_batches(input, output, bath_ids, task_id)