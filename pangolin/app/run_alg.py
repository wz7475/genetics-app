import os

def run_alg(input: str, output: str):
    os.system(f"pangolin {input} GRCh38.primary_assembly.genome.fa.gz gencode.v38.annotation.db {output}")