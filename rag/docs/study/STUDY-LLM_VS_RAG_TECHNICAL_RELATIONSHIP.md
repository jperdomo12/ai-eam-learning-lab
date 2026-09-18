# LLM vs. RAG — Cómo se relacionan técnicamente

> **Subtítulo:** Conceptos compartidos, diferencias fundamentales y flujo de trabajo.
>
> **Tipo:** Nota de estudio del AI-EAM Learning Lab  
> **Estado:** 📘 CONSOLIDADO — referencia de apoyo; Learning Lab congelado  
> **Fecha:** 2026-09-13

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-18 | Auditoría final: se añade Resumen de contenido, se actualiza la secuencia del Lab hasta Paso 12 y el estudio queda consolidado como referencia durante el estado congelado. |
| 2026-09-13 | Se reorganiza la nota dentro de `rag/docs/study/` para separar claramente el material pedagógico de la documentación canónica del laboratorio. |
| 2026-09-13 | Creación inicial. Se comparan entrenamiento e inferencia de LLM con adquisición, chunking, retrieval y generación en RAG; se identifican los conceptos técnicos compartidos y las diferencias fundamentales. |

---

## 🧭 Resumen de contenido

| Punto | Contenido |
|---|---|
| **1. Comparación** | Define qué es LLM y qué es RAG antes de relacionarlos. |
| **2. Modelo de LLM** | Resume entrenamiento e inferencia del modelo de lenguaje. |
| **3. Modelo de RAG** | Separa preparación del conocimiento y consulta en tiempo de ejecución. |
| **4. Conceptos compartidos** | Compara tokens, vectores, embeddings y representaciones sin confundir sus usos. |
| **5. Diferencias** | Contrasta pesos aprendidos, conocimiento externo, actualización y trazabilidad. |
| **6. Texto → vectores** | Explica el puente técnico común de las representaciones numéricas. |
| **7. Attention vs. similitud vectorial** | Aclara que relacionar tokens dentro del contexto no es retrieval. |
| **8. Ejemplo EAM** | Aplica LLM + RAG + capacidades externas a IBM Maximo. |
| **9. Relación con el Lab** | Sitúa el estudio dentro de la secuencia completa de Pasos 01–12. |
| **10. Resumen** | Condensa el papel de LLM y RAG para recordar. |
| **11. No confundir** | Enumera errores conceptuales frecuentes. |

---

## 1. Qué estamos comparando

Un **LLM** y un sistema **RAG** no son tecnologías equivalentes ni competidoras.

- Un **LLM** es un modelo generativo entrenado para procesar y generar lenguaje.
- **RAG (Retrieval-Augmented Generation)** es un patrón de arquitectura que recupera conocimiento externo y lo entrega al modelo generativo como contexto en el momento de responder.

Modelo mental inicial:

```text
LLM
→ aprende patrones durante el entrenamiento
→ genera durante la inferencia

RAG
→ recupera conocimiento externo cuando se necesita
→ lo incorpora al contexto
→ utiliza un LLM para generar la respuesta
```

La relación más importante es, por tanto:

> **RAG normalmente utiliza un LLM; no lo sustituye ni lo reentrena.**

---

## 2. Modelo técnico simplificado de un LLM

Conviene separar dos momentos distintos: **creación/entrenamiento** y **ejecución/inferencia**.

### 2.1 Entrenamiento

De forma muy simplificada:

```text
GRANDES CORPUS DE TEXTO
        ↓
tokenización
        ↓
secuencias de tokens
        ↓
modelo Transformer
        ↓
predicción
        ↓
error / loss
        ↓
backpropagation
        ↓
optimización / gradient descent
        ↓
actualización de parámetros
        ↓
MODELO ENTRENADO
```

Durante este proceso el modelo ajusta una gran cantidad de **parámetros o pesos**. El conocimiento no queda almacenado como una biblioteca de documentos consultables, sino distribuido estadísticamente en esos parámetros.

### 2.2 Inferencia

Cuando el modelo ya está entrenado:

```text
PROMPT
  ↓
tokens
  ↓
modelo entrenado
  ↓
predicción del siguiente token
  ↓
repetición
  ↓
RESPUESTA
```

Aquí ya no estamos entrenando el modelo. Estamos utilizando sus parámetros existentes para generar una salida.

---

## 3. Modelo técnico simplificado de RAG

En RAG también conviene separar dos momentos: **preparación/indexación** y **consulta**.

