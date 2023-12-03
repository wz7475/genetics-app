import os
from .config import ext_alg_path

def run_alg(input: str, output: str):
    os.system(f"python3 {ext_alg_path} {input} {output}")