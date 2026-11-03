def matriz_similitud(lista_tokens, funcion, parametro=None):
    """Matriz simétrica S[i][j] = funcion(x_i, x_j[, parametro]), con diagonal 1.

    Solo se calcula la mitad superior: n(n-1)/2 evaluaciones.
    """
    n = len(lista_tokens)
    matriz = [[1.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if parametro is None:
                valor = funcion(lista_tokens[i], lista_tokens[j])
            else:
                valor = funcion(lista_tokens[i], lista_tokens[j], parametro)
            matriz[i][j] = matriz[j][i] = valor
    return matriz