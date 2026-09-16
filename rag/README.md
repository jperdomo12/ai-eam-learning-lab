# 📚 RAG — Retrieval-Augmented Generation

> 🎯 **Objetivo:** aprender RAG de forma práctica con foco EAM / IBM Maximo.
>
> 📍 **Estado:** ✅ **RAG BÁSICO VERIFICADO / CERRADO** · ✅ **Aplicación EAM verificada hasta Paso 10** · 🧪 **Paso 11 preparado: datos transaccionales + RAG**
>
> 🗓️ **Actualizado:** 2026-09-16

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-16 | Se prepara el **Paso 11**: `WORKORDER` simulado + consulta estructurada de OTs abiertas + `Doclinks → RAG` + combinación final mediante LLM. Se reutilizan convenciones del MCP Lab sin modificarlo ni reabrirlo. |
| 2026-09-16 | ✅ Se verifica localmente el **Paso 10**: `contexto EAM → Doclinks → documentos asociados → retrieval limitado → LLM`. Se documenta una inconsistencia puntual del LLM sobre `as-found`/observaciones pese a existir evidencia en la FUENTE 2; no se abre nueva fase de tuning. |
| 2026-09-16 | Se prepara el **Paso 10** para integrar `contexto EAM → Doclinks → documentos asociados → retrieval semántico → LLM`. |
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
6. [`docs/LAB-STEP10_EAM_CONTEXT_TO_RAG.md`](docs/LAB-STEP10_EAM_CONTEXT_TO_RAG.md) — práctica verificada: limitar RAG a documentos resueltos por contexto EAM y generar respuesta con LLM local.
7. [`docs/LAB-STEP11_TRANSACTIONAL_PLUS_RAG.md`](docs/LAB-STEP11_TRANSACTIONAL_PLUS_RAG.md) — práctica actual: combinar OTs estructuradas con conocimiento documental RAG.
8. [`docs/LAB-STEP08_GENERATION_EVALUATION.md`](docs/LAB-STEP08_GENERATION_EVALUATION.md) — evaluación detallada del Paso 08.
9. [`docs/study/`](docs/study/) — otras notas pedagógicas.

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
Integración EAM → RAG → LLM      ✅ Paso 10
Datos transaccionales + RAG      🧪 Paso 11 preparado
```

Aprendizajes esenciales:

```text
RAG recupera evidencia; no reentrena al LLM.
Los embeddings localizan chunks; el LLM recibe texto original.
Similarity ≠ confianza / answerability.
Top-k encontrado ≠ respuesta encontrada.
Retrieval correcto ≠ generación necesariamente completa/correcta.
Sin evidencia suficiente → abstención.
Maximo/Doclinks determina qué documentos corresponden al contexto EAM.
El contexto EAM puede reducir el universo documental antes del retrieval.
Datos estructurados/transaccionales y RAG documental son rutas distintas que pueden combinarse en el LLM.
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

El Paso 11 reutiliza nombres/campos y estados ya conocidos del MCP Lab, pero no ejecuta MCP ni modifica el laboratorio MCP cerrado.

## 🚀 Estado del bloque Maximo simulado + Doclinks + RAG

La base conceptual queda:

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

El Paso 10 verificó:

```text
contexto EAM
→ documentos permitidos por Maximo simulado
→ chunking / embeddings solo sobre esos documentos
→ retrieval semántico
→ contexto fundamentado
→ Llama 3 vía Ollama
→ respuesta
```

Resultado conceptual consolidado:

```text
MAXIMO / EAM
→ determina QUÉ documentos aplican

RAG
→ determina QUÉ evidencia dentro de esos documentos responde la pregunta

LLM
→ interpreta y redacta
```

Se observó una inconsistencia puntual del LLM: negó evidencia sobre `as-found` y observaciones aunque la FUENTE 2 sí las contenía. Se conserva como aprendizaje de generación y no se continúa con tuning adicional en esta etapa.

## 🚀 Paso 11 — datos transaccionales + RAG

El incremento preparado separa explícitamente dos rutas:

```text
WORKORDER mock
→ filtro estructurado por ASSETNUM / SITEID / STATUS
→ OTs abiertas
             \
              → LLM
             /
DOCLINKS / DOCINFO
→ documentos del activo
→ RAG
→ evidencia documental
```

Pregunta objetivo:

```text
¿Tiene el PT-201 alguna OT abierta y qué indica su documentación
que debo revisar antes de intervenirlo?
```

La orquestación sigue siendo fija y visible en código. Todavía no hay agente ni MCP activo.

No se profundizará ahora en reranking, retrieval híbrido, thresholds, evaluación avanzada o tuning adicional salvo que una necesidad EAM concreta lo justifique.
