import pymupdf as fitz
import json
import re
from pathlib import Path
import unicodedata

BASE = Path(__file__).resolve().parent.parent.parent
CARPETA_PDFS = BASE / "data" / "pdfs"
SALIDA = BASE / "data" / "corpus.json"
MANUAL = BASE / "data" / "manual.json"

def aplicar_manual(corpus):
    if not MANUAL.exists():
        return corpus
    manual = json.load(open(MANUAL, encoding="utf-8"))
    for doc in corpus:
        doc.update(manual.get(doc["archivo"], {}))
    return corpus
def leer_texto(ruta_pdf, max_paginas=2):
    """Lee solo las primeras páginas: el abstract casi siempre está ahí."""
    doc = fitz.open(ruta_pdf)
    texto = ""
    for i in range(min(max_paginas, len(doc))):
        texto += doc[i].get_text() + "\n"
    doc.close()
    return texto

INICIO = re.compile(r"A\s?B\s?S\s?T\s?R\s?A\s?C\s?T\s*[:.\-—]?", re.IGNORECASE)

#Posibles ffinales abstract
FINALES = [
    re.compile(r"keywords?\s*[:—\-]", re.IGNORECASE),
    re.compile(r"key\s+words?\s*[:—\-]", re.IGNORECASE),
    re.compile(r"index\s+terms", re.IGNORECASE),
    re.compile(r"\n\s*(?:1\.?|I\.?)?\s*introduction\b", re.IGNORECASE),
    re.compile(r"\n\s*(?:1\.?\s*)?background\b", re.IGNORECASE),
    re.compile(r"©|\bcopyright\b|https?://doi\.org", re.IGNORECASE),
    re.compile(r"article\s+history|a\s?r\s?t\s?i\s?c\s?l\s?e\s+i\s?n\s?f\s?o", re.IGNORECASE),
]

def extraer_abstract(texto, min_len=300, max_len=3500):
    for m in INICIO.finditer(texto):
        resto = texto[m.end():]
        # el final más cercano entre todos los patrones
        cortes = [f.search(resto) for f in FINALES]
        cortes = [c.start() for c in cortes if c and c.start() >= min_len]
        fin = min(cortes) if cortes else min(len(resto), 2000)
        candidato = re.sub(r"\s+", " ", resto[:fin]).strip()
        if min_len <= len(candidato) <= max_len:
            return candidato
    return None

def extraer_titulo(ruta_pdf, texto):
    doc = fitz.open(ruta_pdf)
    meta = doc.metadata or {}
    doc.close()
    if meta.get("title") and len(meta["title"]) > 10:
        return meta["title"].strip()
    lineas = [l.strip() for l in texto.split("\n") if l.strip()]
    return lineas[0] if lineas else None

def procesar_carpeta(carpeta=CARPETA_PDFS):
    print("Buscando PDFs en:", carpeta)
    if not carpeta.exists():
        print("La carpeta NO existe.")
        return []

    archivos = sorted(p for p in carpeta.rglob("*") if p.suffix.lower() == ".pdf")
    print("PDFs encontrados:", len(archivos))

    corpus = []
    for pdf in archivos:
        texto = leer_texto(pdf)
        corpus.append({
            "archivo": pdf.name,
            "titulo": extraer_titulo(pdf, texto),
            "autores": None,
            "abstract": extraer_abstract(texto),
        })
    return corpus

def diagnosticar(nombre_parcial, max_paginas=2):
    for pdf in CARPETA_PDFS.rglob("*.pdf"):
        if nombre_parcial in pdf.name:
            texto = leer_texto(pdf, max_paginas)
            print("=" * 80, "\n", pdf.name, "\n", "=" * 80)
            print(texto[:2500])
            

def limpiar_abstract(txt):
    txt = unicodedata.normalize("NFKC", txt)   # arregla ligaduras: ﬁ -> fi
    txt = re.split(r"\s+Key\s?words?\b\s*(?::|(?=[A-Z]))", txt, maxsplit=1)[0]
    txt = re.sub(r"\b(AI|instance|human|pre)- ", r"\1-", txt)  # proteger guiones legítimos
    txt = re.sub(r"(\w)- ([a-z])", r"\1\2", txt)               # unir palabras rotas
    return re.sub(r"\s+", " ", txt).strip()

        
