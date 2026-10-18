from math import sqrt

from clustering.jerarquia import matriz_cofenetica


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    vx = sum((a - mx) ** 2 for a in x)
    vy = sum((b - my) ** 2 for b in y)
    if vx == 0 or vy == 0:
        return 0.0
    return cov / sqrt(vx * vy)


def correlacion_cofenetica(D, fusiones):
    """Qué tan bien el árbol conserva las distancias originales (1 = perfecto)."""
    n = len(D)
    C = matriz_cofenetica(fusiones, n)
    originales = [D[i][j] for i in range(n) for j in range(i + 1, n)]
    del_arbol = [C[i][j] for i in range(n) for j in range(i + 1, n)]
    return pearson(originales, del_arbol)


def silueta(D, etiquetas):
    """Silueta promedio de una partición (de -1 a 1; más alto = clusters más coherentes)."""
    n = len(D)
    grupos = {}
    for i, e in enumerate(etiquetas):
        grupos.setdefault(e, []).append(i)
    if len(grupos) < 2:
        return 0.0

    total = 0.0
    for i in range(n):
        propios = [j for j in grupos[etiquetas[i]] if j != i]
        if not propios:                       # cluster de un solo elemento
            continue
        a = sum(D[i][j] for j in propios) / len(propios)
        b = min(
            sum(D[i][j] for j in miembros) / len(miembros)
            for e, miembros in grupos.items() if e != etiquetas[i]
        )
        mayor = max(a, b)
        total += (b - a) / mayor if mayor > 0 else 0.0
    return total / n