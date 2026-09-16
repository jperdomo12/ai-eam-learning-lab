# 📘 RAG Learning Lab — Documentación viva

> 🎯 **Propósito:** conservar el conocimiento vigente, decisiones de laboratorio, resultados y aprendizajes del frente **RAG aplicado a EAM / IBM Maximo**.
>
> 📍 **Estado:** ✅ **RAG básico verificado** · ✅ **Aplicación EAM verificada hasta Paso 11** · 🧪 **Paso 12 preparado: Tools/MCP + EAM + RAG**
>
> 🗓️ **Actualizado:** 2026-09-16

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-16 | Se consolida la documentación viva hasta el **Paso 12**: Pasos 09–11 verificados y Paso 12 preparado para exponer capacidades EAM/RAG como Tools MCP en Cline. Se simplifica esta documentación canónica y se remiten los detalles experimentales a los documentos `LAB-STEP*.md`. |
| 2026-09-14 | Se consolida la distinción entre **RAG documental** y acceso a **datos estructurados/transaccionales** mediante SQL, API o MCP. |
| 2026-09-14 | ✅ Se cierra el **Paso 08 — generación fundamentada** y con ello la fase de RAG básico. |
| 2026-09-13 | ✅ Se verifican evaluación de retrieval, índice persistente y contexto fundamentado. |
| 2026-09-12 | ✅ Inicio y primeras validaciones del RAG Learning Lab. |

---

## 1. Modelo mental vigente

```text
DOCUMENTOS
   ↓
lectura / normalización
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
LLM
   ↓
RESPUESTA
```

Idea esencial:

> **RAG no reentrena al LLM; recupera evidencia relevante en tiempo de consulta y entrega el texto original al modelo.**

---

## 2. RAG documental vs. datos estructurados/transaccionales

Regla mental adoptada para AI-Driven EAM:

```text
DOCUMENTOS / CONOCIMIENTO
→ RAG

DATOS ESTRUCTURADOS / TRANSACCIONALES
→ SQL / API / MCP

LLM / agente
→ combina ambos cuando hace falta
```

Ejemplos:

```text
¿Cuántas OTs prioridad 1 están abiertas?
→ Maximo / API / MCP

¿Qué indica el manual del equipo sobre vibración?
→ RAG documental
```

Una base de datos también puede participar en RAG cuando almacena chunks, embeddings y metadata, por ejemplo `PostgreSQL + pgvector`. Eso no convierte toda consulta SQL en RAG.

---

## 3. RAG básico — Pasos 01–08

Estado:

```text
01. Descubrimiento de documentos        ✅
02. Lectura y chunking visible          ✅
03. Retrieval léxico                    ✅
04. Retrieval semántico                 ✅
05. Índice vectorial persistente        ✅
06. Contexto fundamentado               ✅
07. Evaluación de retrieval             ✅
08. Generación fundamentada             ✅
```

Baseline pedagógica utilizada:

```text
Embeddings → sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
Dimensión  → 384
Índice     → NumPy + JSON
Top-k      → 4 como baseline del experimento
Runtime    → Ollama
LLM        → llama3:latest / Llama 3 8B Q4_0
```

Estas elecciones son del LAB y **no constituyen arquitectura aprobada de AI-EAM-MAXIMO**.

Aprendizajes consolidados:

```text
1. Embeddings localizan evidencia; no contienen la respuesta decodificable.
2. El LLM recibe texto original recuperado.
3. Similarity ≠ confianza / answerability.
4. Top-k encontrado ≠ respuesta encontrada.
5. Retrieval correcto ≠ generación necesariamente completa/correcta.
6. Sin evidencia suficiente, el sistema debe poder abstenerse.
7. Retrieval y backend generativo son capas desacoplables.
8. Prompt y generación también deben evaluarse como capas propias.
```

Detalle experimental:

```text
rag/docs/LAB-STEP08_GENERATION_EVALUATION.md
```

---

## 4. Paso 09 — Maximo simulado + Doclinks

✅ **VERIFICADO**

Se estudió y simuló la relación:

```text
ASSET
→ DOCLINKS
→ DOCINFO
→ archivo / referencia documental
```

Baseline del LAB:

```text
PT-201 / PLANTA1
ASSETUID = 1001
ASSETID  = 2001

DOCLINKS.OWNERID
→ ASSETUID en la baseline site-specific elegida
```

Se mantiene explícito que `ASSETID` también puede intervenir en Maximo real según el comportamiento/configuración aplicable de Asset Doclinks.

Resultado probado:

```text
PT-201 / PLANTA1
→ 2 documentos asociados existentes
→ manual_transmisor_PT201.md
→ procedimiento_seguridad_instrumentacion.md
```

Detalle:

```text
rag/docs/LAB-STEP09_MAXIMO_DOCLINKS_SIMULATION.md
rag/docs/study/STUDY-MAXIMO_DOCLINKS_DATA_MODEL.md
```

