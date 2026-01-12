import os

from json_converter.converter import Converter


if __name__ == "__main__":
    input_name = os.path.join(os.path.dirname(__file__), "input.json")
    folder = os.path.join(os.path.dirname(__file__), "folder")
    output_name = os.path.join(os.path.dirname(__file__), "output.json")
    schema = os.path.join(os.path.dirname(__file__), "schema.json")
    conv = Converter()
    conv.processing(input_name, folder, output_name)
