def construir_matriz(a, b):
    """Matriz completa de programación dinámica.
    Sirve para el caso de estudio (mostrar el llenado paso a paso)."""
    n, m = len(a), len(b)
    matriz = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        matriz[i][0] = i
    for j in range(m + 1):
        matriz[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            costo = 0 if a[i - 1] == b[j - 1] else 1
            matriz[i][j] = min(
                matriz[i - 1][j] + 1,           # borrar
                matriz[i][j - 1] + 1,           # insertar
                matriz[i - 1][j - 1] + costo,   # sustituir / coincidir
            )
    return matriz


def levenshtein(a, b):
    #Distancia de edición usando solo dos filas (memoria O(min(n, m)))
    if len(a) < len(b):
        a, b = b, a                        # b siempre es la secuencia corta
    previa = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        actual = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            costo = 0 if a[i - 1] == b[j - 1] else 1
            actual[j] = min(
                previa[j] + 1,
                actual[j - 1] + 1,
                previa[j - 1] + costo,
            )
        previa = actual
    return previa[-1]


def _normalizar(distancia, largo_a, largo_b):
    mayor = max(largo_a, largo_b)
    return 1.0 if mayor == 0 else 1 - distancia / mayor


def similitud_palabras(tokens_a, tokens_b):
    #Levenshtein con cada TOKEN como símbolo.
    return _normalizar(levenshtein(tokens_a, tokens_b), len(tokens_a), len(tokens_b))


def similitud_caracteres(tokens_a, tokens_b):
    #Levenshtein con cada LETRA como símbolo.
    a, b = " ".join(tokens_a), " ".join(tokens_b)
    return _normalizar(levenshtein(a, b), len(a), len(b))


if __name__ == "__main__":
    for fila in construir_matriz("pan", "pana"):
        print(fila)
    print(levenshtein("casa", "cosa"), levenshtein("sol", "sal"), levenshtein("", "abc"))
    print(similitud_palabras(["ai", "improves", "education"],
                             ["ai", "supports", "education"]))