def tabla_caracter_malo(patron):
    """λ(c) = última posición de c en el patrón (las ausentes valen -1 al consultar)."""
    ultimo = {}
    for j, c in enumerate(patron):
        ultimo[c] = j
    return ultimo


def tabla_sufijo_bueno(patron):
    """Regla (fuerte) del sufijo bueno.

    bueno[j] = desplazamiento mínimo s ≥ 1 que alinea de nuevo el sufijo patron[j..m-1] ya
    emparejado con otra aparición suya en el patrón (precedida por un carácter distinto de
    patron[j-1]) o, si no existe, con un prefijo del patrón. bueno[m] = 1 (sufijo vacío) y
    bueno[0] se usa tras encontrar una ocurrencia completa.
    Se calcula con el arreglo de bordes de los sufijos. Tiempo O(m).
    """
    m = len(patron)
    desplazamiento = [0] * (m + 1)
    borde = [0] * (m + 1)

    # Caso 1: el sufijo que coincidió reaparece más a la izquierda en el patrón
    i, j = m, m + 1
    borde[i] = j
    while i > 0:
        while j <= m and patron[i - 1] != patron[j - 1]:
            if desplazamiento[j] == 0:
                desplazamiento[j] = j - i
            j = borde[j]
        i -= 1
        j -= 1
        borde[i] = j

    # Caso 2: solo un prefijo del patrón coincide con un sufijo de lo ya emparejado
    j = borde[0]
    for i in range(m + 1):
        if desplazamiento[i] == 0:
            desplazamiento[i] = j
        if i == j:
            j = borde[j]
    return desplazamiento


def preprocesar(patron):
    return tabla_caracter_malo(patron), tabla_sufijo_bueno(patron)


def boyer_moore(texto, patron, tablas=None):
    """Todas las posiciones de inicio de patron en texto, comparando de derecha a izquierda.

    Si falla la comparación en la posición j del patrón con el carácter c del texto, se avanza
        max( j - λ(c) ,  bueno[j+1] )     (carácter malo, sufijo bueno)
    Tras una ocurrencia se avanza bueno[0]. Búsqueda: mejor caso O(n/m); peor caso O(n·m)
    (por ejemplo, texto aaaa… con patrón aaa…, donde el patrón aparece en todas partes).
    """
    n, m = len(texto), len(patron)
    if m == 0 or m > n:
        return {"posiciones": [], "comparaciones": 0}
    malo, bueno = tablas if tablas is not None else preprocesar(patron)

    posiciones, comparaciones, s = [], 0, 0
    while s <= n - m:
        j = m - 1
        while j >= 0:
            comparaciones += 1
            if patron[j] != texto[s + j]:
                break
            j -= 1
        if j < 0:
            posiciones.append(s)
            s += bueno[0]
        else:
            ultimo = malo.get(texto[s + j], -1)
            s += max(bueno[j + 1], j - ultimo)
    return {"posiciones": posiciones, "comparaciones": comparaciones}