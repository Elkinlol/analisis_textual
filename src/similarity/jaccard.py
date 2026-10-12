import json
import sys
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent.parent
CORPUS=json.load(open(BASE / "data" / "corpus.json", encoding="utf-8"))
sys.path.insert(0, str(BASE / "src"))               # 1. primero esto
from preprocessing.text_cleaner import preprocesar  # 2. después el import

def jaccard (tokens_a, tokens_b):
    a= set(tokens_a)
    b=set(tokens_b)
    comunes=a & b
    todas= a | b
    if len(todas)==0:
        return 1.0
    return len(comunes)/len(todas)

def matriz_similitud(lista_tokens, funcion):
    n = len(lista_tokens)
    matriz = [[0.0] * n for _ in range(n)]      # tabla n x n de ceros
    for i in range(n):
        for j in range(i, n):                    # solo la mitad superior
            valor = funcion(lista_tokens[i], lista_tokens[j])
            matriz[i][j] = valor
            matriz[j][i] = valor                 # espejo
    return matriz

def imprimir_matriz():
    tokens = [preprocesar(CORPUS[k]["abstract"]) for k in (0, 1)]
    m = matriz_similitud(tokens, jaccard)
    for fila in m:
        print([round(x, 4) for x in fila])
        



if __name__ == "__main__":
    sys.path.insert(0, str(BASE / "src"))

    # 2. Dos abstracts reales
    a = preprocesar(CORPUS[0]["abstract"])
    b = preprocesar(CORPUS[1]["abstract"])
    print (a)
    print (b)
    aux=0
    for i in range (len(a)-1): 
        aux+=1
    print (aux)
    print(round(jaccard(a, b), 4))

    # 3. Un abstract contra sí mismo: 1.0
    print(jaccard(a, a))
    
    imprimir_matriz()
