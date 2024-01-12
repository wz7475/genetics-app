def convert_rename_annotation_column(filepath):
    with open(filepath, "r") as read_file:
        file_lines = read_file.readlines()
        file_lines[0] = file_lines[0].replace("Pangolin", "pangolin")
        with open(filepath, "w") as write_file:
            write_file.writelines(file_lines)
