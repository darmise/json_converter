import os
import json
import pandas as pd


class Converter_CSV:
    def __init__(self):
        pass

    def load_csv_files(self, folder):
        csv_files = [f for f in os.listdir(folder) if f.endswith(".csv")]
        csv_files.sort()
        tables = {}
        for f in csv_files:
            name = os.path.splitext(f)[0]
            df = pd.read_csv(os.path.join(folder, f), dtype=str).fillna('')
            tables[name] = df
        return tables
    
    def load_metadata(self, folder):
        meta_files = [f for f in os.listdir(folder) if f.endswith("_metadata.json")]
        metadata = {}
        for f in meta_files:
            name = f.replace("_metadata.json", "")
            with open(os.path.join(folder, f), "r", encoding="utf-8") as m:
                metadata[name] = json.load(m)
        return metadata
        
    def clean_record(self, row, field_types=None):
        record = {}
        for k, v in row.items():
            if k in ("pk_id", "id_fk"):
                continue
            f_type = field_types.get(k, "string") if field_types else "string"
            record[k] = self.convert_value(v, f_type)
        return record
    
    def convert_value(self, value, field_type):
        if value is None or (isinstance(value, str) and value == ''):
            return None

        if field_type == "boolean":
            if isinstance(value, str):
                s = value.strip().lower()
                if s in ("true"):
                    return True
                elif s in ("false"):
                    return False
                else:
                    return True
            return bool(value)

        if field_type == "integer":
            try:
                if isinstance(value, str):
                    s = value.strip().lower()
                    if s in ("true", "false"):
                        return None
                    if '.' in value:
                        return int(float(value))
                return int(value)
            except:
                return None

        if field_type == "number":
            try:
                return float(value)
            except:
                return None

        if field_type == "string":
            return str(value)

        if field_type in ("object", "array"):
            
            if isinstance(value, (dict, list)):
                return value
            if isinstance(value, str):
                try:
                    parsed = json.loads(value)
                    return parsed
                except:
                    return value
            return value

        return value
    
    def get_hierarchy_list(self, metadata):
        hierarchy = []

        def add_node(node_name):
            if node_name in hierarchy:
                return  
            hierarchy.append(node_name)
            for child in metadata.get(node_name, {}).get('children', []):
                add_node(child)

        all_children = set(child for v in metadata.values() for child in v.get('children', []))
        roots = [k for k in metadata.keys() if k not in all_children]

        for root in roots:
            add_node(root)

        return hierarchy
    
    def find_parent_table_and_field(self, child_table_name, metadata):
        for tname, schema in metadata.items():
            for field_name, field_info in schema.get("fields", {}).items():
                if field_info.get("child_table") == child_table_name:
                    return tname, field_name
        return None, None
    
    def build_child_object_from_row(self, row_series, child_meta):
        meta_fields = child_meta.get("fields", {})
        types_map = {k: v.get("type", "string") for k, v in meta_fields.items()}
        row_dict = row_series.to_dict()
        child_obj = self.clean_record(row_dict, types_map)
        
        non_tech_fields = [fn for fn in meta_fields.keys() if fn not in ("pk_id", "id_fk")]
        if not child_meta.get("children") and len(non_tech_fields) == 1:
            only_field = non_tech_fields[0]
            return child_obj.get(only_field)
        return child_obj
    
    def move_key_to_index_inplace(self, d, key, new_index):
        items = list(d.items())

        try:
            old_index = next(i for i, (k, _) in enumerate(items) if k == key)
        except StopIteration:
            raise KeyError(f"Chiave '{key}' non trovata")

        item = items.pop(old_index)
        items.insert(new_index, item)
        d.clear()
        d.update(items)

    def attach_child_row(self, row_series, table_name, tables, metadata, pk_to_node):    
        parent_table, parent_field = self.find_parent_table_and_field(table_name, metadata)
        
        if parent_table is None:
            print(f"[WARN] Nessun padre trovato nei metadati per tabella figlia {table_name}")
            return
        
        parent_meta = metadata.get(parent_table, {})
        
        row = row_series.to_dict()
        parent_pk = row.get("id_fk")
        if parent_pk is None or parent_pk == '':
            print(f"[WARN] Riga in {table_name} priva di id_fk: {row}")
            return

        parent_node = pk_to_node.get(parent_pk)
        
        if parent_node is None:
            print(f"[WARN] Padre con pk {parent_pk} non trovato per riga in {table_name}")
            return

        fields_order = list(parent_meta["fields"].keys())
        index = fields_order.index(parent_field) 
        parent_field_info = parent_meta.get("fields", {}).get(parent_field, {})
        field_type = parent_field_info.get("type", "string")
        child_meta = metadata.get(table_name, {"fields": {}, "children": []})
        child_obj = self.build_child_object_from_row(row_series, child_meta)

        if field_type == "array":
            if parent_field not in parent_node or not isinstance(parent_node[parent_field], list):
                parent_node[parent_field] = []
            parent_node[parent_field].append(child_obj)
            
        elif field_type == "object":
            parent_node[parent_field] = child_obj
        else:
            if isinstance(child_obj, dict):
                non_tech = [k for k in child_obj.keys() if k not in ("pk_id", "id_fk")]
                val = child_obj.get(non_tech[0]) if non_tech else None
                parent_node[parent_field] = val
            else:
                parent_node[parent_field] = child_obj
        
        self.move_key_to_index_inplace(parent_node, parent_field, index)
        
        child_pk = row.get("pk_id")
        if child_pk:
            pk_to_node[child_pk] = child_obj

    def processing(self, folder):
        tables = self.load_csv_files(folder)
        metadata = self.load_metadata(folder)

        if "root" not in tables:
            raise RuntimeError("root.csv non trovato nella cartella")

        root_df = tables["root"]
        result_list = []
        pk_to_node = {}

        root_meta_fields = metadata.get("root", {}).get("fields", {})

        for _, root_row in root_df.iterrows():
            root_node = self.clean_record(
                root_row, {k: v.get("type", "string") for k, v in root_meta_fields.items()}
            )
            pk_to_node[root_row["pk_id"]] = root_node
            result_list.append(root_node)

        other_tables_sorted = self.get_hierarchy_list(metadata)
        other_tables_sorted.remove("root")

        for table_name in other_tables_sorted:
            df = tables.get(table_name)
            if df is None:
                continue
            for _, row_series in df.iterrows():
                self.attach_child_row(row_series, table_name, tables, metadata, pk_to_node)

        return result_list[0] if len(result_list) == 1 else result_list
