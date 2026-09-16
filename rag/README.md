# 📚 RAG — Retrieval-Augmented Generation

> 🎯 **Objetivo:** aprender RAG de forma práctica con foco EAM / IBM Maximo.
>
> 📍 **Estado:** ✅ **RAG BÁSICO VERIFICADO / CERRADO** · 🟨 **Aplicación EAM en curso: Maximo simulado + Doclinks + RAG**
>
> 🗓️ **Actualizado:** 2026-09-16

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-16 | Se prepara el **Paso 10** para integrar `contexto EAM → Doclinks → documentos asociados → retrieval semántico → LLM`; queda pendiente la ejecución local. |
| 2026-09-15 | ✅ Se verifica localmente el **Paso 09**: `PT-201 / PLANTA1 → ASSET → DOCLINKS → DOCINFO → archivos asociados`; ambos documentos esperados fueron localizados correctamente. |
| 2026-09-15 | Se prepara el **Paso 09** con datos simulados `ASSET + DOCLINKS + DOCINFO` y un script que resuelve los documentos asociados a `PT-201 / PLANTA1`. |
| 2026-09-14 | Se inicia el bloque de aplicación EAM documentando cómo Maximo representa attachments mediante `DOCINFO` + `DOCLINKS`; se añade `STUDY-MAXIMO_DOCLINKS_DATA_MODEL.md`. |
| 2026-09-14 | Se completa el cierre documental con `RAG_LAB_FAST_READING.md` y `RAG_LAB_HANDOFF.md`. |
| 2026-09-14 | Se cierran los Pasos 01–08: retrieval, contexto, generación fundamentada, abstención y control reproducible de prompts. |
| 2026-09-12 | Inicio formal del RAG Learning Lab. |

## 📚 Por dónde empezar

1. [`docs/RAG_LAB_FAST_READING.md`](docs/RAG_LAB_FAST_READING.md) — resumen final de lectura rápida.
2. [`docs/RAG_LIVING_DOCUMENTATION.md`](docs/RAG_LIVING_DOCUMENTATION.md) — documentación canónica y evolutiva.
3. [`docs/RAG_LAB_HANDOFF.md`](docs/RAG_LAB_HANDOFF.md) — cierre y continuidad hacia Maximo simulado / doclinks.
4. [`docs/study/STUDY-MAXIMO_DOCLINKS_DATA_MODEL.md`](docs/study/STUDY-MAXIMO_DOCLINKS_DATA_MODEL.md) — base conceptual del bloque Maximo simulado + Doclinks + RAG.
5. [`docs/LAB-STEP09_MAXIMO_DOCLINKS_SIMULATION.md`](docs/LAB-STEP09_MAXIMO_DOCLINKS_SIMULATION.md) — práctica verificada: resolver documentos desde contexto EAM simulado.
6. [`docs/LAB-STEP10_EAM_CONTEXT_TO_RAG.md`](docs/LAB-STEP10_EAM_CONTEXT_TO_RAG.md) — práctica actual: limitar el RAG a documentos resueltos por el contexto EAM.
7. [`docs/LAB-STEP08_GENERATION_EVALUATION.md`](docs/LAB-STEP08_GENERATION_EVALUATION.md) — evaluación detallada del Paso 08.
8. [`docs/study/`](docs/study/) — otras notas pedagógicas.

## 🧠 Pipeline probado

```text
DOCUMENTOS
→ CHUNKING
→ EMBEDDINGS / ÍNDICE
→ PREGUNTA
→ RETRIEVAL
→ TOP-K
→ TEXTO ORIGINAL + PROCEDENCIA
→ PROMPT FUNDAMENTADO
→ LLM
→ RESPUESTA
```

## ✅ Qué quedó verificado

```text
Fuente local / adquisición       ✅
Chunking visible                 ✅
Retrieval léxico                 ✅
Retrieval semántico              ✅
Índice persistente mínimo        ✅
Contexto fundamentado            ✅
Evaluación retrieval A–D         ✅
Generación fundamentada          ✅
Abstención                       ✅
Control reproducible de prompts  ✅
Resolución Maximo Doclinks       ✅ Paso 09
Integración EAM → RAG             🧪 Paso 10 preparado
```

Aprendizajes esenciales:

```text
RAG recupera evidencia; no reentrena al LLM.
Los embeddings localizan chunks; el LLM recibe texto original.
Similarity ≠ confianza / answerability.
Top-k encontrado ≠ respuesta encontrada.
Retrieval correcto ≠ generación necesariamente completa.
Sin evidencia suficiente → abstención.
Maximo/Doclinks determina qué documentos corresponden al contexto EAM.
```

## 🧪 Baseline pedagógica

```text
Embeddings: MiniLM multilingual
Índice:     NumPy + JSON
Top-k:      4 para evaluación de generación
Runtime:    Ollama 0.34.0
LLM local:  Llama 3 8B Q4_0
```

Estas elecciones son pedagógicas y no constituyen arquitectura aprobada de AI-EAM-MAXIMO.

## 🔗 Relación con MCP

```text
MCP → sistemas, datos y acciones
RAG → conocimiento documental
```

## 🚀 Bloque actual — Maximo simulado + Doclinks + RAG

La base conceptual ya está documentada:

```text
ASSET / WORKORDER / ...
        ↓
     DOCLINKS
        ↓
      DOCINFO
        ↓
archivo / storage / URL
```

El Paso 09 verificó:

```text
PT-201 / PLANTA1
→ ASSET
→ ASSETUID 1001 / ASSETID 2001
→ DOCLINKS
→ DOCINFO
→ 2 documentos asociados existentes
```

El Paso 10, actualmente preparado, añade:

```text
contexto EAM
→ documentos permitidos por Maximo simulado
→ chunking / embeddings solo sobre esos documentos
→ retrieval semántico
→ contexto fundamentado
→ Llama 3 vía Ollama
→ respuesta
```

En este paso los embeddings se calculan en memoria para los documentos seleccionados por Doclinks. Es una simplificación pedagógica deliberada; no reemplaza el índice persistente ni define arquitectura productiva.

No se profundizará ahora en reranking, retrieval híbrido, thresholds, evaluación avanzada o tuning adicional salvo que una necesidad EAM concreta lo justifique.
