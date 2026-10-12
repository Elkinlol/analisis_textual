
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent

with open(BASE / "data" / "corpus.json", encoding="utf-8") as archivo:
    CORPUS = json.load(archivo)

sys.path.insert(0, str(BASE / "src"))

from preprocessing.text_cleaner import preprocesar


def obtener_titulo(articulo, indice):
    return (
        articulo.get("title")
        or articulo.get("titulo")
        or articulo.get("name")
        or articulo.get("nombre")
        or f"Artículo {indice}"
    )


def mostrar_articulos():
    print("\nARTÍCULOS DISPONIBLES\n")

    for i, articulo in enumerate(CORPUS, start=1):
        print(f"{i}. {obtener_titulo(articulo, i)}")


def seleccionar_articulos():
    mostrar_articulos()

    while True:
        try:
            entrada = input(
                "\nSelecciona dos o más artículos separados por comas: "
            )

            numeros = []

            for numero in entrada.split(","):
                numeros.append(int(numero.strip()))

            if len(numeros) < 2:
                print("Selecciona al menos dos artículos.")
                continue

            if len(numeros) != len(set(numeros)):
                print("No repitas artículos.")
                continue

            if any(numero < 1 or numero > len(CORPUS)
                   for numero in numeros):
                print("Hay números fuera del rango.")
                continue

            articulos = []

            for numero in numeros:
                articulos.append(CORPUS[numero - 1])

            abstracts_validos = True

            for articulo in articulos:
                abstract = articulo.get("abstract")

                if not isinstance(abstract, str) or not abstract.strip():
                    abstracts_validos = False
                    break

            if not abstracts_validos:
                print("Uno de los artículos no tiene un abstract válido.")
                continue

            return numeros, articulos

        except ValueError:
            print("Entrada inválida. Escribe números separados por comas.")


def calcular_needleman_wunsch(tokens_a, tokens_b):
    filas = len(tokens_a) + 1
    columnas = len(tokens_b) + 1

    matriz = []

    for i in range(filas):
        fila = []

        for j in range(columnas):
            fila.append(0)

        matriz.append(fila)

    # Inicializar la primera columna: eliminaciones.
    for i in range(1, filas):
        matriz[i][0] = matriz[i - 1][0] - 1

    # Inicializar la primera fila: inserciones.
    for j in range(1, columnas):
        matriz[0][j] = matriz[0][j - 1] - 1

    # Llenar la matriz usando programación dinámica.
    for i in range(1, filas):
        for j in range(1, columnas):
            if tokens_a[i - 1] == tokens_b[j - 1]:
                puntuacion = 1
            else:
                puntuacion = -1

            diagonal = matriz[i - 1][j - 1] + puntuacion
            arriba = matriz[i - 1][j] - 1
            izquierda = matriz[i][j - 1] - 1

            matriz[i][j] = max(diagonal, arriba, izquierda)

    return matriz[-1][-1]


def similitud_needleman_wunsch(tokens_a, tokens_b):
    if not tokens_a or not tokens_b:
        return 0.0

    puntuacion = calcular_needleman_wunsch(tokens_a, tokens_b)

    longitud_a = len(tokens_a)
    longitud_b = len(tokens_b)

    # Puntuación máxima: todas las palabras de la secuencia
    # más corta coinciden con palabras de la más larga.
    puntuacion_maxima = min(longitud_a, longitud_b)

    # Puntuación mínima posible con las penalizaciones actuales.
    puntuacion_minima = -max(longitud_a, longitud_b)

    if puntuacion_maxima == puntuacion_minima:
        return 0.0

    similitud = (
        (puntuacion - puntuacion_minima)
        / (puntuacion_maxima - puntuacion_minima)
    )

    return max(0.0, min(1.0, similitud))


def matriz_similitud(documentos):
    matriz = []

    for i in range(len(documentos)):
        fila = []

        for j in range(len(documentos)):
            if i == j:
                if documentos[i]:
                    valor = 1.0
                else:
                    valor = 0.0
            else:
                valor = similitud_needleman_wunsch(
                    documentos[i], documentos[j]
                )

            fila.append(valor)

        matriz.append(fila)

    return matriz


def imprimir_matriz(numeros, articulos, matriz):
    cantidad = len(articulos)
    ancho = 12

    print("\n" + "=" * 70)
    print("SIMILITUD NEEDLEMAN-WUNSCH")
    print("=" * 70)

    for i, articulo in enumerate(articulos):
        print(
            f"\nA{i + 1} = Artículo {numeros[i]}: "
            f"{obtener_titulo(articulo, numeros[i])}"
        )

    print("\nMatriz de similitud:\n")

    print(" " * ancho, end="")

    for i in range(cantidad):
        print(f"{'A' + str(i + 1):>{ancho}}", end="")

    print()

    for i, fila in enumerate(matriz):
        print(f"{'A' + str(i + 1):>{ancho}}", end="")

        for valor in fila:
            print(f"{valor:>{ancho}.4f}", end="")

        print()



def main():
    numeros, articulos = seleccionar_articulos()

    documentos = []

    for articulo in articulos:
        tokens = preprocesar(articulo["abstract"])
        documentos.append(tokens)

    print("\n--- Verificación de los abstracts ---")

    for i, documento in enumerate(documentos):
        print(f"A{i + 1}: {len(documento)} palabras")
        print("Primeras 15 palabras:", documento[:15])

    if not any(documentos):
        print("\nNo hay términos válidos para comparar.")
        return

    matriz = matriz_similitud(documentos)
    imprimir_matriz(numeros, articulos, matriz)



if __name__ == "__main__":
    main()