### 3.1 Preparación de conocimiento

```text
DOCUMENTOS
   ↓
adquisición / acceso
   ↓
extracción y normalización
   ↓
chunking
   ↓
representación para búsqueda
   ↓
índice
```

Una implementación semántica típica añade:

```text
CHUNK
  ↓
modelo de embeddings
  ↓
VECTOR
  ↓
vector store / índice
```

Pero RAG no exige siempre embeddings: puede utilizar retrieval léxico, semántico, híbrido u otras estrategias.

### 3.2 Consulta

```text
PREGUNTA
   ↓
retrieval
   ↓
chunks relevantes
   ↓
pregunta + contexto recuperado
   ↓
LLM
   ↓
RESPUESTA FUNDAMENTADA
```

La diferencia esencial respecto al entrenamiento de un LLM es que **los documentos continúan fuera del modelo**.

---

## 4. Qué conceptos técnicos comparten

LLM y RAG se relacionan porque utilizan varias ideas comunes del procesamiento moderno de lenguaje.

| Concepto | En un LLM | En RAG | Relación |
|---|---|---|---|
| **Tokenización** | Convierte texto en tokens para el modelo | Se usa al procesar consultas y textos dentro de modelos de embeddings/LLM | Mismo principio básico |
| **Vectores** | El modelo representa información numéricamente | Preguntas y chunks pueden representarse como vectores | Base matemática común |
| **Embeddings** | Existen representaciones internas de tokens y estados | Se usan embeddings de textos/chunks para retrieval semántico | Idea relacionada, uso distinto |
| **Transformers** | Arquitectura dominante de los LLM modernos | Muchos modelos de embeddings también utilizan Transformers | Tecnología compartida frecuente |
| **Similitud / productos vectoriales** | Se usan internamente en mecanismos como attention | Se usan explícitamente para comparar pregunta y chunks | Matemática relacionada, no el mismo algoritmo |
| **Segmentación de texto** | El entrenamiento/inferencia trabaja con secuencias y ventanas limitadas | Los documentos se dividen en chunks recuperables | Necesidad parecida, objetivo distinto |
| **Inferencia** | El LLM genera la respuesta | El LLM de un pipeline RAG genera usando contexto recuperado | Es la misma fase generativa del modelo |

### Aclaración importante sobre embeddings

La palabra **embedding** aparece en ambos mundos, pero no significa exactamente la misma pieza.

En un LLM existen representaciones internas de tokens y estados del modelo. En RAG suele utilizarse un **modelo de embeddings** diseñado para convertir textos completos —por ejemplo una pregunta o un chunk— en un vector que facilite medir similitud semántica.

Por tanto:

```text
embedding interno del LLM
≠ necesariamente
embedding usado por el retriever RAG
```

Comparten la idea de representar información mediante vectores, pero su función concreta puede ser distinta.

---

## 5. Diferencias fundamentales

| Tema | LLM | RAG |
|---|---|---|
| **Objetivo principal** | Aprender patrones y generar lenguaje | Recuperar conocimiento externo relevante antes de generar |
| **Dónde reside el conocimiento** | Distribuido en los parámetros del modelo | Documentos, chunks, metadatos e índices externos |
| **Para incorporar un documento nuevo** | El modelo no lo aprende automáticamente | Puede añadirse/reindexarse sin reentrenar el LLM |
| **Backpropagation / gradient descent** | Fundamental durante entrenamiento | No forman parte del RAG básico |
| **Chunks** | No son la unidad conceptual principal del modelo | Son normalmente unidades recuperables de conocimiento |
| **Vector store** | No es requisito para crear/ejecutar un LLM | Es común en RAG semántico, aunque no obligatorio |
| **Actualización de conocimiento** | Puede requerir nuevo entrenamiento, fine-tuning o contexto externo | Se actualiza modificando/reindexando las fuentes |
| **Trazabilidad documental** | Difícil atribuir una respuesta a un documento de entrenamiento concreto | Puede conservar fuente, sección, revisión y metadata |
| **Uso de información privada** | No la conoce salvo que haya sido entrenado o la reciba como contexto | Puede recuperarla desde repositorios autorizados en tiempo de consulta |

La frase de aprendizaje más útil es:

```text
ENTRENAMIENTO DEL LLM
"Aprende patrones a partir de estos datos"

RAG
"Busca la evidencia relevante cuando la necesites"
```

---

## 6. El puente técnico principal: texto → vectores

