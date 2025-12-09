import os
import json
import pandas as pd


class Tables_to_JSON:
    def __init__(self):
        pass

    def processing(self, folder):
    
        tables, csv_files = self.load_csv_files(folder)

        if "root.csv" not in csv_files:
            raise RuntimeError("File root.csv non trovato nella cartella")

        root_df = tables["root"]
        result_list = []

        pk_to_node = {}

        for _, root_row in root_df.iterrows():
            root_json = self.clean_record(root_row.to_dict(), "pk_id")
            pk_to_node[root_row["pk_id"]] = root_json
            result_list.append(root_json)

        for f in csv_files:
            if f == "root.csv":
                continue

            table_name = os.path.splitext(f)[0]
            df = tables[table_name]

            if "id_fk" not in df.columns:
                continue  

            grouped = df.groupby("id_fk")
            for fk_value, child_group in grouped:
                parent_node = pk_to_node.get(fk_value)
                if parent_node is None:
                    print(f"[WARN] Nessun padre trovato per fk_id={fk_value} in tabella {table_name}")
                    continue

                self.insert_children(parent_node, child_group, table_name, pk_to_node)

        return result_list[0] if len(result_list) == 1 else result_list

    def load_csv_files(self, folder):
        csv_files = [f for f in os.listdir(folder) if f.endswith(".csv")]
        csv_files.sort()
        tables = {}

        for f in csv_files:
            name = os.path.splitext(f)[0]
            df = pd.read_csv(os.path.join(folder, f), dtype=str).fillna('')
            tables[name] = df

        return tables, csv_files

    def clean_record(self, record, pk_field):
        return {k: v for k, v in record.items() if k != pk_field and k != "id_fk"}

    def insert_children(self, parent_node, child_group, table_name, pk_to_node):
        label = table_name.split("_")[-1]

        if len(child_group) == 1:
            row = child_group.iloc[0]
            child_payload = self.clean_record(row, "pk_id" if "pk_id" in row else "id")
            parent_node[label] = child_payload
            pk_to_node[row["pk_id"]] = child_payload
        else:
            children = []
            for _, row in child_group.iterrows():
                child_payload = self.clean_record(row, "pk_id" if "pk_id" in row else "id")
                children.append(child_payload)
                pk_to_node[row["pk_id"]] = child_payload
            parent_node[label] = children

