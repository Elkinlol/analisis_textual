from math import acos, degrees, sqrt


def producto_punto(u, v):
    resultado = 0

    if isinstance(u, dict):

        for clave in u:
            if clave in v:
                resultado += u[clave] * v[clave]

    else:

        for i in range(len(u)):
            resultado += u[i] * v[i]

    return resultado


def norma(u):
    acumulado = 0

    if isinstance(u, dict):

        for clave in u:
            acumulado += u[clave] ** 2

    else:

        for i in range(len(u)):
            acumulado += u[i] ** 2

    return sqrt(acumulado)


def similitud_coseno(u, v):
    nu = norma(u)
    nv = norma(v)

    if nu == 0 or nv == 0:
        return 0.0

    producto = producto_punto(u, v)

    return producto / (nu * nv)


def angulo_grados(coseno):
    if coseno > 1:
        coseno = 1

    elif coseno < -1:
        coseno = -1

    return degrees(acos(coseno))


def distancia_euclidiana(u, v):
    acumulado = 0

    for i in range(len(u)):
        acumulado += (u[i] - v[i]) ** 2

    return sqrt(acumulado)


def normalizar(u):
    n = norma(u)

    if n == 0:
        return list(u)

    resultado = []

    for valor in u:
        resultado.append(valor / n)

    return resultado