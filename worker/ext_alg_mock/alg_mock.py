import os
import sys


if __name__ == "__main__":
    input = sys.argv[1]
    output = sys.argv[2]

    os.system(f"cp {input} {output}")