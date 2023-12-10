def make_long_file(input_path, output_path, desired_lines):
    with open(input_path, "r") as f:
        lines = f.readlines()

    header = lines[0]
    lines = lines[1:]  # remove header
    num_lines = len(lines)

    iterations = desired_lines // num_lines

    with open(output_path, "w") as f:
        f.write(header)
        for i in range(iterations):
            f.writelines(lines)


if __name__ == '__main__':
    input_path = "brca.csv"
    output_path = "brca_4k.csv"
    make_long_file(input_path, output_path, 4000)
