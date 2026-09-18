# 📚 RAG — Retrieval-Augmented Generation

> 🎯 **Objetivo:** aprender RAG de forma práctica con foco EAM / IBM Maximo.
>
> 📍 **Estado:** ✅ **RAG BÁSICO VERIFICADO / CERRADO** · ✅ **Aplicación EAM verificada hasta Paso 12**
>
> 🗓️ **Actualizado:** 2026-09-18

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-18 | Auditoría de continuidad: Fast Reading, Living Documentation y HandOff quedan alineados con Pasos 01–12 para poder retomar desde GitHub sin reconstruir chats anteriores. |
| 2026-09-17 | ✅ Se verifica el **Paso 12**: Cline reconoce `eam-rag-lab` con 2 Tools, valida individualmente la Tool transaccional y la Tool RAG, y finalmente selecciona e invoca ambas para una pregunta integrada. |
| 2026-09-17 | Se resuelve la incidencia de carga de embeddings del Paso 12 usando MiniLM desde caché local (`local_files_only=True`); se evita seguir aumentando timeouts y se mantiene publicación inmediata de Tools. |
| 2026-09-16 | Se prepara el **Paso 12**: las capacidades transaccional y documental/RAG pasan a exponerse como dos Tools en un MCP Server independiente (`eam-rag-lab`) para validación con Cline. El MCP Lab histórico permanece cerrado/congelado. |
| 2026-09-16 | ✅ Se verifica localmente el **Paso 11**: `WORKORDER` aporta datos transaccionales exactos, `Doclinks → RAG` aporta conocimiento documental y Llama 3 integra ambos. |
| 2026-09-16 | ✅ Se verifica localmente el **Paso 10**: `contexto EAM → Doclinks → documentos asociados → retrieval limitado → LLM`. |
| 2026-09-15 | ✅ Se verifica localmente el **Paso 09**: `PT-201 / PLANTA1 → ASSET → DOCLINKS → DOCINFO → archivos asociados`. |
| 2026-09-14 | Se inicia el bloque de aplicación EAM documentando cómo Maximo representa attachments mediante `DOCINFO` + `DOCLINKS`. |
| 2026-09-14 | Se completa el cierre documental del RAG básico. |
| 2026-09-14 | Se cierran los Pasos 01–08: retrieval, contexto, generación fundamentada, abstención y control reproducible de prompts. |
| 2026-09-12 | Inicio formal del RAG Learning Lab. |

## 📚 Por dónde empezar

1. [`docs/RAG_LAB_FAST_READING.md`](docs/RAG_LAB_FAST_READING.md) — resumen final de lectura rápida.
2. [`docs/RAG_LIVING_DOCUMENTATION.md`](docs/RAG_LIVING_DOCUMENTATION.md) — documentación canónica y evolutiva.
3. [`docs/RAG_LAB_HANDOFF.md`](docs/RAG_LAB_HANDOFF.md) — continuidad operativa vigente hasta el cierre del Paso 12.
4. [`docs/study/STUDY-MAXIMO_DOCLINKS_DATA_MODEL.md`](docs/study/STUDY-MAXIMO_DOCLINKS_DATA_MODEL.md) — base conceptual de Maximo Doclinks.
5. [`docs/LAB-STEP09_MAXIMO_DOCLINKS_SIMULATION.md`](docs/LAB-STEP09_MAXIMO_DOCLINKS_SIMULATION.md) — resolver documentos desde contexto EAM simulado.
6. [`docs/LAB-STEP10_EAM_CONTEXT_TO_RAG.md`](docs/LAB-STEP10_EAM_CONTEXT_TO_RAG.md) — limitar RAG a documentos resueltos por contexto EAM.
7. [`docs/LAB-STEP11_TRANSACTIONAL_PLUS_RAG.md`](docs/LAB-STEP11_TRANSACTIONAL_PLUS_RAG.md) — combinar OTs estructuradas con conocimiento documental RAG.
8. [`docs/LAB-STEP12_MCP_TOOLS_EAM_RAG.md`](docs/LAB-STEP12_MCP_TOOLS_EAM_RAG.md) — exponer capacidades EAM/RAG como Tools MCP y componerlas desde Cline.
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
→ PROMPT / HOST LLM
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
Tools/MCP + EAM + RAG            ✅ Paso 12
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
Datos estructurados/transaccionales y RAG documental son rutas distintas.
MCP puede exponer ambas como Tools independientes.
El Host/LLM puede seleccionar e invocar las Tools necesarias y combinar resultados.
```

## 🧪 Baseline pedagógica

```text
Embeddings: MiniLM multilingual
Índice:     NumPy + JSON para Pasos 05–08
Top-k:      4 como baseline pedagógica
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

