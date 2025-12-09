import os
import pandas as pd
import uuid


class JSON_to_tables:

    def __init__(self, output_folder):
        self.output_folder = f"{output_folder}_{self.get_new_id()}"
        os.makedirs(self.output_folder, exist_ok=True)
    
    def processing(self, data, table_name, parent_pk=None):
        rows = []
        children = []

        if isinstance(data, dict):
            data = [data]

        for item in data:
            row = {}
           
            row_pk = self.get_new_id()
            row["pk_id"] = row_pk

            if parent_pk is not None:
                row["id_fk"] = parent_pk

            for key, value in item.items():

                if self.is_nested(value): 
                    child_table = f"{table_name}_{key}"

                    if isinstance(value, dict):
                        nested_items = [value]
                    else:
                        nested_items = [
                            v if isinstance(v, dict) else {key: v}
                            for v in value
                        ]

                    children.append((child_table, nested_items, row_pk))

                else:
                    row[key] = value

            rows.append(row)
        self.save_tables(table_name, rows)

        for (child_name, child_data, parent_pk_value) in children:
            self.processing(child_data, child_name, parent_pk_value)

    def save_tables(self, table_name, rows):
        table_csv = os.path.join(self.output_folder, f"{table_name}.csv")

        if os.path.exists(table_csv):
            existing_df = pd.read_csv(table_csv, dtype=str).fillna('')
            new_df = pd.DataFrame(rows)
            df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            df = pd.DataFrame(rows)

        df.to_csv(table_csv, index=False)
        print(f"[✓] Creato/Aggiornato: {table_name}.csv")
    
    def get_new_id(self):
        return str(uuid.uuid4())
    
    def is_nested(self, value):
        return isinstance(value, (dict, list))