Una conexión muy importante entre ambos mundos es que los sistemas modernos convierten el lenguaje en representaciones numéricas.

Conceptualmente:

```text
TEXTO
  ↓
representación numérica
  ↓
VECTORES
  ↓
operaciones matemáticas
```

En RAG semántico podemos tener:

```text
"procedimiento para calibrar PT-201"
        ↓
embedding
        ↓
[0.21, -0.54, 0.76, ...]
```

Y una pregunta:

```text
"¿cómo ajusto el transmisor de presión?"
        ↓
embedding
        ↓
[0.19, -0.51, 0.79, ...]
```

Aunque las palabras sean diferentes, los vectores pueden resultar cercanos si el modelo de embeddings considera que los textos tienen significado similar.

Esto permite pasar de:

```text
búsqueda por palabras iguales
```

hacia:

```text
búsqueda por similitud de significado
```

---

## 7. Attention y similitud vectorial: relacionados, pero no iguales

Existe una relación conceptual que puede inducir a confusión.

Los Transformers utilizan operaciones entre vectores para calcular **attention** y decidir qué elementos de una secuencia se relacionan entre sí. Un retriever semántico también compara vectores para decidir qué chunks son más próximos a una pregunta.

Sin embargo:

```text
attention dentro de un Transformer
≠
retrieval sobre un vector store
```

Ambos utilizan matemáticas vectoriales, pero tienen objetivos, datos y mecanismos diferentes.

---

## 8. Ejemplo EAM / IBM Maximo

Supongamos la pregunta:

```text
La bomba P-102 presenta alta temperatura.
¿Qué trabajo está abierto y qué indica el manual que debo revisar?
```

Podemos separar las responsabilidades:

```text
MCP / integración con Maximo
→ datos operacionales actuales
→ activo, OTs, historial, mediciones

RAG
→ conocimiento documental
→ manuales, procedimientos, troubleshooting

LLM
→ recibe los hechos + conocimiento recuperado
→ razona y genera una respuesta integrada
```

Modelo conceptual:

```text
                 LLM
                  │
        ┌─────────┴─────────┐
        ↓                   ↓
       RAG                 MCP
conocimiento documental   sistemas/datos/acciones
        ↓                   ↓
manuales y procedimientos   IBM Maximo
        └─────────┬─────────┘
                  ↓
          respuesta / acción
```

Esto muestra por qué LLM, RAG y MCP son complementarios, no sustitutos.

---

## 9. Relación con nuestro RAG Learning Lab

La secuencia completa finalmente verificada fue:

```text
01 descubrir documentos
02 leer / chunking
03 retrieval léxico
04 retrieval semántico
05 índice vectorial
06 contexto fundamentado
07 evaluación de retrieval
08 generación / abstención / prompts
09 Maximo simulado + Doclinks
10 contexto EAM → RAG
11 datos transaccionales + RAG
12 Tools/MCP + EAM + RAG
```

La intención pedagógica se mantuvo constante: comprender cada mecanismo antes de introducir capas que lo oculten.

Los Pasos 01–12 están cerrados y este estudio no representa trabajo pendiente.

---

## 10. Resumen para recordar

```text
LLM
→ modelo entrenado
→ conocimiento distribuido en parámetros
→ genera lenguaje durante inferencia

RAG
→ conocimiento externo
→ lo divide y organiza para poder recuperarlo
→ selecciona evidencia relevante
→ la entrega al LLM durante inferencia
```

Tres conceptos forman el puente técnico más visible entre ambos mundos:

```text
Tokenización
     ↓
Vectores / embeddings
     ↓
Transformers y modelos de lenguaje
```

Y la diferencia fundamental sigue siendo:

> **El entrenamiento modifica el modelo; RAG normalmente modifica o consulta el contexto externo, no los pesos del LLM.**

---

## 11. Ideas que no deben confundirse

- **RAG no es un LLM.**
- **RAG no implica reentrenamiento.**
- **Embeddings no son exclusivos de RAG.**
- **RAG puede existir sin vector database**, por ejemplo con retrieval léxico o híbrido.
- **Un vector store no contiene “inteligencia” por sí mismo**: organiza representaciones para facilitar recuperación.
- **Que un chunk sea recuperado no garantiza que sea correcto o suficiente**; por eso la evaluación forma parte del diseño RAG.
- **LLM + RAG no elimina automáticamente las alucinaciones**; mejora el grounding cuando retrieval, contexto y generación están bien diseñados.
