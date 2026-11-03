import json
from pathlib import Path

from preprocessing.text_cleaner import preprocesar
from similarity.embeddings import cargar_vectores, similitud_euclidiana
from similarity.jaccard import jaccard
from similarity.levenshtein import similitud_caracteres, similitud_palabras
from similarity.needlenman import similitud_needleman_wunsch
from similarity.coseno import crear_similitud_tfidf,calcular_similitud_tfidf
from similarity.vectores import similitud_coseno

BASE = Path(__file__).resolve().parent.parent
MODELOS_EMBEDDINGS = (("minilm", "MiniLM"), ("specter", "SPECTER"))


def cargar_corpus():
    """Lee data/corpus.json (lista de diccionarios con archivo, titulo, autores y abstract)."""
    with open(BASE / "data" / "corpus.json", encoding="utf-8") as f:
        return json.load(f)


def construir_algoritmos(corpus):
    tokens = [preprocesar(d.get("abstract") or "") for d in corpus]

    idf = crear_similitud_tfidf(tokens)

    algoritmos = {
        "Jaccard": (tokens, jaccard, None),
        "Levenshtein (palabras)": (tokens, similitud_palabras, None),
        "Levenshtein (caracteres)": (tokens, similitud_caracteres, None),
        "TF-IDF + coseno": (tokens, calcular_similitud_tfidf, idf),
        "Needleman-Wunsch": (tokens, similitud_needleman_wunsch, None),
    }

    for clave, etiqueta in MODELOS_EMBEDDINGS:
        ruta = BASE / "data" / f"embeddings_{clave}.json"

        if ruta.exists():
            vectores = cargar_vectores(ruta)

            algoritmos[f"Embeddings {etiqueta} (coseno)"] = (
                vectores, similitud_coseno, None
            )

            algoritmos[f"Embeddings {etiqueta} (euclidiana)"] = (
                vectores, similitud_euclidiana, None
            )

    return algoritmos