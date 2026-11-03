import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

BASE = Path(__file__).resolve().parent.parent.parent

MODELOS = {
    "minilm": "sentence-transformers/all-MiniLM-L6-v2",
    "specter": "sentence-transformers/allenai-specter",
}


def main():
    with open(BASE / "data" / "corpus.json", encoding="utf-8") as f:
        corpus = json.load(f)

    # Los modelos reciben el abstract original, no los tokens:
    # necesitan el texto natural (con stopwords y orden) para captar el significado.
    textos = [d["abstract"] for d in corpus]

    for clave, nombre in MODELOS.items():
        print("Cargando", nombre)
        modelo = SentenceTransformer(nombre)
        vectores = modelo.encode(textos)          # matriz de 20 x dimensión

        salida = BASE / "data" / f"embeddings_{clave}.json"
        with open(salida, "w", encoding="utf-8") as f:
            json.dump({
                "modelo": nombre,
                "archivos": [d["archivo"] for d in corpus],
                "vectores": [v.tolist() for v in vectores],
            }, f)
        print("Guardado:", salida, "| dimensión:", len(vectores[0]))

