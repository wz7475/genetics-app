import csv
import random
import sys


def run_alg(input_csv_file: str, output_file: str) -> None:
    if not output_file.endswith(".csv"):
        output_file += ".csv"
    with open(input_csv_file, 'r') as csv_input:
        with open(output_file, 'w', newline='') as csv_output:
            reader = csv.reader(csv_input)
            writer = csv.writer(csv_output)

            # Write the headers to the output file, including the new 'spip' column
            headers = next(reader)
            headers.append('spip')
            writer.writerow(headers)

            # annotation is random number
            for row in reader:
                row.append(str(random.randint(100000000, 999999999)))
                writer.writerow(row)

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    run_alg(input_file, output_file)