---

## 5. Paso 10 — contexto EAM → Doclinks → RAG → LLM

✅ **VERIFICADO**

Se demostró:

```text
contexto EAM
→ Maximo simulado determina qué documentos aplican
→ RAG busca únicamente dentro de esos documentos
→ LLM redacta usando evidencia recuperada
```

Regla consolidada:

```text
MAXIMO / EAM
→ determina QUÉ documentos aplican

RAG
→ determina QUÉ evidencia dentro de esos documentos responde la pregunta

LLM
→ interpreta y redacta
```

Se observó una inconsistencia puntual de generación: el LLM negó evidencia sobre `as-found`/observaciones aunque el chunk recuperado sí la contenía. Se conserva como aprendizaje y no se abre nueva fase de tuning.

Detalle:

```text
rag/docs/LAB-STEP10_EAM_CONTEXT_TO_RAG.md
```

---

## 6. Paso 11 — datos transaccionales + RAG documental

✅ **VERIFICADO**

Se añadió `WORKORDER` simulado para `PT-201 / PLANTA1`:

```text
OT-PT201-01 | APPR  | prioridad 2 | abierta
OT-PT201-02 | INPRG | prioridad 1 | abierta
OT-PT201-03 | COMP  | prioridad 3 | excluida
```

El experimento separó dos rutas:

```text
WORKORDER mock
→ filtro estructurado exacto
→ OTs abiertas
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

La orquestación seguía estando cableada explícitamente en Python.

Detalle:

```text
rag/docs/LAB-STEP11_TRANSACTIONAL_PLUS_RAG.md
```

---

## 7. Paso 12 — Tools/MCP + datos EAM + RAG

🧪 **PREPARADO — pendiente de validación local con Cline**

Objetivo: pasar de una orquestación fija en código a capacidades expuestas como Tools MCP.

Servidor:

```text
rag/src/step12_eam_rag_mcp_server.py
```

Tools:

```text
consultar_ots_abiertas_activo(assetnum, siteid)
→ datos estructurados WORKORDER
→ [MAXIMO]

buscar_documentacion_activo(assetnum, siteid, pregunta)
→ ASSET / DOCLINKS / DOCINFO
→ retrieval RAG
→ [FUENTE 1..N]
```

Arquitectura:

```text
Usuario
  ↓
Cline + modelo seleccionado
  ↓
MCP Client
  ↓
eam-rag-lab MCP Server
  ├── Tool transaccional
  └── Tool documental/RAG
          ↓
Host LLM
          ↓
respuesta integrada
```

Decisión importante:

> **La Tool RAG recupera evidencia, pero no invoca un segundo LLM. La síntesis final corresponde al LLM del Host MCP.**

El MCP Lab histórico bajo `mcp/` permanece cerrado/congelado; este experimento no modifica `mcp/src/maximo_mcp.py`.

Detalle:

```text
rag/docs/LAB-STEP12_MCP_TOOLS_EAM_RAG.md
rag/config/cline_step12_mcp_settings.example.json
```

---

## 8. Arquitectura general aprendida

```text
FUENTES TRANSACCIONALES
Maximo / APIs / MCP
        ↓
 datos actuales
        │
        ├──────────────┐
        │              ↓
        │             LLM
        │              ↑
        └──────────────┤
                       │
FUENTES DOCUMENTALES   │
manuales / procedimientos
        ↓
       RAG
        ↓
   evidencia técnica
```

En etapas futuras un agente podría decidir dinámicamente qué capacidades utilizar, pero todavía no es necesario introducir autonomía para validar el Paso 12.

---

## 9. Qué NO está validado todavía

```text
Maximo real
API REST real contra Maximo
IBM Maximo MCP Server oficial
seguridad productiva
permisos documentales reales
actualización incremental productiva del índice
acciones de escritura reales
agentes autónomos
```

---

## 10. Decisiones no tomadas para AI-EAM-MAXIMO

No se ha decidido productivamente:

- proveedor/modelo de embeddings;
- vector database;
- framework RAG;
- LLM productivo;
- ejecución local vs API;
- chunking definitivo;
- Top-k definitivo;
- threshold de relevancia/answerability;
- arquitectura MCP/RAG definitiva.

Los resultados del Learning Lab son aprendizaje y evidencia. Cualquier traslado al producto debe tratarse como:

```text
🟨 CANDIDATO A INCORPORAR
→ análisis
→ decisión explícita
→ 🟩 INCORPORADO si se aprueba
```

---

## 11. Próximo paso operativo

Validar el Paso 12 con Cline:

```text
eam-rag-lab activo
→ 2 Tools visibles
→ Tool transaccional devuelve OTs abiertas
→ Tool documental devuelve evidencia RAG
→ Host/LLM utiliza ambas
→ respuesta integrada
```

Después de esa validación se decidirá el siguiente salto sin abrir complejidad innecesaria.
