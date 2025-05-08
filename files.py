# filepath: generate_file_list.py

import os
import csv

def generate_file_list(root_dir: str, output_file: str = "project_file_list.csv"):
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Relative Path", "Size (bytes)"])

        for dirpath, _, filenames in os.walk(root_dir):
            for file in filenames:
                full_path = os.path.join(dirpath, file)
                rel_path = os.path.relpath(full_path, root_dir)
                size = os.path.getsize(full_path)
                writer.writerow([rel_path, size])

if __name__ == "__main__":
    generate_file_list(".")  # Runs on current directory
