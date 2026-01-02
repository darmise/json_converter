import os

from .converter import Converter


if __name__ == "__main__":
    input = os.path.join(os.path.dirname(__file__), "input.json")
    output = os.path.join(os.path.dirname(__file__), "output")
    conv = Converter()
    conv.processing_json(input, output)