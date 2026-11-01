import random

import pytest

from similarity.jaccard import jaccard


# ---------- Ejemplos calculados a mano ----------

def test_ejemplo_a_mano():
    # A ∩ B = {ai, education} (2), A ∪ B tiene 5 elementos -> 2/5
    a = ["ai", "improves", "education"]
    b = ["ai", "supports", "education", "research"]
    assert jaccard(a, b) == pytest.approx(0.4)


def test_caso_de_estudio_articulos_1_y_10():
    # 84 y 92 tokens distintos con 13 en común: |A ∪ B| = 84 + 92 - 13 = 163
    comunes = [f"c{i}" for i in range(13)]
    a = comunes + [f"a{i}" for i in range(71)]
    b = comunes + [f"b{i}" for i in range(79)]
    assert len(set(a)) == 84 and len(set(b)) == 92
    assert jaccard(a, b) == pytest.approx(13 / 163)
    assert round(jaccard(a, b), 4) == 0.0798


# ---------- Casos borde ----------

def test_identicos_dan_uno():
    assert jaccard(["a", "b"], ["b", "a"]) == 1.0


def test_disjuntos_dan_cero():
    assert jaccard(["a"], ["b"]) == 0.0


def test_dos_vacios_dan_uno_por_convencion():
    assert jaccard([], []) == 1.0


def test_uno_vacio_da_cero():
    assert jaccard(["a"], []) == 0.0


#Propiedades de la definicion

def test_ignora_repeticiones_y_orden():
    assert jaccard(["ai", "ai", "education"], ["education", "ai"]) == 1.0


def _aleatorio(rng):
    palabras = list("abcdefghij")
    return [rng.choice(palabras) for _ in range(rng.randint(0, 8))]


def test_simetria_y_rango():
    rng = random.Random(1)
    for _ in range(1000):
        a, b = _aleatorio(rng), _aleatorio(rng)
        j = jaccard(a, b)
        assert j == jaccard(b, a)
        assert 0.0 <= j <= 1.0


def test_distancia_jaccard_cumple_desigualdad_triangular():
    # d = 1 - J es una métrica: d(a, c) <= d(a, b) + d(b, c)
    rng = random.Random(2)
    for _ in range(1000):
        a, b, c = _aleatorio(rng), _aleatorio(rng), _aleatorio(rng)
        d = lambda x, y: 1 - jaccard(x, y)
        assert d(a, c) <= d(a, b) + d(b, c) + 1e-12