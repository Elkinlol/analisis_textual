import json
from pathlib import Path

from similarity.embeddings import (
    angulo_grados, distancia_euclidiana, norma, producto_punto, similitud_coseno_denso,
)

BASE = Path(__file__).resolve().parent.parent
PAR = (0, 9)    # artículos 1 y 10

with open(BASE / "data" / "corpus.json", encoding="utf-8") as f:
    archivos_corpus = [d["archivo"] for d in json.load(f)]

for clave in ("minilm", "specter"):
    with open(BASE / "data" / f"embeddings_{clave}.json", encoding="utf-8") as f:
        datos = json.load(f)
    v = datos["vectores"]
    a, b = v[PAR[0]], v[PAR[1]]
    c = similitud_coseno_denso(a, b)

    print(f"\n=== {clave} ===")
    print("Vectores:", len(v), "| dimensión:", len(v[0]))
    print("Mismo orden que el corpus:", datos["archivos"] == archivos_corpus)
    print("Producto punto:", round(producto_punto(a, b), 4))
    print("Normas:", round(norma(a), 4), round(norma(b), 4))
    print("Coseno:", round(c, 4), "| ángulo:", round(angulo_grados(c), 1), "grados")
    print("Distancia euclidiana:", round(distancia_euclidiana(a, b), 4))