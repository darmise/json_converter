import os

from src.converter import Converter


if __name__ == "__main__":
    input = os.path.join(os.path.dirname(__file__), "input.json")
    output = os.path.join(os.path.dirname(__file__), "output")
    schema = os.path.join(os.path.dirname(__file__), "schema.json")
    conv = Converter()
    conv.processing_json(input, output, schema)
