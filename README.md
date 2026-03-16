# json_converter

Tool Python che consente la conversione bidirezionale di file JSON annidati in tabelle CSV “relazionali”. Utile per normalizzare dati JSON complessi, trasformazioni, esportazioni/importazioni, e pipeline dati.

**Funzionalità principali**

- Conversione JSON → tabelle CSV; 

- Conversione CSV → JSON, con ricostruzione della struttura originaria (basata sulle relazioni padre-figlo);

- Supporto a JSON singolo o lista di oggetti JSON;

- Validazione dei file JSON (input-output) passando in input lo schema JSON corrispondente.


**Esempio di utilizzo: JSON → CSV**
```python
from json_converter.converter import Converter


input = os.path.join(os.path.dirname(__file__), "input.json") #filename JSON
output = os.path.join(os.path.dirname(__file__), "output")    #foldername output
conv = Converter()
conv.processing_json(input, output)
```
Nella cartella output/ vengono salvati i .csv che rappresentano le tabelle generate dal JSON annidato.

**Esempio di utilizzo: CSV → JSON**
```python
from json_converter.converter import Converter

input = os.path.join(os.path.dirname(__file__), "input") #foldername input
output = os.path.join(os.path.dirname(__file__), "output.json") #filename JSON
conv = Converter()
conv.processing_csv(output, input)
```
Il file JSON ricostruito, a partire dai file .CSV presenti nella cartella input, viene salvato nella cartella corrente.
