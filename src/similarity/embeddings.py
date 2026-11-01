import json

from similarity.vectores import distancia_euclidiana, normalizar


def cargar_vectores(ruta):
    """Lee los embeddings precalculados: una lista de vectores, uno por artículo."""
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)["vectores"]


def similitud_euclidiana(u, v):
    """Similitud = 1 / (1 + d), con d la distancia euclidiana entre los vectores normalizados.

    Se normaliza antes porque la distancia sin normalizar depende del tamaño de los vectores
    (los de SPECTER tienen norma ~22 y los de MiniLM norma 1) y no sería comparable entre
    modelos. Con vectores unitarios d² = 2 − 2·cos θ, así que la similitud es una función
    creciente del coseno.
    """
    return 1 / (1 + distancia_euclidiana(normalizar(u), normalizar(v)))