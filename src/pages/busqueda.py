import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # para encontrar registro.py

from time import perf_counter

import pandas as pd
import streamlit as st

from matching.algoritmos import ALGORITMOS_BUSQUEDA
from matching.booyer_moore import tabla_caracter_malo, tabla_sufijo_bueno
from matching.kpm import tabla_prefijos
from matching.rabin_karp import preprocesar as preprocesar_rk
from registro import cargar_corpus

st.set_page_config(page_title="Búsqueda de patrones", layout="wide")


@st.cache_resource
def cargar():
    return cargar_corpus()


def contexto(texto, posicion, largo, margen=50):
    """Fragmento del abstract con la coincidencia resaltada en negrita."""
    a = max(0, posicion - margen)
    b = min(len(texto), posicion + largo + margen)
    return (texto[a:posicion] + "**" + texto[posicion:posicion + largo] + "**"
            + texto[posicion + largo:b])


corpus = cargar()

st.title("Búsqueda de patrones en los abstracts")
st.caption("Coincidencia exacta con KMP, Boyer-Moore y Rabin-Karp implementados desde cero.")

c1, c2, c3 = st.columns([3, 2, 2])
with c1:
    patron = st.text_input("Patrón a buscar")
with c2:
    algoritmo = st.selectbox("Algoritmo", list(ALGORITMOS_BUSQUEDA))
with c3:
    distinguir = st.checkbox("Distinguir mayúsculas", value=False)

if not patron:
    st.info("Escribe un patrón para buscar.")
    st.stop()


def normalizar(texto):
    return texto if distinguir else texto.lower()


patron_n = normalizar(patron)
preprocesar, buscar = ALGORITMOS_BUSQUEDA[algoritmo]
tablas = preprocesar(patron_n)          # se calcula una sola vez para los 20 abstracts

filas, resultados = [], {}
t0 = perf_counter()
for i, d in enumerate(corpus):
    texto = normalizar(d.get("abstract") or "")
    res = buscar(texto, patron_n, tablas=tablas)
    resultados[i] = res
    filas.append({
        "Artículo": f"A{i + 1}",
        "Título": d.get("titulo") or d["archivo"],
        "Ocurrencias": len(res["posiciones"]),
        "Posiciones": ", ".join(str(p) for p in res["posiciones"][:8])
                      + (" ..." if len(res["posiciones"]) > 8 else ""),
        "Comparaciones": res["comparaciones"],
    })
t_busqueda = (perf_counter() - t0) * 1000

total = sum(f["Ocurrencias"] for f in filas)
con_resultados = sum(1 for f in filas if f["Ocurrencias"] > 0)
st.subheader("Resultados")
st.write(f"**{total}** ocurrencias de «{patron}» en **{con_resultados}** de {len(corpus)} abstracts "
         f"({algoritmo}, {t_busqueda:.2f} ms).")
st.dataframe(pd.DataFrame(filas))

if total:
    st.subheader("Contexto de las coincidencias")
    for i, d in enumerate(corpus):
        pos = resultados[i]["posiciones"]
        if not pos:
            continue
        with st.expander(f"A{i + 1}: {len(pos)} ocurrencia(s)"):
            for p in pos[:3]:
                st.markdown("…" + contexto(d["abstract"], p, len(patron)) + "…")
            if len(pos) > 3:
                st.caption(f"Se muestran 3 de {len(pos)}.")

if len(patron_n) <= 30:
    with st.expander("Estructuras auxiliares del patrón"):
        m = len(patron_n)
        lps, bueno = tabla_prefijos(patron_n), tabla_sufijo_bueno(patron_n)
        st.markdown("**KMP: tabla de prefijos π** (π[i] = prefijo más largo de patrón[0..i] que también es sufijo)")
        st.dataframe(pd.DataFrame({"i": range(m), "carácter": list(patron_n), "π[i]": lps}).set_index("i"))
        st.markdown("**Boyer-Moore: carácter malo λ(c)** (última posición de c en el patrón; los ausentes valen −1)")
        malo = tabla_caracter_malo(patron_n)
        st.dataframe(pd.DataFrame({"carácter": list(malo), "λ(c)": list(malo.values())}).set_index("carácter"))
        st.markdown("**Boyer-Moore: sufijo bueno** (bueno[j] = desplazamiento si ya coincidió patrón[j..])")
        st.dataframe(pd.DataFrame({"j": range(m + 1), "sufijo": [patron_n[j:] for j in range(m + 1)],
                                   "bueno[j]": bueno}).set_index("j"))
        hash_patron, factor = preprocesar_rk(patron_n)
        st.markdown(f"**Rabin-Karp:** H(patrón) = {hash_patron} y b^(m−1) mod q = {factor} "
                    f"(base 256, módulo 1 000 000 007)")

with st.expander("Comparación de los tres algoritmos con este patrón"):
    comparacion = []
    firmas = []
    for nombre, (pre, bus) in ALGORITMOS_BUSQUEDA.items():
        t0 = perf_counter()
        tb = pre(patron_n)
        t_pre = (perf_counter() - t0) * 1000
        t0 = perf_counter()
        res = [bus(normalizar(d.get("abstract") or ""), patron_n, tablas=tb) for d in corpus]
        t_bus = (perf_counter() - t0) * 1000
        posiciones = [r["posiciones"] for r in res]
        firmas.append(posiciones)
        comparacion.append({
            "Algoritmo": nombre,
            "Ocurrencias": sum(len(p) for p in posiciones),
            "Comparaciones de caracteres": sum(r["comparaciones"] for r in res),
            "Preprocesamiento (ms)": round(t_pre, 4),
            "Búsqueda (ms)": round(t_bus, 3),
        })
    st.dataframe(pd.DataFrame(comparacion))
    if all(f == firmas[0] for f in firmas):
        st.success("Los tres algoritmos encuentran exactamente las mismas posiciones.")
    else:
        st.error("Los algoritmos no coinciden: hay un error en alguna implementación.")
    st.caption("Con textos tan cortos los tiempos son muy pequeños y ruidosos. "
               "Para el análisis de complejidad usa: python src/cli.py benchmark")