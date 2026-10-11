# Analisis textual
Se realiza un proyecto para el analisis textual de textos cientificos de IA generativa donde  se buscaran encontrar similitud textual y patrones entre los diferentes documentos analizados por medio de tecnicas o algoritmos clasicos y modelos basados en IA

# Requerimiento 1: Análisis de Similitud Textual (Enfoques Clásicos e Inteligencia Artificial)
La aplicación deberá permitir la selección dinámica de dos o más artículos científicos del corpus para
extraer sus respectivos abstracts y someterlos a un análisis comparativo de similitud textual. Para
ello, es necesaria la implementación y el análisis de los siguientes algoritmos:

Algoritmos Clásicos (4 algoritmos): Se deben construir cuatro algoritmos tradicionales de similitud.
Se sugiere implementar una combinación de enfoques basados en programación dinámica y
modelos de espacio vectorial. Por ejemplo:
• Basados en Distancia de Edición: Algoritmo de Levenshtein o Needleman-Wunsch.
• Basados en Vectorización y Conjuntos: Similitud del Coseno (usando TF-IDF) y Coeficiente
de Jaccard.
Modelos basados en Inteligencia Artificial (2 algoritmos): Se deben implementar dos enfoques de
similitud apoyados en la generación de embeddings (representaciones vectoriales densas). Los
estudiantes pueden utilizar modelos preentrenados (por ejemplo, Word2Vec, FastText o modelos de
lenguaje a través de APIs/librerías) para vectorizar los abstracts y, posteriormente, calcular la
similitud métrica (distancia euclidiana o coseno) entre dichos vectores.
Análisis algorítmico y matemático (documentación requerida): El análisis de cada algoritmo
implementado se debe presentar en el documento técnico (por escrito) un caso de estudio práctico.
Específicamente se requiere:
• Caso de análisis concreto: Seleccionar dos abstracts específicos de los artículos
proporcionados.
• Demostración paso a paso: Utilizando los dos abstracts seleccionados, demostrar de forma
detallada cómo funciona matemáticamente cada algoritmo, por ejemplo el llenado de la
matriz en programación dinámica o el cálculo de los pesos y el ángulo en la similitud del
coseno.
• Análisis crítico: Comparar los resultados de similitud obtenidos empíricamente por los
algoritmos clásicos frente a los modelos de IA para ese mismo caso de estudio.
# Requerimiento 2: Agrupamiento Jerárquico (Clustering)
Implementar tres algoritmos de agrupamiento jerárquico para construir un árbol (dendrograma) que
represente la similitud entre los abstracts científicos extraídos de los 20 documentos PDF. Para llegar
a este resultado, se debe realizar un preprocesamiento del texto (transformar el abstract), el cálculo
de la similitud, la aplicación de clustering y la representación mediante un dendrograma.
Análisis algorítmico y matemático (documentación requerida):
• Es necesario determinar cuál de los algoritmos produce agrupamientos más coherentes.
Esta coherencia debe sustentarse mediante la aplicación de una métrica matemática de
evaluación interna.
• Aplicación de Clustering: Implementar desde cero tres criterios distintos de agrupamiento
jerárquico (por ejemplo: Single Linkage, Complete Linkage y Average Linkage o Ward).
• Representación Visual: Construir el dendrograma correspondiente para cada uno de los tres
algoritmos ejecutados.
