from matching.boyer_moore import tabla_caracter_malo, tabla_sufijo_bueno
from matching.kmp import tabla_prefijos
from matching.rabin_karp import BASE, preprocesar as preprocesar_rk


def _fila(titulo, valores, ancho=3):
    return f"{titulo:<10}" + "".join(f"{str(v):>{ancho}}" for v in valores)


def _alineamiento(texto, patron, inicio, columna_marca=None, nota=""):
    """Dibuja el patrón desplazado `inicio` posiciones bajo el texto, con una marca opcional."""
    lineas = ["    texto : " + texto, "    patrón: " + " " * inicio + patron]
    if columna_marca is not None:
        lineas.append("            " + " " * columna_marca + "^ " + nota)
    return lineas


def traza_kmp(texto, patron):
    """Texto de la traza de KMP: tabla de prefijos y cada realineación del patrón."""
    lps = tabla_prefijos(patron)
    m = len(patron)
    lineas = ["TABLA DE PREFIJOS (π)",
              _fila("índice", range(m)), _fila("patrón", patron), _fila("π", lps),
              "", "BÚSQUEDA (solo se dibujan los desajustes con k > 0; los demás solo avanzan i)"]
    k, comparaciones, triviales = 0, 0, 0
    for i in range(len(texto)):
        while True:
            comparaciones += 1
            if texto[i] == patron[k]:
                k += 1
                break
            if k == 0:
                triviales += 1
                break
            lineas.append(f"\ni={i}: coincidieron k={k} caracteres y falla texto[{i}]={texto[i]!r} "
                          f"vs patrón[{k}]={patron[k]!r}")
            lineas += _alineamiento(texto, patron, i - k, i, "desajuste")
            nuevo = lps[k - 1]
            lineas.append(f"    k pasa de {k} a π[{k - 1}] = {nuevo}: el patrón se corre a la "
                          f"posición {i - nuevo} (el texto no retrocede)")
            k = nuevo
        if k == m:
            lineas.append(f"\ni={i}: OCURRENCIA en la posición {i - m + 1}")
            lineas += _alineamiento(texto, patron, i - m + 1)
            lineas.append(f"    k pasa de {m} a π[{m - 1}] = {lps[m - 1]}")
            k = lps[k - 1]
    lineas += ["", f"Comparaciones de caracteres: {comparaciones} (texto de {len(texto)} caracteres; "
               f"{triviales} desajustes con k = 0)"]
    return "\n".join(lineas)


def traza_boyer_moore(texto, patron):
    """Texto de la traza de Boyer-Moore: las dos tablas y cada desplazamiento."""
    malo = tabla_caracter_malo(patron)
    bueno = tabla_sufijo_bueno(patron)
    m, n = len(patron), len(texto)
    lineas = ["TABLA DEL CARÁCTER MALO  λ(c) = última posición de c en el patrón",
              "  " + ", ".join(f"{c!r}: {j}" for c, j in malo.items()) + "   (los demás: -1)",
              "", "TABLA DEL SUFIJO BUENO  (bueno[j]: el sufijo patrón[j..] ya coincidió)",
              _fila("j", range(m + 1)), _fila("bueno[j]", bueno),
              "", "BÚSQUEDA (se compara de derecha a izquierda)"]
    s, comparaciones = 0, 0
    while s <= n - m:
        j = m - 1
        while j >= 0:
            comparaciones += 1
            if patron[j] != texto[s + j]:
                break
            j -= 1
        lineas.append(f"\nalineación s={s}")
        if j < 0:
            lineas += _alineamiento(texto, patron, s, s, "OCURRENCIA")
            lineas.append(f"    avanza bueno[0] = {bueno[0]}")
            s += bueno[0]
        else:
            ultimo = malo.get(texto[s + j], -1)
            a, b = j - ultimo, bueno[j + 1]
            lineas += _alineamiento(texto, patron, s, s + j,
                                    f"falla en j={j}: texto={texto[s + j]!r}, patrón={patron[j]!r}")
            lineas.append(f"    carácter malo: {j} - ({ultimo}) = {a}   |   sufijo bueno: "
                          f"bueno[{j + 1}] = {b}   ->   avanza {max(a, b)}")
            s += max(a, b)
    lineas += ["", f"Alineaciones probadas: {len(_posiciones_visitadas(texto, patron))}, "
               f"comparaciones de caracteres: {comparaciones} (texto de {n} caracteres)"]
    return "\n".join(lineas)


def _posiciones_visitadas(texto, patron):
    malo, bueno = tabla_caracter_malo(patron), tabla_sufijo_bueno(patron)
    m, n, s, visitadas = len(patron), len(texto), 0, []
    while s <= n - m:
        visitadas.append(s)
        j = m - 1
        while j >= 0 and patron[j] == texto[s + j]:
            j -= 1
        s += bueno[0] if j < 0 else max(bueno[j + 1], j - malo.get(texto[s + j], -1))
    return visitadas


def traza_rabin_karp(texto, patron, base=BASE, modulo=101):
    """Texto de la traza de Rabin-Karp: hash del patrón y hash de cada ventana."""
    hp, factor = preprocesar_rk(patron, base, modulo)
    m, n = len(patron), len(texto)
    lineas = [f"Base b = {base}, módulo q = {modulo}, b^(m-1) mod q = {factor}",
              "", "HASH DEL PATRÓN (Horner): h = (h·b + código) mod q"]
    h = 0
    for c in patron:
        nuevo = (h * base + ord(c)) % modulo
        lineas.append(f"  {c!r} (código {ord(c)}): ({h}·{base} + {ord(c)}) mod {modulo} = {nuevo}")
        h = nuevo
    lineas += [f"  H(patrón) = {hp}", "", "VENTANAS DEL TEXTO"]

    hv = 0
    for i in range(m):
        hv = (hv * base + ord(texto[i])) % modulo
    colisiones, ocurrencias = 0, 0
    for s in range(n - m + 1):
        ventana = "".join(texto[s + j] for j in range(m))
        linea = f"s={s:<3} ventana={ventana!r:<16} H={hv:<4}"
        if hv == hp:
            igual = all(texto[s + j] == patron[j] for j in range(m))
            ocurrencias += igual
            colisiones += not igual
            linea += " hash igual -> " + ("OCURRENCIA" if igual else "COLISIÓN: el texto es distinto")
        lineas.append(linea)
        if s < n - m:
            nuevo = ((hv - ord(texto[s]) * factor) * base + ord(texto[s + m])) % modulo
            lineas.append(f"      H(s+1) = (({hv} − {ord(texto[s])}·{factor})·{base} + {ord(texto[s + m])}) mod {modulo} = {nuevo}")
            hv = nuevo
    lineas += ["", f"Ocurrencias: {ocurrencias} | colisiones: {colisiones} | ventanas: {n - m + 1}"]
    return "\n".join(lineas)