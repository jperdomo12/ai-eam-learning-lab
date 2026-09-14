# 📚 RAG — Retrieval-Augmented Generation

> 🎯 **Objetivo:** aprender RAG de forma práctica con foco EAM / IBM Maximo, entendiendo el mecanismo básico y su aplicación antes de introducir arquitecturas o frameworks más avanzados.
>
> 📍 **Estado:** ✅ **RAG BÁSICO VERIFICADO — siguiente bloque: simulación Maximo / doclinks**
>
> 🗓️ **Actualizado:** 2026-09-14

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-14 | ✅ Se cierra la fase de **RAG básico (Pasos 01–08)**. La generación local con `Ollama + llama3:latest` verifica respuesta fundamentada y abstención ante evidencia inexistente. El control reproducible 08C confirma que un prompt orientado a cobertura mejora `completeness` manteniendo fijo retrieval, contexto, modelo y parámetros. Se decide no profundizar ahora en optimizaciones adicionales y avanzar hacia aplicación EAM / Maximo simulado. |
| 2026-09-14 | ♻️ Se reutiliza `Ollama 0.34.0` + `llama3:latest` ya instalados. La ruta OpenAI API se abandona para este LAB al requerir crédito independiente de ChatGPT Plus. |
| 2026-09-13 | ✅ Se verifican retrieval semántico, índice persistente, contexto fundamentado y evaluación A–D con sensibilidad a `Top-k`. |
| 2026-09-12 | ✅ Se verifican fuente local, lectura/chunking y retrieval léxico. |
| 2026-09-12 | Inicio formal del RAG Learning Lab. |

## 🎯 Pregunta guía

```text
¿Cómo calibro este equipo según su manual?
```

## 🧠 Pipeline comprendido y probado

```text
DOCUMENTOS
   ↓
CHUNKING
   ↓
EMBEDDINGS / ÍNDICE
   ↓
PREGUNTA
   ↓
RETRIEVAL
   ↓
TOP-K
   ↓
TEXTO ORIGINAL + PROCEDENCIA
   ↓
PROMPT FUNDAMENTADO
   ↓
LLM
   ↓
RESPUESTA
```

## ✅ Qué quedó verificado

```text
Fuente local / adquisición       ✅
Chunking visible                 ✅
Retrieval léxico                 ✅
Embeddings / retrieval semántico ✅
Índice persistente mínimo        ✅
Contexto fundamentado            ✅
Evaluación retrieval A–D         ✅
Generación fundamentada          ✅
Abstención                       ✅ caso probado
Control reproducible de prompts  ✅
```

Aprendizajes esenciales:

```text
- RAG recupera evidencia; no reentrena al LLM.
- Los embeddings ayudan a localizar chunks; el LLM recibe texto original.
- Similarity no equivale a confianza ni a answerability.
- Top-k encontrado no significa respuesta encontrada.
- Retrieval correcto no garantiza generación completa.
- Prompt y generación deben evaluarse como capas propias.
- El sistema debe poder abstenerse cuando falta evidencia.
- Retrieval y backend generativo están desacoplados.
```

## 🧪 Baseline pedagógica utilizada

```text
Embeddings: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
Índice:     NumPy + JSON
Top-k:      4 para evaluación de generación
Runtime:    Ollama 0.34.0
LLM local:  llama3:latest — Llama 3 8B Q4_0
```

Estas elecciones son **solo del Learning Lab** y no constituyen decisiones de arquitectura de AI-EAM-MAXIMO.

## 📁 Artefactos principales

```text
rag/data/source_documents/
rag/data/evaluation_cases.json
rag/src/step01_discover_documents.py
rag/src/step02_read_and_chunk.py
rag/src/step03_lexical_retrieval.py
rag/src/step04_semantic_retrieval.py
rag/src/step04b_semantic_retrieval_content_filter.py
rag/src/step05_build_vector_index.py
rag/src/step05_query_vector_index.py
rag/src/step06_build_grounded_context.py
rag/src/step07_evaluate_retrieval_cases.py
rag/src/step07b_evaluate_topk_sensitivity.py
rag/src/step08_generate_grounded_answer.py
rag/src/step08b_generate_grounded_answer_prompt_completeness.py
rag/src/step08c_compare_prompts_deterministic.py
```

## 📚 Documentación

Documento vivo principal:

[`docs/RAG_LIVING_DOCUMENTATION.md`](docs/RAG_LIVING_DOCUMENTATION.md)

Evaluación detallada de generación:

[`docs/LAB-STEP08_GENERATION_EVALUATION.md`](docs/LAB-STEP08_GENERATION_EVALUATION.md)

Notas de estudio:

- [`docs/study/STUDY-RAG_CORE_CONCEPTS.md`](docs/study/STUDY-RAG_CORE_CONCEPTS.md)
- [`docs/study/STUDY-LLM_VS_RAG_TECHNICAL_RELATIONSHIP.md`](docs/study/STUDY-LLM_VS_RAG_TECHNICAL_RELATIONSHIP.md)

## 🔗 Relación con MCP y EAM

```text
MCP → acceso a sistemas, datos y acciones
RAG → recuperación de conocimiento documental
```

Ejemplo futuro:

```text
“La bomba B-201 presenta alta temperatura.
¿Tiene OTs abiertas y qué indica su manual que debo revisar?”

MCP / Maximo → contexto operativo / transaccional
RAG          → manuales / procedimientos
LLM          → integra la evidencia
```

## 🚀 Siguiente bloque

La fase de RAG básico queda cerrada. El siguiente objetivo es:

```text
Maximo simulado / doclinks
        ↓
contexto EAM identifica documentos asociados
        ↓
RAG procesa el documento localizado
        ↓
respuesta fundamentada
```

No se profundizará ahora en prompt tuning, otros modelos, reranking, retrieval híbrido, thresholds o evaluación avanzada salvo que una necesidad posterior lo justifique.
