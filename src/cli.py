import argparse
import json
import sys


def comando_corpus(_args):
    """Extrae título, autores y abstract de los PDFs y escribe data/corpus.json."""
    from extraction.extractor import SALIDA, aplicar_manual, limpiar_abstract, procesar_carpeta

    corpus = aplicar_manual(procesar_carpeta())
    if not corpus:
        print("No se encontraron PDFs: no se escribe corpus.json (se conserva el actual).")
        return 1

    for doc in corpus:
        doc["abstract"] = limpiar_abstract(doc["abstract"] or "")
    sin_abstract = [d["archivo"] for d in corpus if not d["abstract"]]

    SALIDA.parent.mkdir(exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)

    print(f"Corpus guardado: {len(corpus)} documentos en {SALIDA}")
    for nombre in sin_abstract:
        print("  Sin abstract, revisar a mano (data/manual.json):", nombre)
    return 0


def comando_embeddings(_args):
    """Genera data/embeddings_minilm.json y data/embeddings_specter.json."""
    from embeddings.generador import generar_embeddings

    for ruta in generar_embeddings():
        print("Guardado:", ruta)
    return 0


def comando_busqueda(args):
    """Traza paso a paso de KMP, Boyer-Moore y Rabin-Karp sobre un párrafo de un abstract."""
    from matching.trazas import traza_boyer_moore, traza_kmp, traza_rabin_karp
    from registro import cargar_corpus

    corpus = cargar_corpus()
    abstract = corpus[args.articulo - 1]["abstract"]
    texto = abstract[args.inicio:args.inicio + args.largo]

    print(f"Artículo {args.articulo} | patrón = {args.patron!r} | texto ({len(texto)} caracteres):")
    print(texto)
    for titulo, traza in (("KMP", traza_kmp), ("BOYER-MOORE", traza_boyer_moore)):
        print("\n" + "=" * 20, titulo, "=" * 20)
        print(traza(texto, args.patron))
    print("\n" + "=" * 20, f"RABIN-KARP (módulo {args.modulo})", "=" * 20)
    print(traza_rabin_karp(texto, args.patron, modulo=args.modulo))
    return 0


def comando_benchmark(args):
    """Compara KMP, Boyer-Moore y Rabin-Karp (preprocesamiento, búsqueda y comparaciones)."""
    from matching.benchmark import ejecutar, escenarios_corpus, escenarios_sinteticos, formatear
    from registro import cargar_corpus

    escenarios = escenarios_sinteticos() + escenarios_corpus(cargar_corpus(), args.patrones)
    print(formatear(ejecutar(escenarios)))
    return 0


def construir_parser():
    parser = argparse.ArgumentParser(description="Tareas que se ejecutan a mano.")
    sub = parser.add_subparsers(dest="comando", required=True)
    sub.add_parser("corpus", help="extraer los PDFs y escribir data/corpus.json")
    sub.add_parser("embeddings", help="generar los embeddings (requiere sentence-transformers)")

    busqueda = sub.add_parser("busqueda", help="traza de los tres algoritmos de búsqueda")
    busqueda.add_argument("--patron", default="intelligence")
    busqueda.add_argument("--articulo", type=int, default=1, help="número del artículo (1 a 20)")
    busqueda.add_argument("--inicio", type=int, default=0, help="carácter donde empieza el párrafo")
    busqueda.add_argument("--largo", type=int, default=45, help="largo del párrafo")
    busqueda.add_argument("--modulo", type=int, default=101, help="módulo de Rabin-Karp")

    benchmark = sub.add_parser("benchmark", help="rendimiento de los algoritmos de búsqueda")
    benchmark.add_argument("--patrones", nargs="+", default=["learning", "artificial intelligence", "zzzz"])
    return parser


COMANDOS = {
    "corpus": comando_corpus,
    "embeddings": comando_embeddings,
    "busqueda": comando_busqueda,
    "benchmark": comando_benchmark,
}


def main(argv=None):
    args = construir_parser().parse_args(argv)
    return COMANDOS[args.comando](args)


if __name__ == "__main__":
    sys.exit(main())