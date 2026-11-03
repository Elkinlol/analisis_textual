from pathlib import Path

from registro import cargar_corpus, construir_algoritmos
from similarity.matriz import matriz_similitud
from clustering.jerarquia import agrupar, cortar
from clustering.dendograma import dibujar_dendrograma
from evaluation.metricas import correlacion_cofenetica, silueta

BASE = Path(__file__).resolve().parent.parent
SALIDA = BASE / "output"

ALGORITMO_BASE = "TF-IDF + coseno"       # de aquí sale la matriz de similitud
CRITERIOS = ["single", "complete", "average"]
RANGO_K = range(2, 9)                    # cortes del árbol para la silueta


def distancias_desde_similitud(similitud):
    """Distancia = 1 - similitud."""
    n = len(similitud)
    return [[0.0 if i == j else 1 - similitud[i][j] for j in range(n)] for i in range(n)]


def main():
    corpus = cargar_corpus()
    representaciones, funcion = construir_algoritmos(corpus)[ALGORITMO_BASE]

    similitud = matriz_similitud(representaciones, funcion)
    D = distancias_desde_similitud(similitud)
    etiquetas = [f"A{i + 1}" for i in range(len(corpus))]

    SALIDA.mkdir(exist_ok=True)
    print(f"Matriz base: {ALGORITMO_BASE} | documentos: {len(corpus)}\n")

    resultados = {}
    for criterio in CRITERIOS:
        fusiones = agrupar(D, criterio)
        resultados[criterio] = {
            "fusiones": fusiones,
            "ccc": correlacion_cofenetica(D, fusiones),
            "siluetas": {k: silueta(D, cortar(fusiones, len(D), k)) for k in RANGO_K},
        }
        fig = dibujar_dendrograma(fusiones, etiquetas, f"{criterio} linkage - {ALGORITMO_BASE}")
        fig.savefig(SALIDA / f"dendrograma_{criterio}.png", dpi=150)

    print("Correlación cofenética (1 = el árbol conserva las distancias):")
    for criterio in CRITERIOS:
        print(f"  {criterio:<10}{resultados[criterio]['ccc']:.4f}")

    print("\nSilueta promedio según el número de grupos k:")
    print(f"{'k':<6}" + "".join(f"{c:>12}" for c in CRITERIOS))
    for k in RANGO_K:
        print(f"{k:<6}" + "".join(f"{resultados[c]['siluetas'][k]:>12.4f}" for c in CRITERIOS))

    print("\nDendrogramas guardados en:", SALIDA)
