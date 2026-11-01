from matching.booyer_moore import boyer_moore, preprocesar as preprocesar_bm
from matching.kpm import kmp, tabla_prefijos
from matching.rabin_karp import preprocesar as preprocesar_rk, rabin_karp

# nombre -> (función de preprocesamiento, función de búsqueda)
ALGORITMOS_BUSQUEDA = {
    "KMP": (tabla_prefijos, kmp),
    "Boyer-Moore": (preprocesar_bm, boyer_moore),
    "Rabin-Karp": (preprocesar_rk, rabin_karp),
}