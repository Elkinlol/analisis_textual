import json
from extraction.extractor import (
    procesar_carpeta, aplicar_manual, limpiar_abstract, SALIDA
)

corpus = aplicar_manual(procesar_carpeta())
for d in corpus:
    d["abstract"] = limpiar_abstract(d["abstract"] or "")

SALIDA.parent.mkdir(exist_ok=True)
with open(SALIDA, "w", encoding="utf-8") as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print("Corpus guardado:", len(corpus), "documentos")