# ⚡ RAG LAB — Fast Reading

> 🎯 **Objetivo:** recuperar en pocos minutos qué se aprendió, qué se probó y cómo quedó cerrado el laboratorio básico de RAG aplicado a EAM / IBM Maximo.
>
> 📍 **Estado:** ✅ **RAG BÁSICO CERRADO / VERIFICADO** para el nivel actual de aprendizaje.
>
> 🗓️ **Actualizado:** 2026-09-14
>
> 📘 **Documento canónico:** [`RAG_LIVING_DOCUMENTATION.md`](RAG_LIVING_DOCUMENTATION.md)

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-14 | Se incorpora la distinción práctica entre RAG documental y acceso a datos estructurados/transaccionales mediante SQL, API o MCP, incluyendo el matiz de bases de datos con soporte vectorial. |
| 2026-09-14 | Creación del resumen de recuperación rápida al cierre de los Pasos 01–08 del RAG Learning Lab. |

## 1. En una frase

Se verificó un flujo RAG básico completo que toma documentos técnicos locales, los fragmenta e indexa, recupera los fragmentos relevantes para una pregunta y entrega al LLM el **texto original recuperado** para generar una respuesta fundamentada.

Pregunta guía:

```text
¿Cómo calibro este equipo según su manual?
```

---

## 2. Arquitectura mental

```text
DOCUMENTOS
   ↓
lectura / normalización
   ↓
CHUNKING
   ↓
EMBEDDINGS / ÍNDICE

PREGUNTA
   ↓
embedding de la consulta
   ↓
RETRIEVAL
   ↓
TOP-K
   ↓
TEXTO ORIGINAL + PROCEDENCIA
   ↓
PROMPT FUNDAMENTADO
   ↓
MODELO (LLM)
   ↓
RESPUESTA
```

Idea clave:

> **Los vectores ayudan a localizar evidencia; el LLM recibe el texto original recuperado.**

---

## 3. Indexación y consulta

No son lo mismo.

```text
INDEXACIÓN / INGESTIÓN
 documentos → chunks → embeddings → índice persistente

CONSULTA
 pregunta → embedding → búsqueda/ranking → Top-k
         → texto original → contexto → LLM → respuesta
```

La indexación se repite cuando cambian los documentos; la consulta ocurre para cada pregunta.

---

## 4. Componentes usados

| Componente | Papel |
|---|---|
| Python | scripts del pipeline |
| `sentence-transformers` | embeddings |
| `paraphrase-multilingual-MiniLM-L12-v2` | modelo de embeddings |
| NumPy + JSON | índice vectorial persistente mínimo |
| Ollama 0.34.0 | runtime local de generación |
| Llama 3 8B Q4_0 | Modelo (LLM) local |

Se intentó también OpenAI Responses API, pero la generación no llegó a ejecutarse por falta de crédito independiente; no se adoptó esa ruta para el LAB.

No se utilizaron LangChain, LlamaIndex ni una base vectorial dedicada.

---

## 5. Pasos verificados

```text
01 → descubrir documentos                         ✅
02 → leer y fragmentar / chunking                 ✅
03 → retrieval léxico                             ✅
04 → retrieval semántico                          ✅
05 → índice vectorial persistente                 ✅
06 → contexto fundamentado                        ✅
07 → evaluación retrieval / sensibilidad Top-k    ✅
08 → generación y evaluación fundamentada         ✅
```

Los documentos de prueba son sintéticos y están bajo `rag/data/source_documents/`.

---

## 6. Qué aprendimos del retrieval

El retrieval léxico mostró que coincidir palabras no basta:

```text
ajustar ≈ calibrar
```

El retrieval semántico mejoró la búsqueda por significado, pero dejó una lección crítica:

```text
similarity alta ≠ confianza
similarity alta ≠ evidencia suficiente
```

Otra regla esencial:

```text
BUEN LLM + BUEN DOCUMENTO + MAL RETRIEVAL
=
MALA RESPUESTA RAG
```

---

## 7. Qué es Top-k

Después de ordenar los chunks por relevancia, `Top-k` indica cuántos de los primeros se conservan para construir el contexto.

```text
Top-k = 4
→ usar los 4 chunks mejor clasificados
```

Pero:

```text
Top-k encontrado ≠ respuesta encontrada
```

Si el dato solicitado no existe en ningún documento, el retriever igualmente devuelve los mejores candidatos disponibles.

En este LAB `k=4` quedó como **baseline pedagógica**, no como recomendación productiva.

---

## 8. Retrieval correcto no garantiza respuesta completa

En el Caso C se recuperó evidencia suficiente, pero la primera respuesta de Llama 3 omitió parte del procedimiento.

Lección:

```text
RETRIEVAL COMPLETO + CONTEXTO SUFICIENTE
≠
RESPUESTA NECESARIAMENTE COMPLETA
```

La generación debe evaluarse como una capa propia.

---

## 9. Papel del prompt

El prompt base exigía:

```text
usar solo el contexto recuperado
no inventar
informar si falta evidencia
citar fuentes
```

Una segunda variante añadió cobertura explícita de todas las partes de la pregunta. Manteniendo fijo retrieval, contexto, LLM y parámetros, esa variante produjo una respuesta sustancialmente más completa.

