import pandas as pd

def remove_other_columns(path: str):
    columns = ["Chr", "POS", "Ref", "Alt", "HGVS"]
    df = pd.read_csv(path, sep="\t")
    df = df[columns]
    df.to_csv(path, sep="\t", index=False)