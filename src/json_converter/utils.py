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

    def override_json(self, json_name, meta): #nuovo metodo
        saved_json = self.read_json(json_name) or {}

        saved_fields = saved_json.setdefault("fields", {})
        new_fields = meta.get("fields", {})

        saved_keys = set(saved_fields.keys())
        new_keys = set(new_fields.keys())

        for field_name in new_keys - saved_keys:
            merged_def = new_fields[field_name].copy()
            merged_def["optional"] = "true"
            saved_fields[field_name] = merged_def

        for field_name in saved_keys - new_keys:
            if "optional" not in saved_fields[field_name]:
                saved_fields[field_name]["optional"] = "true"

        saved_children = saved_json.setdefault("children", [])
        new_children = meta.get("children", [])

        for child in new_children:
            if child not in saved_children:
                saved_children.append(child)

        self.save_json(saved_json, json_name)


