def tabla_prefijos(patron):
    """Función de fallo π de KMP.

    π[i] = largo del prefijo propio más largo de patron[0..i] que también es sufijo de
    patron[0..i]   (con π[0] = 0).

    Un borde de un borde también es un borde, así que si el siguiente carácter no extiende
    el borde actual k, se prueba con el siguiente más corto, π[k-1]. Tiempo O(m).
    """
    lps = [0] * len(patron)
    k = 0
    for i in range(1, len(patron)):
        while k > 0 and patron[i] != patron[k]:
            k = lps[k - 1]
        if patron[i] == patron[k]:
            k += 1
        lps[i] = k
    return lps


def kmp(texto, patron, tablas=None):
    """Todas las posiciones de inicio de patron en texto (incluye ocurrencias traslapadas).

    Estado: k = largo del prefijo del patrón que es sufijo de texto[0..i] (como un AFD).
    Ante un desajuste con k > 0 se retrocede en el patrón (k = π[k-1]) y nunca en el texto,
    por eso el texto se recorre una sola vez. Búsqueda O(n), con a lo sumo 2n comparaciones.
    """
    n, m = len(texto), len(patron)
    if m == 0 or m > n:
        return {"posiciones": [], "comparaciones": 0}
    lps = tablas if tablas is not None else tabla_prefijos(patron)

    posiciones, comparaciones, k = [], 0, 0
    for i in range(n):
        while True:
            comparaciones += 1
            if texto[i] == patron[k]:
                k += 1
                break
            if k == 0:
                break
            k = lps[k - 1]
        if k == m:                              # estado de aceptación
            posiciones.append(i - m + 1)
            k = lps[k - 1]
    return {"posiciones": posiciones, "comparaciones": comparaciones}