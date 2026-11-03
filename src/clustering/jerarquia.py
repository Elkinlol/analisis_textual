def distancia_entre_clusters(D, a, b, criterio):
    """Distancia entre dos clusters a partir de la matriz D original.
    a y b son listas con los índices de sus miembros."""
    distancias = [D[i][j] for i in a for j in b]
    if criterio == "single":        # el par más cercano
        return min(distancias)
    if criterio == "complete":      # el par más lejano
        return max(distancias)
    if criterio == "average":       # promedio de todos los pares (UPGMA)
        return sum(distancias) / len(distancias)
    raise ValueError(f"Criterio desconocido: {criterio}")


def agrupar(D, criterio):
    """Clustering jerárquico aglomerativo.
    Devuelve una lista de fusiones (id_a, id_b, altura, tamaño).
    Las hojas son 0..n-1 y cada fusión crea el cluster n, n+1, ..."""
    n = len(D)
    clusters = {i: [i] for i in range(n)}      # id -> miembros
    fusiones = []
    siguiente = n

    while len(clusters) > 1:
        ids = sorted(clusters)
        mejor = None
        for x in range(len(ids)):
            for y in range(x + 1, len(ids)):
                d = distancia_entre_clusters(D, clusters[ids[x]], clusters[ids[y]], criterio)
                if mejor is None or d < mejor[0]:
                    mejor = (d, ids[x], ids[y])

        d, a, b = mejor
        clusters[siguiente] = clusters.pop(a) + clusters.pop(b)
        fusiones.append((a, b, d, len(clusters[siguiente])))
        siguiente += 1

    return fusiones


def cortar(fusiones, n, k):
    """Repite las primeras n-k fusiones y devuelve la etiqueta de cluster de cada documento."""
    clusters = {i: [i] for i in range(n)}
    for paso, (a, b, _, _) in enumerate(fusiones[: n - k]):
        clusters[n + paso] = clusters.pop(a) + clusters.pop(b)
    etiquetas = [0] * n
    for etiqueta, miembros in enumerate(clusters.values()):
        for m in miembros:
            etiquetas[m] = etiqueta
    return etiquetas


def matriz_cofenetica(fusiones, n):
    """C[i][j] = altura a la que i y j quedan juntos por primera vez en el árbol."""
    miembros = {i: [i] for i in range(n)}
    C = [[0.0] * n for _ in range(n)]
    for paso, (a, b, altura, _) in enumerate(fusiones):
        for i in miembros[a]:
            for j in miembros[b]:
                C[i][j] = C[j][i] = altura
        miembros[n + paso] = miembros.pop(a) + miembros.pop(b)
    return C

