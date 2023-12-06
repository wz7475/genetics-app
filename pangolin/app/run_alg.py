import os
import subprocess
from .logger import get_logger


def run_alg(input: str, output: str):
    process = subprocess.Popen(f"pangolin {input} GRCh38.primary_assembly.genome.fa.gz gencode.v38.annotation.db {output}", shell=True, stdout=subprocess.PIPE)
    process.wait()
    get_logger().info(f"pangolin DONE: {process.returncode}")
    return process.returncode
    # os.system(f"pangolin {input} GRCh38.primary_assembly.genome.fa.gz gencode.v38.annotation.db {output}")  #database version important!!!
    # get_logger().info("pangolin DONE")

