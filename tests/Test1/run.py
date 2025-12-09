
import os
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)


from src.utils import Utils
from src.json_to_tables import JSON_to_tables

def main(input_name, output_folder):
    data = Utils().read_json(input_name)
    json_tables = JSON_to_tables(output_folder)
    json_tables.processing(data, "root")
    print(f"[✓] Output salvato in: {output_folder}")

if __name__ == "__main__":
    input = os.path.join(os.path.dirname(__file__), "input.json")
    output = os.path.join(os.path.dirname(__file__), "out")
    main(input, output)