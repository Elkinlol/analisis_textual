import json
from math import acos, degrees, sqrt


def cargar_vectores(ruta):
    """Lee los embeddings precalculados (lista de vectores, uno por artículo)."""
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)["vectores"]


def producto_punto(a, b):
    return sum(x * y for x, y in zip(a, b))


def norma(v):
    return sqrt(sum(x * x for x in v))


def similitud_coseno_denso(a, b):
    na, nb = norma(a), norma(b)
    if na == 0 or nb == 0:
        return 0.0
    return producto_punto(a, b) / (na * nb)


def distancia_euclidiana(a, b):
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def similitud_euclidiana(a, b):
    """Convierte la distancia en similitud en (0, 1]: 1 / (1 + d)."""
    return 1 / (1 + distancia_euclidiana(a, b))


def angulo_grados(coseno):
    return degrees(acos(max(-1.0, min(1.0, coseno))))


if __name__ == "__main__":
    a, b = [1, 0], [1, 1]
    c = similitud_coseno_denso(a, b)
    print("producto punto:", producto_punto(a, b))
    print("normas:", round(norma(a), 4), round(norma(b), 4))
    print("coseno:", round(c, 4), "| ángulo:", round(angulo_grados(c), 1))