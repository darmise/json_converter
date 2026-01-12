import os
import uuid
import pandas as pd
from .utils import Utils


class Converter_JSON:
    def __init__(self, out_folder):
        self.output_folder = out_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def get_new_id(self):
        return str(uuid.uuid4())
    
    def infer_type(self, value):
        if isinstance(value, dict):
            return "object"

        elif isinstance(value, list):
            return "array"

        elif isinstance(value, bool):
            return "boolean"

        elif isinstance(value, int):
            return "integer"
        
        elif isinstance(value, float):
            return "number"

        elif isinstance(value, str):
            s = value.strip().lower()
            if s in ("true", "false"):
                return "boolean"
            try:
                int(s)
                return "integer"
            except:
                pass
            try:
                float(s)
                return "number"
            except:
                pass
            return "string"
        return "string"
    
    def is_nested(self, value):
        return isinstance(value, (dict, list))

    def processing(self, data, table_name, parent_table=None, parent_pk=None):
        rows = []
        children = []

        items = data if isinstance(data, list) else [data]
        
        metadata = {"fields": {}, "children": []}

        for item in items:  
            row = {}
            row_pk = self.get_new_id()
            row["pk_id"] = row_pk
            if parent_pk is not None:
                row["id_fk"] = parent_pk

            if not isinstance(item, dict):
                row["value"] = item
                metadata["fields"]["value"] = {"type": self.infer_type(item)}
                rows.append(row)
                continue
            for key, value in item.items():
                if self.is_nested(value):
                    child_table = f"{table_name}_{key}"
                    if isinstance(value, dict):
                        nested_items = [value]
                    else:
                        nested_items = [v if isinstance(v, dict) else {key: v} for v in value]
                    children.append((child_table, nested_items, row_pk))

                    metadata["fields"][key] = {
                    "type": self.infer_type(value),
                    "child_table": child_table
                    }

                    if child_table not in metadata["children"]:
                        metadata["children"].append(child_table)
                else:
                    row[key] = "NLL" if value is None else value 
                    metadata["fields"][key] = {
                        "type": self.infer_type(value)
                    }
            
            rows.append(row)
        
        table_csv = os.path.join(self.output_folder, f"{table_name}.csv")
        df_new = pd.DataFrame(rows).fillna('')

        if os.path.exists(table_csv):
            existing_df = pd.read_csv(table_csv, dtype=str).fillna('')
            df = pd.concat([existing_df, df_new], ignore_index=True)
        else:
            df = df_new

        df.to_csv(table_csv, index=False)
        print(f"[✓] CSV generato: {table_name}.csv")

        metadata_file = os.path.join(self.output_folder, f"{table_name}_metadata.json")
        
        if os.path.exists(metadata_file): 
            Utils().override_json(metadata_file, metadata)
        else: 
            Utils().save_json(metadata, metadata_file)
        print(f"[✓] JSON metadati generato: {table_name}_metadata.json")
        
        for child_name, child_data, parent_pk_value in children:
            self.processing(child_data, child_name, table_name, parent_pk_value)

        return rows
            
  