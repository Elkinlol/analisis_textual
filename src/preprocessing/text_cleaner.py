import re


# Lista propia de stopwords en inglés
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "nor", "so", "yet",
    "of", "in", "on", "at", "to", "for", "from", "by", "with", "about",
    "as", "into", "through", "over", "under", "between", "among", "within",
    "is", "are", "was", "were", "be", "been", "being", "am",
    "has", "have", "had", "do", "does", "did",
    "it", "its", "this", "that", "these", "those", "which", "who", "whom",
    "we", "our", "they", "their", "he", "she", "his", "her", "you", "your",
    "can", "could", "may", "might", "will", "would", "should", "also",
    "not", "no", "than", "then", "such", "both", "each", "other", "more",
    "most", "some", "any", "all", "however", "thus", "while", "when", "where",
}


def preprocesar(texto):
    """
    Por medio de este proceso recibimos cada uno de los abstracts y devolvemos
    la lista de tokens.
    
    Podemos definir este proceso en 5 pasos principaales
    1. Pasamos todo el abstract a minusculas
    2. Eliminacion de todos los caracteres diferentes a letras y espacios
    3. Separamos los tokens
    4. Se elimina todas las stopwords, dado a que no tienen un valor real para el analisis
    5. Finalmente se hace la eliminación de tokens de un solo carácter.
    """

    if not texto:
        return []

    texto = texto.lower()

    texto = re.sub(r"[^a-z\s]", " ", texto)

    tokens = texto.split()

    tokens_limpios = []

    for token in tokens:
        if token not in STOPWORDS and len(token) > 1:
            tokens_limpios.append(token)

    return tokens_limpios