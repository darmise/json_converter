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

    def override_json(self, json_name, meta):
        saved_json = self.read_json(json_name)

        saved_fields = saved_json.setdefault("fields", {})
        new_fields = meta.get("fields", {})

        STRUCTURED_TYPES = {"object", "array"}
        PRIMITIVE_TYPES = {"string", "integer", "number", "boolean"}

        saved_keys = set(saved_fields.keys())
        new_keys = set(new_fields.keys())

        for field_name in saved_keys & new_keys:
            old_def = saved_fields[field_name]
            new_def = new_fields[field_name]

            old_type = old_def.get("type")
            new_type = new_def.get("type")

            merged_def = new_def.copy()

            if old_type in STRUCTURED_TYPES or new_type in STRUCTURED_TYPES:
                if "object" in (old_type, new_type):
                    merged_def["type"] = "object"
                else:
                    merged_def["type"] = "array"

            else:
                if (
                    old_type in PRIMITIVE_TYPES
                    and new_type in PRIMITIVE_TYPES
                    and old_type != new_type
                ):
                    merged_def["type"] = old_type
                    merged_def["optional"] = "true"
                else:
                    merged_def["type"] = new_type or old_type

            if old_type != new_type:
                merged_def["optional"] = "true"

            if merged_def["type"] in STRUCTURED_TYPES:
                merged_def["child_table"] = (
                    old_def.get("child_table") or new_def.get("child_table")
                )
            else:
                merged_def.pop("child_table", None)

            saved_fields[field_name] = merged_def

        for field_name in new_keys - saved_keys:
            saved_fields[field_name] = new_fields[field_name].copy()

        for field_name in saved_keys - new_keys:
            if "optional" not in saved_fields[field_name]:
                saved_fields[field_name]["optional"] = "true"

        saved_children = saved_json.setdefault("children", [])
        new_children = meta.get("children", [])

        for child in new_children:
            if child not in saved_children:
                saved_children.append(child)

        self.save_json(saved_json, json_name)



