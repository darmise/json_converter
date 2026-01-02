import json

class Utils:
    def __init__(self):
        pass
    
    def read_json(self, fileName):
        with open(fileName, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
            
    def save_json(self, json_data, output):
        with open(output, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)