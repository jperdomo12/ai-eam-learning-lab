# 📚 RAG — Retrieval-Augmented Generation

> 🎯 **Objetivo:** aprender RAG de forma práctica con foco EAM / IBM Maximo.
>
> 📍 **Estado:** ✅ **RAG BÁSICO VERIFICADO / CERRADO** · 🟨 **Aplicación EAM en curso: Maximo simulado + Doclinks + RAG**
>
> 🗓️ **Actualizado:** 2026-09-15

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-15 | Se prepara el **Paso 09** con datos simulados `ASSET + DOCLINKS + DOCINFO` y un script que resuelve los documentos asociados a `PT-201 / PLANTA1`; queda pendiente la ejecución local para cierre pedagógico. |
| 2026-09-14 | Se inicia el bloque de aplicación EAM documentando cómo Maximo representa attachments mediante `DOCINFO` + `DOCLINKS`; se añade `STUDY-MAXIMO_DOCLINKS_DATA_MODEL.md`. |
| 2026-09-14 | Se completa el cierre documental con `RAG_LAB_FAST_READING.md` y `RAG_LAB_HANDOFF.md`. |
| 2026-09-14 | Se cierran los Pasos 01–08: retrieval, contexto, generación fundamentada, abstención y control reproducible de prompts. |
| 2026-09-12 | Inicio formal del RAG Learning Lab. |

## 📚 Por dónde empezar

1. [`docs/RAG_LAB_FAST_READING.md`](docs/RAG_LAB_FAST_READING.md) — resumen final de lectura rápida.
2. [`docs/RAG_LIVING_DOCUMENTATION.md`](docs/RAG_LIVING_DOCUMENTATION.md) — documentación canónica y evolutiva.
3. [`docs/RAG_LAB_HANDOFF.md`](docs/RAG_LAB_HANDOFF.md) — cierre y continuidad hacia Maximo simulado / doclinks.
4. [`docs/study/STUDY-MAXIMO_DOCLINKS_DATA_MODEL.md`](docs/study/STUDY-MAXIMO_DOCLINKS_DATA_MODEL.md) — base conceptual del bloque Maximo simulado + Doclinks + RAG.
5. [`docs/LAB-STEP09_MAXIMO_DOCLINKS_SIMULATION.md`](docs/LAB-STEP09_MAXIMO_DOCLINKS_SIMULATION.md) — práctica actual: resolver documentos desde contexto EAM simulado.
6. [`docs/LAB-STEP08_GENERATION_EVALUATION.md`](docs/LAB-STEP08_GENERATION_EVALUATION.md) — evaluación detallada del Paso 08.
7. [`docs/study/`](docs/study/) — otras notas pedagógicas.

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
```

Aprendizajes esenciales:

```text
RAG recupera evidencia; no reentrena al LLM.
Los embeddings localizan chunks; el LLM recibe texto original.
Similarity ≠ confianza / answerability.
Top-k encontrado ≠ respuesta encontrada.
Retrieval correcto ≠ generación necesariamente completa.
Sin evidencia suficiente → abstención.
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

El Paso 09 ya prepara una simulación mínima:

```text
PT-201 / PLANTA1
→ ASSETUID
→ DOCLINKS
→ DOCINFO
→ localizar los documentos asociados
```

Una vez validada localmente, el siguiente incremento será:

```text
contexto EAM
→ documentos permitidos por Maximo simulado
→ RAG sobre esos documentos
→ respuesta fundamentada
```

No se profundizará ahora en reranking, retrieval híbrido, thresholds, evaluación avanzada o tuning adicional salvo que una necesidad EAM concreta lo justifique.
