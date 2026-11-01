import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # para encontrar registro.py

import pandas as pd
import streamlit as st

from registro import cargar_corpus, construir_algoritmos
from similarity.matriz import matriz_similitud
from clustering.jerarquia import agrupar, cortar
from clustering.dendograma import dibujar_dendrograma
from evaluation.metricas import correlacion_cofenetica, silueta

st.set_page_config(page_title="Agrupamiento jerárquico", layout="wide")

CRITERIOS = ["single", "complete", "average"]
RANGO_K = list(range(2, 9))


@st.cache_resource
def cargar():
    corpus = cargar_corpus()
    return corpus, construir_algoritmos(corpus)


@st.cache_data(show_spinner=False)
def distancias(nombre):
    """Matriz de distancias entre los documentos: 1 - similitud."""
    _, algoritmos = cargar()
    representaciones, funcion = algoritmos[nombre]
    s = matriz_similitud(representaciones, funcion)
    n = len(s)
    return [[0.0 if i == j else 1 - s[i][j] for j in range(n)] for i in range(n)]


@st.cache_data(show_spinner=False)
def arbol(nombre, criterio):
    return agrupar(distancias(nombre), criterio)


corpus, algoritmos = cargar()
n = len(corpus)
etiquetas = [f"A{i + 1}" for i in range(n)]
titulos = [d.get("titulo") or d["archivo"] for d in corpus]

st.title("Agrupamiento jerárquico")
st.caption(
    "Los 20 abstracts se agrupan con tres criterios de enlace implementados desde cero. "
    "La distancia entre documentos es 1 - similitud."
)

# Levenshtein por caracteres tarda minutos con todos los pares, se excluye aquí.
opciones = [a for a in algoritmos if "caracteres" not in a]
predeterminado = opciones.index("TF-IDF + coseno") if "TF-IDF + coseno" in opciones else 0

col1, col2 = st.columns(2)
with col1:
    base = st.selectbox("Similitud base", opciones, index=predeterminado)
with col2:
    k = st.slider("Número de grupos (k) para cortar el árbol", 2, 8, 3)

with st.spinner("Calculando..."):
    D = distancias(base)
    fusiones = {c: arbol(base, c) for c in CRITERIOS}
    ccc = {c: correlacion_cofenetica(D, fusiones[c]) for c in CRITERIOS}
    siluetas = {c: {kk: silueta(D, cortar(fusiones[c], n, kk)) for kk in RANGO_K} for c in CRITERIOS}

st.subheader("¿Qué criterio agrupa de forma más coherente?")
tabla_ccc = pd.DataFrame({"Correlación cofenética": ccc})
tabla_sil = pd.DataFrame(siluetas, index=RANGO_K)
tabla_sil.index.name = "k"

izq, der = st.columns(2)
with izq:
    st.markdown("**Correlación cofenética** (1 = el árbol conserva las distancias)")
    st.dataframe(tabla_ccc.style.format("{:.4f}"))
with der:
    st.markdown("**Silueta promedio** según k (más alta = grupos más coherentes)")
    st.dataframe(tabla_sil.style.format("{:.4f}"))

mejor_sil = max(CRITERIOS, key=lambda c: siluetas[c][k])
mejor_ccc = max(CRITERIOS, key=lambda c: ccc[c])
st.info(
    f"Con k = {k}, la mayor silueta es de **{mejor_sil}** ({siluetas[mejor_sil][k]:.4f}). "
    f"La mayor correlación cofenética es de **{mejor_ccc}** ({ccc[mejor_ccc]:.4f})."
)

st.subheader("Dendrogramas")
pestanas = st.tabs(CRITERIOS)
for pestana, criterio in zip(pestanas, CRITERIOS):
    with pestana:
        fig = dibujar_dendrograma(fusiones[criterio], etiquetas, f"{criterio} linkage - {base}")
        st.pyplot(fig)

        grupos = {}
        for i, e in enumerate(cortar(fusiones[criterio], n, k)):
            grupos.setdefault(e, []).append(i)
        st.markdown(f"**Grupos al cortar en k = {k}**")
        for numero, miembros in enumerate(grupos.values(), 1):
            nombres = "; ".join(f"A{i + 1}" for i in miembros)
            st.write(f"Grupo {numero} ({len(miembros)} artículos): {nombres}")

with st.expander("Equivalencia de etiquetas"):
    for e, t in zip(etiquetas, titulos):
        st.write(f"{e}: {t}")