import os
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)

from src.utils import Utils
from src.tables_to_json import Tables_to_JSON

def main(input_folder, output):
    convert = Tables_to_JSON()
    result_json = convert.processing(input_folder)
    Utils().save_json(result_json, output)
    print(f"[✓] Output salvato in: {output}")

if __name__ == "__main__":
    input = os.path.join(os.path.dirname(__file__), "input")
    output = os.path.join(os.path.dirname(__file__), "out.json")
    main(input, output)