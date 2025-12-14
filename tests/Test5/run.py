import os


from src.utils import Utils
from src.converter_CSV import Converter_CSV

def main(input_folder, output):
    convert = Converter_CSV()
    result_json = convert.processing(input_folder)
    Utils().save_json(result_json, output)
    print(f"[✓] Output salvato in: {output}")

if __name__ == "__main__":
    input = os.path.join(os.path.dirname(__file__), "input")
    output = os.path.join(os.path.dirname(__file__), "output.json")
    main(input, output)