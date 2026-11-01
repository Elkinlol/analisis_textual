
"""
    Coeficiente de Jaccard entre dos listas de tokens.

    J(A, B) = |A ∩ B| / |A ∪ B|,  con A = set(tokens_a) y B = set(tokens_b).

    Ignora el orden y las repeticiones. Devuelve un número en [0, 1].
    Convención: si A y B son vacíos, J = 1 (dos textos vacíos son idénticos).
"""

def jaccard(tokens_a, tokens_b):

    # Eliminar elementos repetidos
    a = eliminar_repetidos(tokens_a)
    b = eliminar_repetidos(tokens_b)

    # Calcular intersección y unión
    comunes = calcular_interseccion(a, b)
    todas = calcular_union(a, b)

    # Evitar división por cero
    if len(todas) == 0:
        return 1.0

    # Calcular coeficiente
    return len(comunes) / len(todas)

def eliminar_repetidos(tokens):
    resultado = []

    for token in tokens:
        if token not in resultado:
            resultado.append(token)

    return resultado

def calcular_interseccion(a, b):
    comunes = []

    for token in a:
        if token in b:
            comunes.append(token)

    return comunes

def calcular_union(a, b):
    todas = []

    for token in a:
        todas.append(token)

    for token in b:
        if token not in todas:
            todas.append(token)

    return todas

        


