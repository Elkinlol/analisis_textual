
"""
    Coeficiente de Jaccard entre dos listas de tokens.

    J(A, B) = |A ∩ B| / |A ∪ B|,  con A = set(tokens_a) y B = set(tokens_b).

    Ignora el orden y las repeticiones. Devuelve un número en [0, 1].
    Convención: si A y B son vacíos, J = 1 (dos textos vacíos son idénticos).
"""

def jaccard (tokens_a, tokens_b):
    a= set(tokens_a)
    b=set(tokens_b)
    comunes=a & b
    todas= a | b
    if len(todas)==0:
        return 1.0
    return len(comunes)/len(todas)




        


