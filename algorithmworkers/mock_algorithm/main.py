from ..common import Algorithm
import csv


class Mock_Algorithm(Algorithm):
    def __init__(self):
        super().__init__("mock_algorithm")

    def run(self):
        return 0

    def prepare_input(self, input_file_path):
        self.input_file_path = input_file_path

    def prepare_output(self, output_file_path):
        with open(output_file_path, mode="w") as output_file, open(
            self.input_file_path
        ) as input_file:
            source = csv.DictReader(input_file, delimiter="\t")
            dest = csv.DictWriter(
                output_file,
                delimiter="\t",
                fieldnames=[self.name],
            )

            dest.writeheader()
            for row in source:
                dest.writerow({self.name: 123})


if __name__ == "__main__":
    Mock_Algorithm().main()