Los Pasos 09–11 reutilizaron conceptos del MCP Lab pero no ejecutaron MCP. El Paso 12 introdujo un **MCP Server de integración bajo `rag/`**, sin modificar `mcp/src/maximo_mcp.py` ni reabrir el MCP Lab histórico.

Servidor validado:

```text
eam-rag-lab
├── consultar_ots_abiertas_activo(...)
│   → datos estructurados WORKORDER
└── buscar_documentacion_activo(...)
    → DOCLINKS / DOCINFO + retrieval RAG
```

La Tool RAG devuelve evidencia; no llama a un segundo LLM. La síntesis final corresponde al modelo usado por el Host MCP.

## 🚀 Evolución EAM aplicada

```text
Paso 09
PT-201 / PLANTA1
→ ASSET
→ DOCLINKS
→ DOCINFO
→ 2 documentos asociados

Paso 10
contexto EAM
→ documentos aplicables
→ RAG
→ LLM

Paso 11
WORKORDER estructurado + RAG documental
→ orquestación fija en Python
→ respuesta integrada

Paso 12
Tools MCP independientes
→ Host/LLM selecciona capacidades
→ Tool transaccional + Tool RAG
→ respuesta integrada
```

Resultado conceptual consolidado:

```text
DATOS ESTRUCTURADOS / TRANSACCIONALES
→ consulta estructurada / API / MCP

DOCUMENTOS / CONOCIMIENTO
→ RAG

MCP
→ expone capacidades como Tools

LLM / Host
→ selecciona, combina e interpreta
```

## ✅ Paso 12 — resultado final

Cline verificó individualmente:

```text
consultar_ots_abiertas_activo  ✅
buscar_documentacion_activo    ✅
```

y después, ante una pregunta única sin indicar qué Tool usar, seleccionó e invocó ambas:

```text
¿Tiene alguna OT abierta y qué indica su documentación
que debo revisar antes de intervenirlo?
```

Resultado:

```text
[MAXIMO]
→ 2 OTs abiertas
→ OT-PT201-01 APPR
→ OT-PT201-02 INPRG

[DOCUMENTACIÓN]
→ inspección previa
→ seguridad previa
→ procedimiento de calibración
→ seguridad específica antes de calibrar
```

La diferencia pedagógica quedó demostrada:

```text
Paso 11 → el script decide el flujo
Paso 12 → el Host/LLM decide qué Tools invocar
```

Esto demuestra **tool calling y composición dinámica mediante MCP**, no autonomía completa de un agente.

## 🚀 Siguiente decisión

El siguiente salto no se da por supuesto. Los candidatos naturales son:

```text
A. composición MCP más realista / contraste con IBM Maximo MCP oficial
B. introducir conceptos mínimos de agente sobre capacidades ya comprendidas
C. cerrar este bloque y transferir aprendizajes candidatos a AI-EAM-MAXIMO
```

No se profundizará en reranking, retrieval híbrido, thresholds, evaluación avanzada o tuning adicional salvo que una necesidad EAM concreta lo justifique.
