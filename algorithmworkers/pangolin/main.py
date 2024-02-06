from ..common import Algorithm
import csv
import subprocess
import os


class Pangolin(Algorithm):
    def __init__(self):
        super().__init__("pangolin")

    def get_alg_input_name(self):
        return os.path.join(self.tmp_dir_name, "input.csv")

    def get_alg_output_name(self):
        return os.path.join(self.tmp_dir_name, "output.csv")

    def run(self):
        process = subprocess.Popen(
            [
                "pangolin",
                self.get_alg_input_name(),
                "GRCh38.primary_assembly.genome.fa.gz",
                "gencode.v38.annotation.db",
                os.path.join(self.tmp_dir_name, "output")
            ],
            stdout=subprocess.PIPE,
        )
        process.wait()

        return process.returncode

    def prepare_input(self, input_file_path):
        with open(input_file_path) as input_file, open(self.get_alg_input_name(), mode="w") as alg_input_file:
            source = csv.DictReader(input_file, delimiter="\t")
            dest = csv.DictWriter(
                alg_input_file,
                delimiter=",",
                fieldnames=["CHROM", "POS", "REF", "ALT"],
            )

            dest.writeheader()
            for row in source:
                for column_name in ["Chr", "POS", "Ref", "Alt"]:
                    if column_name not in row.keys():
                        raise AttributeError(f"An input file does not have column with name: {column_name}")
                chromosome = row["Chr"][3:]
                position = row["POS"]
                reference = row["Ref"]
                alternative = row["Alt"]

                dest.writerow(
                    {
                        "CHROM": chromosome,
                        "POS": position,
                        "REF": reference,
                        "ALT": alternative,
                    }
                )

    def prepare_output(self, output_file_path):
        with open(output_file_path, mode="w") as output_file, open(self.get_alg_output_name()) as alg_output_file:
            source = csv.DictReader(alg_output_file, delimiter=",")
            dest = csv.DictWriter(
                output_file,
                delimiter="\t",
                fieldnames=[self.name],
            )

            dest.writeheader()
            for row in source:
                result = row["Pangolin"]

                dest.writerow({self.name: result})


if __name__ == "__main__":
    Pangolin().main()
