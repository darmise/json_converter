
import os

from src.converter_JSON import Converter_JSON
from src.utils import Utils 


def main(input_name, output_folder):
    data = Utils().read_json(input_name)
    json_tables = Converter_JSON(output_folder)
    json_tables.processing(data, "root")
    print(f"[✓] Output salvato in: {output_folder}")

if __name__ == "__main__":
    input = os.path.join(os.path.dirname(__file__), "input.json")
    output = os.path.join(os.path.dirname(__file__), "output")
    main(input, output)