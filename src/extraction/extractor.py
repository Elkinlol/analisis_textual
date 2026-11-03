
import pymupdf as fitz
import json
import re
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent

CARPETA_PDFS = BASE / "data" / "pdfs"
SALIDA = BASE / "data" / "corpus.json"
MANUAL = BASE / "data" / "manual.json"



INICIO = re.compile(
    r"A\s?B\s?S\s?T\s?R\s?A\s?C\s?T\s*[:.\-—]?",
    re.IGNORECASE
)

FINALES = [
    re.compile(r"keywords?\s*[:—\-]", re.IGNORECASE),
    re.compile(r"key\s+words?\s*[:—\-]", re.IGNORECASE),
    re.compile(r"index\s+terms", re.IGNORECASE),
    re.compile(r"\n\s*(?:1\.?|I\.?)?\s*introduction\b", re.IGNORECASE),
    re.compile(r"\n\s*(?:1\.?\s*)?background\b", re.IGNORECASE),
    re.compile(r"©|\bcopyright\b|https?://doi\.org", re.IGNORECASE),
    re.compile(
        r"article\s+history|a\s?r\s?t\s?i\s?c\s?l\s?e\s+i\s?n\s?f\s?o",
        re.IGNORECASE
    ),
]




def leer_texto(ruta_pdf, max_paginas=2):
    """Lee las primeras páginas de un documento PDF."""

    doc = fitz.open(ruta_pdf)

    texto = ""

    for i in range(min(max_paginas, len(doc))):
        texto += doc[i].get_text() + "\n"

    doc.close()

    return texto




def extraer_abstract(texto, min_len=300, max_len=3500):
    """Identifica y extrae el abstract del texto del PDF."""

    for coincidencia in INICIO.finditer(texto):

        resto = texto[coincidencia.end():]

        # Buscar posibles puntos de finalización
        cortes = []

        for patron in FINALES:
            resultado = patron.search(resto)

            if resultado and resultado.start() >= min_len:
                cortes.append(resultado.start())

        # Seleccionar el punto de corte más cercano
        if cortes:
            fin = min(cortes)
        else:
            fin = min(len(resto), 2000)

        candidato = re.sub(
            r"\s+",
            " ",
            resto[:fin]
        ).strip()

        if min_len <= len(candidato) <= max_len:
            return candidato

    return None


def extraer_titulo(ruta_pdf, texto):
    """Obtiene el título desde los metadatos o el contenido del PDF."""

    doc = fitz.open(ruta_pdf)

    meta = doc.metadata or {}

    doc.close()

    if meta.get("title") and len(meta["title"]) > 10:
        return meta["title"].strip()

    lineas = [
        linea.strip()
        for linea in texto.split("\n")
        if linea.strip()
    ]

    return lineas[0] if lineas else None




def limpiar_abstract(texto):
    """Normaliza y limpia el abstract extraído."""

    if not texto:
        return ""

    # Normalización Unicode
    texto = unicodedata.normalize("NFKC", texto)

    # Eliminar bloque de palabras clave
    patron_keywords = (
        r"\s*(?:key\s*words?|index\s+terms)\s*"
        r"(?::|[-—–])?.*$"
    )

    texto = re.sub(
        patron_keywords,
        "",
        texto,
        count=1,
        flags=re.IGNORECASE
    )

    # Unir palabras partidas por saltos de línea
    texto = re.sub(
        r"(\w)-\s*\n\s*([a-z])",
        r"\1\2",
        texto
    )

    # Normalizar espacios
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()




def procesar_pdf(ruta_pdf):
    """Extrae y limpia la información de un documento."""

    texto = leer_texto(ruta_pdf)

    titulo = extraer_titulo(ruta_pdf, texto)

    abstract = extraer_abstract(texto)
    
    autors = extraer_autores(texto)

    if abstract:
        abstract = limpiar_abstract(abstract)

    documento = {
        "archivo": ruta_pdf.name,
        "titulo": titulo,
        "autores": autors,
        "abstract": abstract
    }

    return documento



def buscar_pdfs(carpeta):
    """Busca todos los documentos PDF de una carpeta."""

    if not carpeta.exists():
        print("La carpeta NO existe.")
        return []

    archivos = []

    for archivo in carpeta.rglob("*"):

        if archivo.suffix.lower() == ".pdf":
            archivos.append(archivo)

    archivos.sort()

    print("PDFs encontrados:", len(archivos))

    return archivos




def procesar_archivos(archivos):
    """Procesa cada PDF y construye el corpus."""

    corpus = []

    for archivo in archivos:

        documento = procesar_pdf(archivo)

        corpus.append(documento)

    return corpus



def aplicar_manual(corpus):
    """Aplica correcciones registradas en manual.json."""

    if not MANUAL.exists():
        return corpus

    with open(MANUAL, "r", encoding="utf-8") as archivo:
        manual = json.load(archivo)

    for documento in corpus:

        correcciones = manual.get(documento["archivo"], {})

        documento.update(correcciones)

        # Limpiar también los abstracts corregidos manualmente
        if documento.get("abstract"):
            documento["abstract"] = limpiar_abstract(
                documento["abstract"]
            )

    return corpus




def guardar_corpus(corpus):
    """Guarda el corpus procesado en formato JSON."""

    SALIDA.parent.mkdir(parents=True, exist_ok=True)

    with open(SALIDA, "w", encoding="utf-8") as archivo:

        json.dump(
            corpus,
            archivo,
            ensure_ascii=False,
            indent=4
        )

    print("Corpus guardado en:", SALIDA)



def procesar_carpeta(carpeta=CARPETA_PDFS):
    """Coordina la extracción y procesamiento de los PDF."""

    print("Buscando PDFs en:", carpeta)

    archivos = buscar_pdfs(carpeta)

    if not archivos:
        print("No hay documentos para procesar.")
        return []

    corpus = procesar_archivos(archivos)

    corpus = aplicar_manual(corpus)

    guardar_corpus(corpus)

    print("Documentos procesados:", len(corpus))

    return corpus



def diagnosticar(nombre_parcial, max_paginas=2):
    """Muestra el texto extraído de un PDF específico."""

    if not CARPETA_PDFS.exists():
        print("La carpeta de PDF no existe.")
        return

    for pdf in CARPETA_PDFS.rglob("*"):

        if pdf.suffix.lower() == ".pdf" and nombre_parcial.lower() in pdf.name.lower():

            texto = leer_texto(pdf, max_paginas)

            print("=" * 80)
            print(pdf.name)
            print("=" * 80)

            print(texto[:2500])

            return

    print("No se encontró el documento:", nombre_parcial)

def extraer_autores(texto):
    """Intenta identificar los autores antes del abstract."""

    coincidencia = INICIO.search(texto)

    if not coincidencia:
        return None

    texto_anterior = texto[:coincidencia.start()]

    lineas = []

    for linea in texto_anterior.split("\n"):
        linea = linea.strip()

        if linea:
            lineas.append(linea)

    # Eliminar posibles líneas del título
    if len(lineas) < 2:
        return None

    posibles_autores = lineas[1:]

    autores = []

    for linea in posibles_autores:

        # Evitar información de instituciones y encabezados
        if len(linea) > 150:
            continue

        if re.search(
            r"\b(university|department|faculty|school|institute|"
            r"college|abstract|corresponding|email)\b",
            linea,
            re.IGNORECASE
        ):
            continue

        if re.search(r"@|https?://|\d", linea):
            continue

        autores.append(linea)

    if not autores:
        return None

    return " ".join(autores)


if __name__ == "__main__":
    procesar_carpeta()
