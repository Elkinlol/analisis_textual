import random
from time import perf_counter

from matching.algoritmos import ALGORITMOS_BUSQUEDA


def _mejor_tiempo_ms(funcion, repeticiones=3):
    mejor, resultado = None, None
    for _ in range(repeticiones):
        t0 = perf_counter()
        resultado = funcion()
        t = (perf_counter() - t0) * 1000
        mejor = t if mejor is None or t < mejor else mejor
    return mejor, resultado


def escenarios_sinteticos(n=100_000, semilla=7):
    """Casos que ponen a prueba la teoría: alfabeto grande, alfabeto pequeño y peores casos."""
    azar = random.Random(semilla)
    texto26 = "".join(azar.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n))
    texto2 = "".join(azar.choice("ab") for _ in range(n))
    return [
        ("Alfabeto 26, patrón ausente (m=8)", texto26, "zzzzzzzz"),
        ("Alfabeto 2, patrón de m=20", texto2, "a" * 19 + "b"),
        ("Texto a^n, patrón a^49 b (ausente)", "a" * n, "a" * 49 + "b"),
        ("Texto a^n, patrón a^50 (aparece en todas partes)", "a" * n, "a" * 50),
    ]


def escenarios_corpus(corpus, patrones):
    """Los abstracts reales: uno solo, y todos concatenados."""
    abstracts = [d.get("abstract") or "" for d in corpus]
    lista = []
    for patron in patrones:
        lista.append((f"Abstract 1 ({len(abstracts[0])} car.), {patron!r}", abstracts[0], patron))
        lista.append((f"Corpus completo ({len(' '.join(abstracts))} car.), {patron!r}",
                      " ".join(abstracts), patron))
    return lista


def ejecutar(escenarios):
    """Para cada escenario y algoritmo: tiempo de preprocesamiento y de búsqueda, y conteos."""
    filas = []
    for nombre, texto, patron in escenarios:
        for algoritmo, (preprocesar, buscar) in ALGORITMOS_BUSQUEDA.items():
            t_pre, tablas = _mejor_tiempo_ms(lambda: preprocesar(patron))
            t_bus, res = _mejor_tiempo_ms(lambda: buscar(texto, patron, tablas=tablas))
            filas.append({
                "escenario": nombre, "algoritmo": algoritmo, "n": len(texto), "m": len(patron),
                "ocurrencias": len(res["posiciones"]), "comparaciones": res["comparaciones"],
                "comp_por_caracter": res["comparaciones"] / len(texto),
                "pre_ms": t_pre, "busqueda_ms": t_bus,
            })
    return filas


def formatear(filas):
    cabecera = (f"{'Escenario':<52}{'Algoritmo':<13}{'n':>8}{'m':>4}{'occ':>6}"
                f"{'comp':>9}{'comp/n':>8}{'pre ms':>9}{'búsq ms':>10}")
    lineas, anterior = [cabecera], None
    for f in filas:
        if anterior is not None and f["escenario"] != anterior:
            lineas.append("")
        anterior = f["escenario"]
        lineas.append(f"{f['escenario'][:51]:<52}{f['algoritmo']:<13}{f['n']:>8}{f['m']:>4}"
                      f"{f['ocurrencias']:>6}{f['comparaciones']:>9}{f['comp_por_caracter']:>8.2f}"
                      f"{f['pre_ms']:>9.4f}{f['busqueda_ms']:>10.2f}")
    return "\n".join(lineas)