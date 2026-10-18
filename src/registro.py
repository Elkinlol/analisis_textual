import json
from pathlib import Path

from preprocessing.text_cleaner import preprocesar
from similarity.jaccard import jaccard
from similarity.levenshtein import similitud_palabras, similitud_caracteres
from similarity.coseno import crear_similitud_tfidf
from similarity.needlenman import similitud_needleman_wunsch
from similarity.embeddings import (
    cargar_vectores, similitud_coseno_denso, similitud_euclidiana,
)

BASE = Path(__file__).resolve().parent.parent


def cargar_corpus():
    with open(BASE / "data" / "corpus.json", encoding="utf-8") as f:
        return json.load(f)


def construir_algoritmos(corpus):
    """Devuelve {nombre: (representación de cada artículo, función de similitud)}.
    Los de embeddings solo aparecen si existen sus archivos JSON."""
    tokens = [preprocesar(d.get("abstract") or "") for d in corpus]

    algoritmos = {
        "Jaccard": (tokens, jaccard),
        "Levenshtein (palabras)": (tokens, similitud_palabras),
        "Levenshtein (caracteres)": (tokens, similitud_caracteres),
        "TF-IDF + coseno": (tokens, crear_similitud_tfidf(tokens)),
        "Needleman-Wunsch": (tokens, similitud_needleman_wunsch),
    }

    for clave, etiqueta in (("minilm", "MiniLM"), ("specter", "SPECTER")):
        ruta = BASE / "data" / f"embeddings_{clave}.json"
        if ruta.exists():
            vectores = cargar_vectores(ruta)
            algoritmos[f"Embeddings {etiqueta} (coseno)"] = (vectores, similitud_coseno_denso)
            algoritmos[f"Embeddings {etiqueta} (euclidiana)"] = (vectores, similitud_euclidiana)

    return algoritmos