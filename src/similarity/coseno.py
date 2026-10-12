from collections import Counter
from math import acos, degrees, log, sqrt


def calcular_idf(documentos):
    """IDF suavizado: log((N + 1) / (df + 1)) + 1, calculado sobre TODO el corpus."""
    n = len(documentos)
    frecuencia_doc = Counter()
    for doc in documentos:
        for palabra in set(doc):
            frecuencia_doc[palabra] += 1
    return {p: log((n + 1) / (df + 1)) + 1 for p, df in frecuencia_doc.items()}


def vectorizar(tokens, idf):
    """Vector disperso: diccionario palabra -> peso TF-IDF."""
    if not tokens:
        return {}
    total = len(tokens)
    return {p: (f / total) * idf.get(p, 0) for p, f in Counter(tokens).items()}


def producto_punto(va, vb):
    comunes = va.keys() & vb.keys()
    return sum(va[p] * vb[p] for p in comunes)


def norma(v):
    return sqrt(sum(x * x for x in v.values()))


def similitud_coseno(va, vb):
    na, nb = norma(va), norma(vb)
    if na == 0 or nb == 0:
        return 0.0
    return producto_punto(va, vb) / (na * nb)


def angulo_grados(coseno):
    coseno = max(-1.0, min(1.0, coseno))      # evita errores de redondeo
    return degrees(acos(coseno))


def crear_similitud_tfidf(corpus_tokens):
    """Fija el IDF con todo el corpus y devuelve f(tokens_a, tokens_b)
    con la misma firma que jaccard y levenshtein."""
    idf = calcular_idf(corpus_tokens)

    def similitud(tokens_a, tokens_b):
        return similitud_coseno(vectorizar(tokens_a, idf), vectorizar(tokens_b, idf))

    return similitud


def top_terminos(tokens, idf, k=10):
    """Los k términos con mayor peso TF-IDF (útil para el caso de estudio)."""
    vector = vectorizar(tokens, idf)
    return sorted(vector.items(), key=lambda par: par[1], reverse=True)[:k]


if __name__ == "__main__":
    # Verificación a mano: A = "ai education", B = "ai research", C = "education research"
    docs = [["ai", "education"], ["ai", "research"], ["education", "research"]]
    idf = calcular_idf(docs)
    print("IDF:", {p: round(v, 4) for p, v in idf.items()})
    va, vb = vectorizar(docs[0], idf), vectorizar(docs[1], idf)
    c = similitud_coseno(va, vb)
    print("coseno(A, B) =", round(c, 4), "| ángulo =", round(angulo_grados(c), 1), "grados")