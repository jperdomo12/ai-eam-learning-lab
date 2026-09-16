# 📚 RAG — Retrieval-Augmented Generation

> 🎯 **Objetivo:** aprender RAG de forma práctica con foco EAM / IBM Maximo.
>
> 📍 **Estado:** ✅ **RAG BÁSICO VERIFICADO / CERRADO** · ✅ **Aplicación EAM verificada hasta Paso 11** · 🧪 **Paso 12 preparado: Tools/MCP + datos EAM + RAG**
>
> 🗓️ **Actualizado:** 2026-09-16

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-16 | Se prepara el **Paso 12**: las capacidades transaccional y documental/RAG pasan a exponerse como dos Tools en un MCP Server independiente (`eam-rag-lab`) para validación con Cline. El MCP Lab histórico permanece cerrado/congelado. |
| 2026-09-16 | ✅ Se verifica localmente el **Paso 11**: `WORKORDER` aporta datos transaccionales exactos, `Doclinks → RAG` aporta conocimiento documental y Llama 3 integra ambos. Se observó una desviación menor en el formato literal de citas; no se abre tuning adicional. |
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
3. [`docs/RAG_LAB_HANDOFF.md`](docs/RAG_LAB_HANDOFF.md) — cierre y continuidad desde el RAG básico.
4. [`docs/study/STUDY-MAXIMO_DOCLINKS_DATA_MODEL.md`](docs/study/STUDY-MAXIMO_DOCLINKS_DATA_MODEL.md) — base conceptual de Maximo Doclinks.
5. [`docs/LAB-STEP09_MAXIMO_DOCLINKS_SIMULATION.md`](docs/LAB-STEP09_MAXIMO_DOCLINKS_SIMULATION.md) — práctica verificada: resolver documentos desde contexto EAM simulado.
6. [`docs/LAB-STEP10_EAM_CONTEXT_TO_RAG.md`](docs/LAB-STEP10_EAM_CONTEXT_TO_RAG.md) — práctica verificada: limitar RAG a documentos resueltos por contexto EAM.
7. [`docs/LAB-STEP11_TRANSACTIONAL_PLUS_RAG.md`](docs/LAB-STEP11_TRANSACTIONAL_PLUS_RAG.md) — práctica verificada: combinar OTs estructuradas con conocimiento documental RAG.
8. [`docs/LAB-STEP12_MCP_TOOLS_EAM_RAG.md`](docs/LAB-STEP12_MCP_TOOLS_EAM_RAG.md) — práctica actual: exponer ambas capacidades como Tools MCP y validarlas con Cline.
9. [`docs/LAB-STEP08_GENERATION_EVALUATION.md`](docs/LAB-STEP08_GENERATION_EVALUATION.md) — evaluación detallada del Paso 08.
10. [`docs/study/`](docs/study/) — otras notas pedagógicas.

## 🧠 Pipeline RAG probado

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
Datos transaccionales + RAG      ✅ Paso 11
Tools/MCP + EAM + RAG            🧪 Paso 12 preparado
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
Índice:     NumPy + JSON para Pasos 05–08
Top-k:      4 como baseline pedagógica de generación/retrieval
Runtime:    Ollama 0.34.0 en Pasos 08–11
LLM local:  Llama 3 8B Q4_0 en Pasos 08–11
MCP:        FastMCP en Paso 12
Host:       Cline para validación del Paso 12
```

Estas elecciones son pedagógicas y no constituyen arquitectura aprobada de AI-EAM-MAXIMO.

## 🔗 Relación con MCP

```text
MCP → protocolo para exponer e invocar capacidades
RAG → conocimiento documental
```

Los Pasos 09–11 reutilizaron conceptos del MCP Lab pero no ejecutaron MCP. El Paso 12 introduce un **nuevo MCP Server de integración bajo `rag/`**, sin modificar `mcp/src/maximo_mcp.py` ni reabrir el MCP Lab histórico.

El servidor preparado expone únicamente:

```text
consultar_ots_abiertas_activo(...)
→ datos estructurados WORKORDER

buscar_documentacion_activo(...)
→ DOCLINKS / DOCINFO + retrieval RAG
```

La Tool RAG devuelve evidencia; no llama a un segundo LLM. La síntesis final corresponde al modelo usado por el Host MCP.

## 🚀 Evolución EAM aplicada

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
→ retrieval semántico
→ contexto fundamentado
→ Llama 3
→ respuesta
```

El Paso 11 verificó dos rutas en paralelo:

```text
WORKORDER mock
→ filtro estructurado por ASSETNUM / SITEID / STATUS
→ 2 OTs abiertas de 3
             \
              → LLM → respuesta integrada
             /
DOCLINKS / DOCINFO
→ documentos del activo
→ RAG
→ evidencia documental
```

Resultado conceptual consolidado:

```text
DATOS ESTRUCTURADOS / TRANSACCIONALES
→ consulta estructurada / API / MCP

DOCUMENTOS / CONOCIMIENTO
→ RAG

LLM
→ combina ambos cuando hace falta
```

## 🚀 Paso 12 — orquestación mediante Tools/MCP

El nuevo incremento cambia la responsabilidad:

```text
PASO 11
script decide previamente todo el flujo

PASO 12
Cline / LLM
→ MCP Client
→ eam-rag-lab MCP Server
   ├── Tool transaccional
   └── Tool documental/RAG
→ Host LLM sintetiza
```

Servidor:

```text
rag/src/step12_eam_rag_mcp_server.py
```

Configuración Cline de ejemplo:

```text
rag/config/cline_step12_mcp_settings.example.json
```

La validación pendiente debe confirmar que Cline reconoce **2 Tools**, invoca ambas para la pregunta integrada del `PT-201 / PLANTA1` y distingue hechos `[MAXIMO]` de evidencia `[FUENTE n]`.

No se introducen todavía agentes autónomos, Maximo real, IBM Maximo MCP Server oficial ni acciones de escritura.

No se profundizará ahora en reranking, retrieval híbrido, thresholds, evaluación avanzada o tuning adicional salvo que una necesidad EAM concreta lo justifique.
