# Análisis Textual de Artículos Científicos sobre Inteligencia Artificial Generativa

## Descripción del proyecto

El proyecto consiste en desarrollar una aplicación para el análisis computacional de textos científicos relacionados con la **Inteligencia Artificial Generativa**. Su objetivo es identificar y comparar similitudes textuales y patrones entre un corpus de 20 artículos científicos en formato PDF, mediante la implementación de algoritmos clásicos y modelos basados en inteligencia artificial.

La aplicación permitirá analizar los *abstracts* de los artículos, comparar los resultados y representar visualmente las relaciones de similitud entre los documentos.

---

## Requerimiento 1: Análisis de Similitud Textual

### 1.1. Objetivo

La aplicación deberá permitir la selección dinámica de dos o más artículos científicos del corpus, extraer sus respectivos *abstracts* y realizar un análisis comparativo de similitud textual.

### 1.2. Algoritmos clásicos

Se deberán implementar **cuatro algoritmos tradicionales de similitud textual**, combinando enfoques basados en programación dinámica, teoría de conjuntos y representación vectorial.

| Enfoque | Algoritmo de referencia | Principio de funcionamiento |
|---|---|---|
| Distancia de edición | Levenshtein o Needleman-Wunsch | Mide el costo de transformar una secuencia de texto en otra. |
| Espacio vectorial | Similitud del coseno con TF-IDF | Compara la orientación de los vectores que representan los textos. |
| Teoría de conjuntos | Coeficiente de Jaccard | Compara la intersección y la unión de los términos de los textos. |
| Algoritmo adicional | Por definir | Se seleccionará un cuarto algoritmo que complemente los anteriores. |

> **Nota:** el enunciado exige cuatro algoritmos clásicos, pero solo presenta tres enfoques de referencia. Por tanto, será necesario seleccionar un cuarto algoritmo.

### 1.3. Modelos basados en inteligencia artificial

Se deberán implementar **dos enfoques de similitud basados en embeddings**, es decir, representaciones vectoriales densas que permitan capturar relaciones semánticas entre palabras y textos.

Se podrán utilizar modelos preentrenados, como Word2Vec, FastText o modelos de lenguaje disponibles mediante bibliotecas o API.

Una vez generados los embeddings de los *abstracts*, se calculará su similitud mediante métricas como:

- Similitud del coseno.
- Distancia euclidiana.

La selección de los modelos deberá justificarse teniendo en cuenta su funcionamiento, los recursos disponibles y la naturaleza del corpus.

### 1.4. Análisis algorítmico y matemático

Para cada algoritmo implementado se deberá elaborar documentación técnica que incluya los siguientes elementos:

#### Caso de estudio

Seleccionar dos artículos científicos específicos del corpus y utilizar sus *abstracts* como entrada para el análisis.

#### Demostración matemática paso a paso

Explicar detalladamente el funcionamiento de cada algoritmo utilizando el caso de estudio seleccionado. La demostración deberá incluir, según corresponda:

- Construcción y llenado de la matriz de programación dinámica.
- Cálculo de frecuencias y pesos TF-IDF.
- Representación de los textos como conjuntos o vectores.
- Cálculo de intersecciones, distancias, productos escalares o ángulos.
- Generación y comparación de embeddings.

#### Análisis crítico de resultados

Comparar los resultados obtenidos mediante los algoritmos clásicos y los modelos basados en inteligencia artificial para el mismo caso de estudio. Se deberán interpretar las diferencias y discutir las ventajas y limitaciones de cada enfoque.

---

## Requerimiento 2: Agrupamiento Jerárquico (*Clustering*)

### 2.1. Objetivo

Implementar tres algoritmos de agrupamiento jerárquico para identificar patrones y relaciones de similitud entre los *abstracts* de los 20 artículos científicos.

El resultado deberá permitir representar las relaciones entre los documentos mediante dendrogramas y determinar qué criterio de agrupamiento genera resultados más coherentes según una métrica matemática de evaluación interna.

### 2.2. Etapas del proceso

El proceso de agrupamiento deberá contemplar las siguientes etapas:

1. **Extracción de información:** obtener los *abstracts* de los 20 documentos PDF.
2. **Preprocesamiento textual:** transformar los textos para facilitar su análisis.
3. **Representación de los documentos:** convertir los textos en representaciones adecuadas para calcular similitudes o distancias.
4. **Cálculo de similitudes o distancias:** establecer las relaciones cuantitativas entre los documentos.
5. **Agrupamiento jerárquico:** ejecutar los tres criterios seleccionados.
6. **Representación visual:** construir un dendrograma para cada criterio.
7. **Evaluación y comparación:** aplicar una métrica interna para analizar la coherencia de los agrupamientos.

### 2.3. Algoritmos de agrupamiento

Se deberán implementar **desde cero tres criterios diferentes de agrupamiento jerárquico**. Entre las alternativas sugeridas se encuentran:

| Criterio | Descripción |
|---|---|
| *Single Linkage* | Define la distancia entre dos grupos mediante la menor distancia entre sus elementos. |
| *Complete Linkage* | Define la distancia entre dos grupos mediante la mayor distancia entre sus elementos. |
| *Average Linkage* | Define la distancia entre dos grupos mediante el promedio de las distancias entre sus elementos. |
| *Ward* | Selecciona las fusiones que producen el menor incremento de la variación interna, bajo las condiciones apropiadas de distancia. |

Se seleccionarán tres criterios de la lista anterior y se documentará su implementación.

### 2.4. Representación visual mediante dendrogramas

Para cada algoritmo se deberá generar un dendrograma que represente gráficamente la secuencia de fusiones de los documentos y la distancia a la que se producen.

Los dendrogramas deberán permitir observar la estructura jerárquica de los grupos y facilitar la comparación de los resultados obtenidos con cada criterio.

### 2.5. Evaluación matemática de los agrupamientos

Se deberá seleccionar y aplicar una métrica de evaluación interna para determinar cuál de los tres métodos produce agrupamientos más coherentes.

La documentación deberá incluir:

- Justificación de la métrica seleccionada.
- Explicación de su fundamento matemático.
- Cálculo e interpretación de los resultados.
- Comparación entre los tres métodos.
- Identificación de las limitaciones de la evaluación.

La conclusión deberá estar respaldada por los resultados experimentales y no únicamente por la inspección visual de los dendrogramas.

---

## Consideraciones de implementación

- El corpus estará compuesto por 20 artículos científicos en formato PDF.
- El análisis se centrará principalmente en los *abstracts*.
- Los títulos y autores se conservarán como metadatos para identificar los documentos y facilitar las consultas.
- Los algoritmos exigidos deberán implementarse de manera explícita, evitando funciones de alto nivel que resuelvan directamente el algoritmo evaluado.
- Se deberán realizar pruebas para comprobar la corrección de las implementaciones.
- Las decisiones técnicas y los resultados deberán quedar documentados para facilitar su reproducción y evaluación.
