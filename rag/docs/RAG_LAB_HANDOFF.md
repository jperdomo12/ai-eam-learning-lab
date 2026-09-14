# 🔄 RAG LAB — HandOff

> 🎯 **Propósito:** permitir retomar rápidamente el trabajo del frente RAG sin reconstruir chats anteriores ni duplicar la documentación canónica.
>
> 📍 **Estado:** ✅ **RAG BÁSICO CERRADO / VERIFICADO**
>
> 🗓️ **Actualizado:** 2026-09-14
>
> 📘 **Documento canónico:** [`RAG_LIVING_DOCUMENTATION.md`](RAG_LIVING_DOCUMENTATION.md)

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-14 | Creación del HandOff al cierre de los Pasos 01–08 y transición hacia aplicación EAM / Maximo simulado / doclinks. |

## 1. Dónde estamos

La fase de **RAG básico** está cerrada para el nivel actual de aprendizaje.

Se verificó el flujo completo:

```text
documentos locales
→ lectura / chunking
→ embeddings
→ índice persistente
→ retrieval
→ Top-k
→ contexto fundamentado
→ Modelo (LLM)
→ respuesta
```

También se verificaron evaluación de retrieval, generación fundamentada, abstención cuando falta evidencia y control reproducible de dos variantes de prompt.

---

## 2. Qué quedó cerrado

```text
Paso 01 → descubrimiento de documentos                ✅
Paso 02 → lectura y chunking                           ✅
Paso 03 → retrieval léxico                            ✅
Paso 04 → retrieval semántico                         ✅
Paso 05 → índice vectorial persistente                ✅
Paso 06 → contexto fundamentado                       ✅
Paso 07 → evaluación de retrieval / Top-k             ✅
Paso 08 → generación fundamentada / evaluación        ✅
```

Lecciones que deben conservarse:

```text
RAG recupera evidencia; no reentrena al LLM.
Embeddings localizan chunks; el LLM recibe texto original.
Similarity ≠ confianza / answerability.
Top-k encontrado ≠ respuesta encontrada.
Retrieval correcto ≠ generación necesariamente completa.
El prompt influye en cómo el LLM utiliza la evidencia.
Sin evidencia suficiente, el sistema debe abstenerse.
Retrieval y backend generativo están desacoplados.
```

---

## 3. Baseline pedagógica utilizada

```text
Embeddings: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
Índice:     NumPy + JSON
Top-k:      4 para la evaluación de generación
Runtime:    Ollama 0.34.0
Modelo:     llama3:latest — Llama 3 8B Q4_0
```

Estas elecciones corresponden al Learning Lab y **no son decisiones de arquitectura del producto AI-EAM-MAXIMO**.

---

## 4. Documentos y artefactos relevantes

Leer primero:

```text
1. rag/README.md
2. rag/docs/RAG_LAB_FAST_READING.md
3. rag/docs/RAG_LIVING_DOCUMENTATION.md
```

Consultar después según necesidad:

```text
rag/docs/LAB-STEP08_GENERATION_EVALUATION.md
rag/docs/study/STUDY-RAG_CORE_CONCEPTS.md
rag/docs/study/STUDY-LLM_VS_RAG_TECHNICAL_RELATIONSHIP.md
rag/data/evaluation_cases.json
rag/data/source_documents/
rag/src/
```

---

## 5. Qué NO continuar ahora

No reabrir por defecto investigación sobre:

```text
reranking
hybrid retrieval
threshold tuning
RAGAS
LLM-as-judge
auto-evaluadores avanzados
otros modelos por comparación exploratoria
vector databases productivas
prompt tuning adicional
```

Solo profundizar si una necesidad concreta de EAM / IBM Maximo lo justifica.

---

## 6. Seguridad / APIs

Durante el Paso 08 se intentó una ruta de generación mediante OpenAI Responses API. El proveedor fue alcanzado, pero no se generó respuesta por falta de crédito independiente.

Las claves utilizadas para esa prueba fueron eliminadas/revocadas y no deben recuperarse ni documentarse en el repositorio.

La ruta adoptada para cerrar el LAB fue generación local con Ollama + Llama 3.

---

## 7. Relación con MCP

Mantener la separación conceptual:

```text
MCP
→ acceso a sistemas, datos y acciones

RAG
→ conocimiento documental
```

La combinación futura prevista es:

```text
IBM Maximo / MCP
→ identifica contexto EAM actual

RAG
→ recupera conocimiento de documentación asociada

Modelo (LLM) / agente
→ integra la evidencia
```

---

## 8. Siguiente bloque aprobado

El siguiente trabajo no es profundizar RAG, sino aplicarlo a EAM:

```text
IBM Maximo simulado
→ asset / site
→ metadata de documentos / doclinks
→ localizar documento asociado
→ aplicar el RAG ya aprendido
→ generar respuesta fundamentada
```

Pregunta de ejemplo:

```text
Estoy trabajando sobre PT-201 en PLANTA1.
¿Cómo debo calibrarlo según la documentación asociada al activo?
```

La simulación debe modelar el concepto de Maximo/doclinks sin afirmar todavía una implementación real o conexión viva a Maximo.

---

## 9. Regla de continuidad

Cuando se retome RAG:

```text
README
→ Fast Reading
→ Living Documentation
→ código / documentos específicos solo si hacen falta
```

No reconstruir pasos ya cerrados ni convertir experimentos del Learning Lab en decisiones de AI-EAM-MAXIMO sin revisión explícita.
