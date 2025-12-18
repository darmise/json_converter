from jsonschema import validate, exceptions


class Validator:
    def __init__(self):
        pass
        
    def validation(self, file, schema):
        try:
            if isinstance(file, list):
                for js in file:
                    validate(instance=js, schema=schema)
            else: 
                validate(instance=file, schema=schema)
        except exceptions.ValidationError as e: 
            print(f"Data failed validation: {e}")
        else:    
            print("Validazione avvenuta con successo")
