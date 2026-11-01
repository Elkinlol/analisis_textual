import random

import pytest

from similarity.levenshtein import (
    _normalizar,
    construir_matriz,
    levenshtein,
    similitud_caracteres,
    similitud_palabras,
)


#Ejemplos

@pytest.mark.parametrize("a, b, esperado", [
    ("casa", "cosa", 1),     # una sustitución
    ("sol", "sal", 1),
    ("pan", "pana", 1),      # una inserción
    ("", "abc", 3),          # tres inserciones
    ("abc", "", 3),          # tres borrados
    ("sol", "luz", 3),
])
def test_distancias_a_mano(a, b, esperado):
    assert levenshtein(a, b) == esperado


def test_matriz_de_pan_a_pana_coincide_con_la_del_documento():
    assert construir_matriz("pan", "pana") == [
        [0, 1, 2, 3, 4],
        [1, 0, 1, 2, 3],
        [2, 1, 0, 1, 2],
        [3, 2, 1, 0, 1],
    ]


def test_funciona_con_listas_de_tokens():
    a = ["ai", "improves", "education"]
    b = ["ai", "supports", "education"]
    assert levenshtein(a, b) == 1


#Propiedades del concepto

def _aleatoria(rng):
    return [rng.choice("abc") for _ in range(rng.randint(0, 7))]


def test_version_de_dos_filas_igual_a_matriz_completa():
    rng = random.Random(1)
    for _ in range(1000):
        a, b = _aleatoria(rng), _aleatoria(rng)
        assert levenshtein(a, b) == construir_matriz(a, b)[-1][-1]


def test_es_una_metrica():
    rng = random.Random(2)
    for _ in range(1000):
        a, b, c = _aleatoria(rng), _aleatoria(rng), _aleatoria(rng)
        assert (levenshtein(a, b) == 0) == (a == b)               # identidad
        assert levenshtein(a, b) == levenshtein(b, a)             # simetría
        assert levenshtein(a, c) <= levenshtein(a, b) + levenshtein(b, c)   # triangular


def test_cotas():
    rng = random.Random(3)
    for _ in range(1000):
        a, b = _aleatoria(rng), _aleatoria(rng)
        d = levenshtein(a, b)
        assert abs(len(a) - len(b)) <= d <= max(len(a), len(b))


# Normalizar una similitud

def test_similitud_en_rango_y_extremos():
    assert similitud_palabras(["a", "b"], ["a", "b"]) == 1.0
    assert similitud_palabras(["a"], ["b"]) == 0.0
    assert similitud_palabras([], []) == 1.0
    assert similitud_caracteres([], []) == 1.0


def test_similitud_caracteres_une_los_tokens_con_espacios():
    # "ab" vs "ac": distancia 1, largo máximo 2 -> 1 - 1/2
    assert similitud_caracteres(["ab"], ["ac"]) == pytest.approx(0.5)


def test_caso_de_estudio_articulos_1_y_10_por_palabras():
    # 105 y 136 tokens, 9 coincidencias alineadas -> distancia 136 - 9 = 127
    comunes = [f"c{i}" for i in range(9)]
    a = comunes + [f"a{i}" for i in range(96)]
    b = comunes + [f"b{i}" for i in range(127)]
    assert len(a) == 105 and len(b) == 136
    assert levenshtein(a, b) == 127
    assert round(similitud_palabras(a, b), 4) == 0.0662


def test_normalizacion_del_caso_de_estudio_por_caracteres():
    # distancia 788 entre cadenas de 811 y 1144 caracteres
    assert round(_normalizar(788, 811, 1144), 4) == 0.3112