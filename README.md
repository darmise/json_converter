# json_converter

Tool Python per convertire JSON annidati in tabelle CSV “relazionali” e ricostruire JSON a partire da CSV. Utile per normalizzare dati JSON complessi, trasformazioni, esportazioni/importazioni, e pipeline dati.


**Funzionalità principali**

- Conversione JSON → tabelle CSV; 

- Conversione CSV → JSON, con ricostruzione della struttura originaria (relazioni padre-figli);

- Supporto a JSON singolo o lista di oggetti JSON.


**Esempio di utilizzo: JSON → CSV**
```python
from src.utils import Utils
from src.json_to_tables import JSON_to_tables

data = Utils().read_json(input_filename)
json_tables = JSON_to_tables(output_folder)
json_tables.processing(data, "root")
print(f"[✓] Output salvato in: {output_folder}")
```
Nella cartella output_folder/ vengono salvati i diversi .csv che rappresentano le tabelle generate dal JSON annidato.
Nella cartella tests vengono proposti gli esempi:Test1 e Test2.

**Esempio di utilizzo: CSV → JSON**
```python
from src.utils import Utils
from src.tables_to_json import Tables_to_JSON

convert = Tables_to_JSON()
result_json = convert.processing(input_folder)
Utils().save_json(result_json, output_filename)
print(f"[✓] Output salvato in: {output_filename}")
```
Nella cartella tests vengono proposti gli esempi: Test3 e Test4.
