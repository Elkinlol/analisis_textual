import re

# Lista propia de stopwords en inglés (palabras muy frecuentes sin carga temática)
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
    """Recibe un abstract (str) y devuelve una lista de tokens limpios."""
    texto = texto.lower()                      # 1. minúsculas
    texto = re.sub(r"[^a-z\s]", " ", texto)    # 2. todo lo que no sea letra -> espacio
    tokens = texto.split()                     # 3. separar por espacios
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]  # 4. filtrar


if __name__ == "__main__":
    print(preprocesar("The use of AI-driven tools in education, in 2023, is growing."))
    # esperado: ['use', 'ai', 'driven', 'tools', 'education', 'growing']