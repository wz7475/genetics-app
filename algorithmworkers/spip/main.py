from ..common import Algorithm
import csv
import subprocess
import os


class SPIP(Algorithm):
    def __init__(self):
        super().__init__("spip")

    def get_alg_input_name(self):
        return os.path.join(self.tmp_dir_name, "input.txt")

    def get_alg_output_name(self):
        return os.path.join(self.tmp_dir_name, "output.txt")

    def run(self):
        process = subprocess.Popen(
            f"Rscript SPiPv2.1_main.r --input {self.get_alg_input_name()} --output {self.get_alg_output_name()}",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            cwd="/usr/src/app/SPiP/",
        )
        """
        process = subprocess.Popen(
            [
                "Rscript",
                "SPiPv2.1_main.r",
                "--input",
                self.get_alg_input_name(),
                "--output",
                self.get_alg_output_name(),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd="/usr/src/app/SPiP/",
        )
        """
        process.wait()

        return process.returncode

    def prepare_input(self, input_file_path):
        with open(input_file_path) as input_file, open(self.get_alg_input_name(), mode="w") as alg_input_file:
            source = csv.DictReader(input_file, delimiter="\t")
            dest = csv.DictWriter(
                alg_input_file,
                delimiter="\t",
                fieldnames=["gene", "varID"],
            )

            dest.writeheader()
            for row in source:
                try:
                    varId = row["HGVS"].split(" ")[0]
                    dest.writerow({"gene": "aaa", "varID": varId})
                except KeyError:
                    dest.writerow({"gene": "aaa", "varID": "."})

    def prepare_output(self, output_file_path):
        with open(output_file_path, mode="w") as output_file, open(self.get_alg_output_name()) as alg_output_file:
            source = csv.DictReader(alg_output_file, delimiter="\t")
            dest = csv.DictWriter(
                output_file,
                delimiter="\t",
                fieldnames=[self.name],
            )

            dest.writeheader()
            for row in source:
                result = row["SPiPscore"]
                dest.writerow({self.name: result})


if __name__ == "__main__":
    SPIP().main()
