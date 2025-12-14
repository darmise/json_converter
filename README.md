# json_converter

Tool Python per convertire JSON annidati in tabelle CSV “relazionali” e ricostruire JSON a partire da CSV. Utile per normalizzare dati JSON complessi, trasformazioni, esportazioni/importazioni, e pipeline dati.


**Funzionalità principali**

- Conversione JSON → tabelle CSV; 

- Conversione CSV → JSON, con ricostruzione della struttura originaria (relazioni padre-figli);

- Supporto a JSON singolo o lista di oggetti JSON.


**Esempio di utilizzo: JSON → CSV**
```python
from src.converter_JSON import Converter_JSON
from src.utils import Utils 

data = Utils().read_json(input_name)
json_tables = Converter_JSON(output_folder)
json_tables.processing(data, "root")
print(f"[✓] Output salvato in: {output_folder}")
```
Nella cartella output_folder/ vengono salvati i .csv che rappresentano le tabelle generate dal JSON annidato.
Nella cartella tests vengono proposti gli esempi: Test1, Test2 e Test3.

**Esempio di utilizzo: CSV → JSON**
```python
from src.utils import Utils
from src.converter_CSV import Converter_CSV

convert = Converter_CSV()
result_json = convert.processing(input_folder)
Utils().save_json(result_json, output)
print(f"[✓] Output salvato in: {output}")
```
Nella cartella tests vengono proposti gli esempi: Test4, Test5 e Test6.
