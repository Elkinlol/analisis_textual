from matplotlib.figure import Figure


def _orden_hojas(fusiones, n):
    hijos = {n + paso: (a, b) for paso, (a, b, _, _) in enumerate(fusiones)}

    def recorrer(nodo):
        if nodo < n:
            return [nodo]
        a, b = hijos[nodo]
        return recorrer(a) + recorrer(b)

    return recorrer(n + len(fusiones) - 1)


def dibujar_dendrograma(fusiones, etiquetas, titulo=""):
    """Dibuja el dendrograma con líneas (sin usar scipy). Devuelve una Figure."""
    n = len(etiquetas)
    orden = _orden_hojas(fusiones, n)
    posicion = {hoja: k for k, hoja in enumerate(orden)}
    altura = {i: 0.0 for i in range(n)}

    fig = Figure(figsize=(9, max(4, 0.35 * n)))
    ax = fig.subplots()

    for paso, (a, b, h, _) in enumerate(fusiones):
        nuevo = n + paso
        ya, yb = posicion[a], posicion[b]
        ax.plot([altura[a], h], [ya, ya], color="#1f4e79")     # rama de a
        ax.plot([altura[b], h], [yb, yb], color="#1f4e79")     # rama de b
        ax.plot([h, h], [ya, yb], color="#1f4e79")             # unión vertical
        posicion[nuevo] = (ya + yb) / 2
        altura[nuevo] = h

    ax.set_yticks(range(n))
    ax.set_yticklabels([etiquetas[h] for h in orden])
    ax.invert_yaxis()
    ax.set_xlabel("Distancia de fusión")
    ax.set_title(titulo)
    fig.tight_layout()
    return fig