# json_converter

Tool Python per convertire JSON annidati in tabelle CSV “relazionali” e ricostruire JSON a partire da CSV. Utile per normalizzare dati JSON complessi, trasformazioni, esportazioni/importazioni, e pipeline dati.


**Funzionalità principali**

- Conversione JSON → tabelle CSV; 

- Conversione CSV → JSON, con ricostruzione della struttura originaria (relazioni padre-figli);

- Supporto a JSON singolo o lista di oggetti JSON;

- Validazione dei file JSON (input-output).


**Esempio di utilizzo: JSON → CSV**
```python
from .converter import Converter

input = os.path.join(os.path.dirname(__file__), "input.json")
output = os.path.join(os.path.dirname(__file__), "output")
conv = Converter()
conv.processing_json(input, output)
```
Nella cartella output_folder/ vengono salvati i .csv che rappresentano le tabelle generate dal JSON annidato.
Nella cartella tests vengono proposti gli esempi: Test1 e Test2.

**Esempio di utilizzo: CSV → JSON**
```python
from .converter import Converter

input = os.path.join(os.path.dirname(__file__), "input")
output = os.path.join(os.path.dirname(__file__), "output.json")
conv = Converter()
conv.processing_csv(output, input)
```
Nella cartella tests vengono proposti gli esempi: Test4 e Test5.
