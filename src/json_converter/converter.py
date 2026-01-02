from converter_JSON import Converter_JSON
from converter_CSV import Converter_CSV
from validator import Validator
from utils import Utils


class Converter:
    def __init__(self):
        pass

    def processing_json(self, input, output_folder, schema=None):
        data = Utils().read_json(input)
        json_tables = Converter_JSON(output_folder)
        json_tables.processing(data, "root")
        print(f"[✓] Output salvato in: {output_folder}")
        if schema :
            print("Validazione...")
            json_schema = Utils().read_json(schema)
            validator = Validator()
            validator.validation(data, json_schema)        

    def processing_csv(self, output, input_folder, schema = None):
        convert = Converter_CSV()
        output_json = convert.processing(input_folder)
        Utils().save_json(output_json, output)
        print(f"[✓] Output {output} salvato con successo")
        if schema:
            print("Validazione..")
            json_schema = Utils().read_json(schema)
            validator = Validator()
            validator.validation(output_json, json_schema)

    def processing(self, input, folder, output, schema = None):
        self.processing_json(input, folder, schema)
        self.processing_csv(output, folder, schema)

