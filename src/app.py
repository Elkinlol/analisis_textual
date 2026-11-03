import pandas as pd
import streamlit as st

from registro import cargar_corpus, construir_algoritmos
from similarity.matriz import matriz_similitud

st.set_page_config(page_title="Similitud textual", layout="wide")


@st.cache_resource
def cargar():
    corpus = cargar_corpus()
    return corpus, construir_algoritmos(corpus)


@st.cache_data(show_spinner=False)
def calcular(nombre, indices):
    _, algoritmos = cargar()
    representaciones, funcion, parametros = algoritmos[nombre]
    return matriz_similitud([representaciones[i] for i in indices], funcion, parametros)


def titulo_de(doc):
    return doc.get("titulo") or doc["archivo"]


def autores_texto(doc):
    autores = doc.get("autores")
    if isinstance(autores, list):
        return ", ".join(autores)
    return autores or "Sin datos"


corpus, algoritmos = cargar()
titulos = [f"{i + 1}. {titulo_de(d)}" for i, d in enumerate(corpus)]

st.title("Análisis de similitud textual")
st.caption(f"Corpus de {len(corpus)} abstracts sobre inteligencia artificial en educación.")

col_a, col_b = st.columns(2)
with col_a:
    elegidos = st.multiselect(
        "Artículos a comparar (2 o más)",
        options=list(range(len(corpus))),
        format_func=lambda i: titulos[i],
    )
with col_b:
    nombres = st.multiselect(
        "Algoritmos",
        options=list(algoritmos),
        default=list(algoritmos)[:2],
    )

if len(elegidos) < 2:
    st.info("Elige al menos 2 artículos.")
    st.stop()
if not nombres:
    st.info("Elige al menos 1 algoritmo.")
    st.stop()
if any(not (corpus[i].get("abstract") or "").strip() for i in elegidos):
    st.error("Alguno de los artículos elegidos no tiene abstract válido.")
    st.stop()

indices = tuple(elegidos)
etiquetas = [f"A{i + 1}" for i in elegidos]

with st.expander("Artículos seleccionados"):
    for i in elegidos:
        st.markdown(f"**A{i + 1}. {titulo_de(corpus[i])}**")
        st.write(f"Autores: {autores_texto(corpus[i])}")
        st.write(corpus[i]["abstract"])

with st.spinner("Calculando..."):
    matrices = {n: calcular(n, indices) for n in nombres}

if len(elegidos) == 2:
    st.subheader("Comparación entre algoritmos")
    resumen = pd.DataFrame(
        {"Similitud": [matrices[n][0][1] for n in nombres]},
        index=nombres,
    )
    st.dataframe(resumen.style.format("{:.4f}"))
    st.bar_chart(resumen)

st.subheader("Matrices de similitud")
pestanas = st.tabs(nombres)
for pestana, nombre in zip(pestanas, nombres):
    with pestana:
        df = pd.DataFrame(matrices[nombre], index=etiquetas, columns=etiquetas)
        st.dataframe(
            df.style.format("{:.4f}").background_gradient(cmap="Blues", vmin=0, vmax=1),
        )