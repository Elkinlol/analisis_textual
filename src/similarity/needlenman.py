def construir_matriz(a, b, coincidencia=1, desajuste=-1, hueco=-1):
    """Matriz de puntajes de Needleman-Wunsch (alineamiento global)."""
    n, m = len(a), len(b)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        D[i][0] = D[i - 1][0] + hueco
    for j in range(1, m + 1):
        D[0][j] = D[0][j - 1] + hueco
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            puntaje = coincidencia if a[i - 1] == b[j - 1] else desajuste
            D[i][j] = max(
                D[i - 1][j - 1] + puntaje,   # diagonal: alinear
                D[i - 1][j] + hueco,         # arriba: hueco en b
                D[i][j - 1] + hueco,         # izquierda: hueco en a
            )
    return D


def alineamiento(a, b, coincidencia=1, desajuste=-1, hueco=-1):
    """Recorre la matriz hacia atrás y devuelve el alineamiento óptimo."""
    D = construir_matriz(a, b, coincidencia, desajuste, hueco)
    i, j = len(a), len(b)
    alin_a, alin_b = [], []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and D[i][j] == D[i - 1][j - 1] + (
                coincidencia if a[i - 1] == b[j - 1] else desajuste):
            alin_a.append(a[i - 1]); alin_b.append(b[j - 1]); i -= 1; j -= 1
        elif i > 0 and D[i][j] == D[i - 1][j] + hueco:
            alin_a.append(a[i - 1]); alin_b.append("-"); i -= 1
        else:
            alin_a.append("-"); alin_b.append(b[j - 1]); j -= 1
    return alin_a[::-1], alin_b[::-1]


def puntaje(a, b, coincidencia=1, desajuste=-1, hueco=-1):
    """Puntaje del alineamiento óptimo usando solo dos filas."""
    previa = [j * hueco for j in range(len(b) + 1)]
    for i in range(1, len(a) + 1):
        actual = [i * hueco] + [0] * len(b)
        for j in range(1, len(b) + 1):
            p = coincidencia if a[i - 1] == b[j - 1] else desajuste
            actual[j] = max(previa[j - 1] + p, previa[j] + hueco, actual[j - 1] + hueco)
        previa = actual
    return previa[-1]


def similitud_needleman_wunsch(tokens_a, tokens_b):
    """Normaliza el puntaje a [0, 1] (válido con coincidencia=1, desajuste=-1, hueco=-1).
    El puntaje va de -L a +L, con L = max(n, m); vale 1 solo si son idénticas."""
    mayor = max(len(tokens_a), len(tokens_b))
    if mayor == 0:
        return 1.0
    return (puntaje(tokens_a, tokens_b) + mayor) / (2 * mayor)


if __name__ == "__main__":
    a = ["ai", "improves", "education"]
    b = ["ai", "supports", "education", "research"]
    for fila in construir_matriz(a, b):
        print(fila)
    print(alineamiento(a, b))
    print(round(similitud_needleman_wunsch(a, b), 4), similitud_needleman_wunsch(a, a))