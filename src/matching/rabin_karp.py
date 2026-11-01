BASE = 256
MODULO = 1_000_000_007

def preprocesar(patron, base=BASE, modulo=MODULO):
    """Devuelve (H(patrón), b^(m-1) mod q).

    H(P) = ( Σ P[i] · b^(m-1-i) ) mod q, evaluado con el método de Horner:
    h ← (h · b + código(carácter)) mod q.
    """
    m = len(patron)
    factor = 1
    for _ in range(m - 1):
        factor = (factor * base) % modulo
    hash_patron = 0
    for c in patron:
        hash_patron = (hash_patron * base + ord(c)) % modulo
    return hash_patron, factor


def rabin_karp(texto, patron, base=BASE, modulo=MODULO, tablas=None):
    """Todas las posiciones de inicio de patron en texto, con hash rodante.

    Hash de la ventana s+1 a partir de la ventana s:
        H(s+1) = ( (H(s) − T[s] · b^(m-1)) · b + T[s+m] ) mod q
    Si H(ventana) = H(patrón) se verifica carácter a carácter: si el texto es distinto es una
    colisión. Búsqueda: O(n + m) esperado; O(n·m) si hay muchas coincidencias de hash o de texto.
    """
    n, m = len(texto), len(patron)
    if m == 0 or m > n:
        return {"posiciones": [], "comparaciones": 0, "comparaciones_hash": 0, "colisiones": 0}
    hash_patron, factor = tablas if tablas is not None else preprocesar(patron, base, modulo)

    hash_ventana = 0
    for i in range(m):
        hash_ventana = (hash_ventana * base + ord(texto[i])) % modulo

    posiciones, comparaciones, colisiones = [], 0, 0
    for s in range(n - m + 1):
        if hash_ventana == hash_patron:
            iguales = True
            for j in range(m):
                comparaciones += 1
                if texto[s + j] != patron[j]:
                    iguales = False
                    break
            if iguales:
                posiciones.append(s)
            else:
                colisiones += 1
        if s < n - m:
            hash_ventana = ((hash_ventana - ord(texto[s]) * factor) * base + ord(texto[s + m])) % modulo
    return {"posiciones": posiciones, "comparaciones": comparaciones,
            "comparaciones_hash": n - m + 1, "colisiones": colisiones}