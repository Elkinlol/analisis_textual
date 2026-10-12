def matriz_similitud(lista_tokens, funcion):
    n = len(lista_tokens)
    matriz = [[1.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            matriz[i][j] = matriz[j][i] = funcion(lista_tokens[i], lista_tokens[j])
    return matriz