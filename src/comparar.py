import json
from pathlib import Path

from preprocessing.text_cleaner import preprocesar
from similarity.jaccard import jaccard
from similarity.levenshtein import similitud_palabras, similitud_caracteres
from similarity.coseno import crear_similitud_tfidf
from similarity.matriz import matriz_similitud
from similarity.needlenman import similitud_needleman_wunsch


BASE = Path(__file__).resolve().parent.parent


def cargar_corpus():
    with open(BASE / "data" / "corpus.json", encoding="utf-8") as f:
        return json.load(f)


def titulo_de(articulo, indice):
    return articulo.get("titulo") or articulo.get("archivo") or f"Artículo {indice}"


def leer_numeros(mensaje, minimo, maximo, cantidad_minima=1):
    """Pide números separados por comas y valida cantidad, rango y repetidos."""
    while True:
        try:
            numeros = [int(x) for x in input(mensaje).split(",")]
        except ValueError:
            print("Escribe solo números separados por comas.")
            continue
        if len(numeros) < cantidad_minima:
            print(f"Elige al menos {cantidad_minima}.")
        elif len(set(numeros)) != len(numeros):
            print("No repitas números.")
        elif any(not minimo <= x <= maximo for x in numeros):
            print(f"Los números deben estar entre {minimo} y {maximo}.")
        else:
            return numeros


def imprimir_matriz(etiquetas, matriz):
    print(" " * 8 + "".join(f"{e:>9}" for e in etiquetas))
    for etiqueta, fila in zip(etiquetas, matriz):
        print(f"{etiqueta:>8}" + "".join(f"{v:>9.4f}" for v in fila))


def main():
    corpus = cargar_corpus()

    # El IDF se calcula con los 20 abstracts, no solo con los elegidos.
    tokens_corpus = [preprocesar(d.get("abstract") or "") for d in corpus]

    algoritmos = {
        "Jaccard": jaccard,
        "Levenshtein (palabras)": similitud_palabras,
        "Levenshtein (caracteres)": similitud_caracteres,
        "TF-IDF + coseno": crear_similitud_tfidf(tokens_corpus),
        "Needleman-Wunsch": similitud_needleman_wunsch,
    }

    print("\nArtículos:")
    for i, d in enumerate(corpus, 1):
        print(f"{i:>2}. {titulo_de(d, i)}")
    elegidos = leer_numeros("\nElige 2 o más (ej: 1, 3, 5): ", 1, len(corpus), 2)

    if any(not tokens_corpus[n - 1] for n in elegidos):
        print("Alguno de los artículos elegidos no tiene abstract válido.")
        return

    nombres = list(algoritmos)
    print("\nAlgoritmos:")
    for i, nombre in enumerate(nombres, 1):
        print(f"{i}. {nombre}")
    algoritmo = nombres[leer_numeros("Elige uno: ", 1, len(nombres))[0] - 1]

    tokens = [tokens_corpus[n - 1] for n in elegidos]
    matriz = matriz_similitud(tokens, algoritmos[algoritmo])

    print(f"\n{algoritmo}")
    imprimir_matriz([f"A{n}" for n in elegidos], matriz)


if __name__ == "__main__":
    main()