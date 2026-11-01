from math import log
from similarity.vectores import similitud_coseno


def contar_frecuencias(tokens):
    frecuencias = {}

    for palabra in tokens:
        if palabra in frecuencias:
            frecuencias[palabra] += 1
        else:
            frecuencias[palabra] = 1

    return frecuencias


def calcular_idf(documentos):
    n = len(documentos)
    frecuencia_doc = {}

    for doc in documentos:

        palabras_documento = []

        for palabra in doc:
            if palabra not in palabras_documento:
                palabras_documento.append(palabra)

        for palabra in palabras_documento:
            if palabra in frecuencia_doc:
                frecuencia_doc[palabra] += 1
            else:
                frecuencia_doc[palabra] = 1

    idf = {}

    for palabra in frecuencia_doc:
        df = frecuencia_doc[palabra]
        idf[palabra] = log((n + 1) / (df + 1)) + 1

    return idf


def vectorizar(tokens, idf):
    if len(tokens) == 0:
        return {}

    frecuencias = contar_frecuencias(tokens)
    total = len(tokens)
    vector = {}

    for palabra in frecuencias:
        tf = frecuencias[palabra] / total

        if palabra in idf:
            peso = tf * idf[palabra]
        else:
            peso = 0

        vector[palabra] = peso

    return vector


def crear_similitud_tfidf(corpus_tokens):
    idf = calcular_idf(corpus_tokens)

    def similitud(tokens_a, tokens_b):
        vector_a = vectorizar(tokens_a, idf)
        vector_b = vectorizar(tokens_b, idf)

        return similitud_coseno(vector_a, vector_b)

    return similitud


def top_terminos(tokens, idf, k=10):
    vector = vectorizar(tokens, idf)

    terminos = []

    for palabra in vector:
        terminos.append([palabra, vector[palabra]])

    # Ordenamiento por selección descendente
    for i in range(len(terminos)):
        mayor = i

        for j in range(i + 1, len(terminos)):
            if terminos[j][1] > terminos[mayor][1]:
                mayor = j

        temporal = terminos[i]
        terminos[i] = terminos[mayor]
        terminos[mayor] = temporal

    resultado = []

    limite = min(k, len(terminos))

    for i in range(limite):
        resultado.append((terminos[i][0], terminos[i][1]))

    return resultado