```text
retrieval determina QUÉ evidencia llega
prompt influye en CÓMO el LLM utiliza esa evidencia
```

---

## 10. Abstención

Se preguntó deliberadamente por un dato inexistente en los documentos: el par de apriete de los bornes del PT-201.

El sistema indicó correctamente que la evidencia disponible no contenía ese dato.

```text
sin evidencia suficiente
→ no inventar
→ abstenerse / informar la ausencia
```

---

## 11. Embeddings y LLM son capas distintas

```text
MiniLM
→ embeddings / retrieval

Llama 3
→ generación
```

El modelo de embeddings localiza evidencia. El LLM interpreta el texto recuperado y redacta la respuesta.

RAG no exige que ambos sean el mismo modelo.

---

## 12. Tokenización, Attention y RAG

```text
RAG RETRIEVAL
→ decide qué chunks externos ENTRAN en el contexto

ATTENTION
→ relaciona tokens que YA están dentro del contexto
```

Por tanto:

```text
retrieval ≠ attention
```

MiniLM y Llama 3 son modelos Transformer y realizan internamente tokenización y mecanismos de atención.

---

## 13. RAG no es Fine-tuning

```text
RAG
→ recupera conocimiento externo en tiempo de consulta
→ no modifica los pesos del LLM

Fine-tuning
→ entrenamiento adicional
→ modifica pesos
```

RAG conserva especial valor para información exacta, actualizable, privada, citable y trazable por documento/revisión.

---

## 14. Relación con MCP, bases de datos y EAM

### 14.1 Regla mental práctica

Para el alcance de este Learning Lab, la forma más útil de pensar en **RAG clásico** es:

```text
RAG "clásico"
→ recuperar conocimiento no estructurado o semiestructurado
→ documentos, PDFs, manuales, procedimientos
→ embeddings / búsqueda semántica
→ chunks
→ LLM
```

Y para una arquitectura AI-Driven EAM:

```text
DOCUMENTOS / CONOCIMIENTO
→ RAG

DATOS ESTRUCTURADOS / TRANSACCIONALES
→ SQL / API / MCP

LLM / agente
→ combina ambos cuando hace falta
```

Ejemplos de datos estructurados/transaccionales en un EAM:

```text
OTs
activos
estados
prioridades
inventario
costes
fechas
```

Una pregunta como:

```text
¿Cuántas OTs de prioridad 1 están abiertas?
```

se resuelve de forma natural consultando Maximo mediante API/MCP, no buscando chunks documentales.

En cambio:

```text
¿Qué indica el manual de la bomba B-201 sobre vibración?
```

encaja directamente en RAG documental.

### 14.2 Una base de datos también puede participar en RAG

Una base de datos puede almacenar y buscar vectores. Por ejemplo:

```text
PostgreSQL + pgvector
→ texto del chunk
→ embedding
→ metadata
→ búsqueda vectorial
```

En ese caso la base de datos participa en el **retrieval semántico** y funciona también como vector store.

Pero:

> **Que una aplicación consulte una base de datos no convierte automáticamente esa consulta en RAG.**

La misma plataforma PostgreSQL podría utilizarse simultáneamente para:

```text
SQL tradicional
→ datos estructurados exactos

pgvector
→ retrieval semántico sobre chunks / embeddings
```

### 14.3 Ejemplo combinado EAM

```text
“La bomba B-201 presenta alta temperatura.
¿Tiene OTs abiertas y qué indica su manual?”

Maximo MCP → OTs / contexto operativo
RAG        → manual / procedimiento
LLM        → respuesta integrada
```

---

## 15. Qué NO quedó decidido para producción

El LAB no determina que AI-EAM-MAXIMO deba usar MiniLM, NumPy, `Top-k=4`, Llama 3, Ollama o los prompts exactos probados.

Fueron elecciones pedagógicas para entender el mecanismo con la mínima complejidad necesaria.

---

## 16. Qué no profundizamos ahora

No se continuará ahora con reranking, retrieval híbrido, thresholds, RAGAS, LLM-as-judge, auto-evaluadores avanzados, bases vectoriales productivas ni tuning adicional, salvo que una necesidad EAM concreta lo justifique.

---

## 17. Documentación del RAG LAB

```text
rag/docs/
├── RAG_LAB_FAST_READING.md
├── RAG_LIVING_DOCUMENTATION.md
├── RAG_LAB_HANDOFF.md
├── LAB-STEP08_GENERATION_EVALUATION.md
└── study/
    ├── STUDY-RAG_CORE_CONCEPTS.md
    └── STUDY-LLM_VS_RAG_TECHNICAL_RELATIONSHIP.md
```

Orden recomendado para recuperar el tema:

```text
1. RAG_LAB_FAST_READING.md
2. RAG_LIVING_DOCUMENTATION.md
3. RAG_LAB_HANDOFF.md
4. documentos study / evaluación específica cuando hagan falta
```

---

## 18. Próximo bloque

RAG básico queda cerrado. El siguiente bloque es **aplicación EAM**:

```text
IBM Maximo simulado
→ activo / site
→ Doclinks / metadata
→ localizar documentación asociada
→ aplicar el RAG ya aprendido
→ respuesta fundamentada
```

> **Maximo identifica qué documentación corresponde al contexto EAM; RAG recupera el conocimiento dentro de esa documentación.**
