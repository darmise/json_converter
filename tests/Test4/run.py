import os

from .converter import Converter


if __name__ == "__main__":
    input = os.path.join(os.path.dirname(__file__), "input")
    output = os.path.join(os.path.dirname(__file__), "output.json")
    conv = Converter()
    conv.processing_csv(output, input)
