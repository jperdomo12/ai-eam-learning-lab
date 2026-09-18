# 🔄 RAG LAB — HandOff

> 🎯 **Propósito:** permitir retomar el frente RAG/EAM sin reconstruir chats anteriores y sin duplicar la documentación canónica.
>
> 📍 **Estado:** ✅ **RAG BÁSICO CERRADO** · ✅ **APLICACIÓN EAM VERIFICADA HASTA PASO 12**
>
> 🗓️ **Actualizado:** 2026-09-18
>
> 📘 **Documento canónico:** [`RAG_LIVING_DOCUMENTATION.md`](RAG_LIVING_DOCUMENTATION.md)

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-18 | Auditoría de continuidad: se actualiza el HandOff desde Paso 08 hasta Paso 12, se registran artefactos, resultados y siguiente estado para que GitHub permita continuar sin chats antiguos. |
| 2026-09-14 | Creación del HandOff al cierre de los Pasos 01–08 y transición hacia aplicación EAM / Maximo simulado / Doclinks. |

---

## 1. Dónde estamos

El bloque actual está **cerrado para el alcance pedagógico previsto**.

Se verificaron dos etapas:

```text
RAG BÁSICO
Pasos 01–08
→ documentos → chunks → embeddings → retrieval → contexto → LLM

APLICACIÓN EAM
Pasos 09–12
→ contexto Maximo simulado → Doclinks → RAG
→ datos transaccionales + conocimiento documental
→ Tools MCP
→ Host/LLM selecciona capacidades y combina resultados
```

No hay trabajo técnico pendiente dentro de los Pasos 01–12.

---

## 2. Estado de los Pasos 01–12

```text
01  descubrimiento de documentos                         ✅
02  lectura y chunking visible                           ✅
03  retrieval léxico                                    ✅
04  retrieval semántico                                 ✅
04b filtro de estructura/metadata                       ✅
05  índice vectorial persistente + consulta              ✅
06  contexto fundamentado                               ✅
07  evaluación retrieval / sensibilidad Top-k           ✅
08  generación fundamentada + abstención + control      ✅
09  Maximo simulado: ASSET → DOCLINKS → DOCINFO         ✅
10  contexto EAM → documentos asociados → RAG → LLM     ✅
11  WORKORDER transaccional + RAG documental            ✅
12  Tools/MCP + EAM + RAG + composición desde Cline     ✅
```

Los Pasos 01–07 se conservan principalmente como scripts reproducibles y documentación consolidada. No se crean documentos LAB separados para cada uno porque no aportaría valor adicional al objetivo del laboratorio.

---

## 3. Aprendizajes que deben conservarse

### RAG

```text
RAG recupera evidencia; no reentrena al LLM.
Embeddings localizan chunks; el LLM recibe texto original.
Similarity ≠ confianza / answerability.
Top-k encontrado ≠ respuesta encontrada.
Retrieval correcto ≠ generación necesariamente completa/correcta.
Sin evidencia suficiente → abstención.
Retrieval y generación son capas desacoplables.
```

### EAM / Maximo + documentación

```text
MAXIMO / EAM
→ determina QUÉ documentos aplican al contexto

RAG
→ determina QUÉ evidencia dentro de esos documentos responde

LLM / Host
→ interpreta y redacta
```

### Datos transaccionales + conocimiento

```text
DATOS ESTRUCTURADOS / TRANSACCIONALES
→ consulta estructurada / API / MCP

DOCUMENTOS / CONOCIMIENTO
→ RAG

LLM / Host
→ combina ambas clases de evidencia
```

### MCP

```text
Paso 11
→ el script decide el flujo

Paso 12
→ las capacidades se exponen como Tools
→ el Host/LLM decide cuáles necesita
→ invoca Tools
→ integra los resultados
```

Esto demuestra **tool calling y composición dinámica mediante MCP**, no autonomía completa de un agente.

---

## 4. Baseline pedagógica utilizada

```text
Embeddings: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
Dimensión:  384
Índice:     NumPy + JSON para Pasos 05–08
Top-k:      4 como baseline de generación
Runtime:    Ollama 0.34.0 en Pasos 08–11
LLM local:  llama3:latest / Llama 3 8B Q4_0
MCP:        FastMCP en Paso 12
Host:       Cline en Paso 12
```

Estas elecciones son **pedagógicas** y no constituyen arquitectura aprobada de AI-EAM-MAXIMO.

No trasladar automáticamente:

```text
MiniLM
NumPy + JSON
Top-k = 4
Ollama
Llama 3
FastMCP
local_files_only=True
timeout = 180 s
prompts exactos del LAB
```

---

## 5. Datos y artefactos que permiten reproducir el LAB

### Documentos fuente

```text
rag/data/source_documents/
├── manual_transmisor_PT201.md
└── procedimiento_seguridad_instrumentacion.md
```

Son documentos sintéticos del LAB.

### Evaluación RAG

```text
rag/data/evaluation_cases.json
```

Incluye casos A–D, entre ellos el caso sin respuesta sobre torque para validar abstención.

### Maximo simulado

```text
rag/data/maximo_mock/
├── assets.json
├── doclinks.json
├── docinfo.json
└── workorders.json
```

Baseline principal:

```text
PT-201 / PLANTA1
ASSETUID = 1001
ASSETID  = 2001

DOCLINKS.OWNERID → ASSETUID
→ elección site-specific del LAB, no regla universal de Maximo

2 documentos asociados
3 OTs totales
2 OTs abiertas
```

### Dependencias

```text
rag/requirements.txt
→ sentence-transformers
→ mcp
```

Ollama/Llama 3 fue usado en Pasos 08–11 pero no está gestionado por `requirements.txt`.

---

## 6. Archivos de código relevantes

```text
rag/src/
├── step01_discover_documents.py
├── step02_read_and_chunk.py
├── step03_lexical_retrieval.py
├── step04_semantic_retrieval.py
├── step04b_semantic_retrieval_content_filter.py
├── step05_build_vector_index.py
├── step05_query_vector_index.py
├── step06_build_grounded_context.py
├── step07_evaluate_retrieval_cases.py
├── step07b_evaluate_topk_sensitivity.py
├── step08_generate_grounded_answer.py
├── step08b_generate_grounded_answer_prompt_completeness.py
├── step08c_compare_prompts_deterministic.py
├── step09_resolve_maximo_doclinks.py
├── step10_eam_context_to_rag.py
├── step11_transactional_plus_rag.py
└── step12_eam_rag_mcp_server.py
```

Para comprender resultados y decisiones, leer los documentos antes de releer todo el código.

---

## 7. Documentos específicos de los pasos

```text
rag/docs/LAB-STEP08_GENERATION_EVALUATION.md
rag/docs/LAB-STEP09_MAXIMO_DOCLINKS_SIMULATION.md
rag/docs/LAB-STEP10_EAM_CONTEXT_TO_RAG.md
rag/docs/LAB-STEP11_TRANSACTIONAL_PLUS_RAG.md
rag/docs/LAB-STEP12_MCP_TOOLS_EAM_RAG.md
```

Los Pasos 01–07 quedan cubiertos por:

```text
código reproducible
+ RAG_LAB_FAST_READING.md
+ RAG_LIVING_DOCUMENTATION.md
+ evaluation_cases.json
```

---

## 8. Paso 12 — estado final que no debe reconstruirse desde chats

Servidor:

```text
rag/src/step12_eam_rag_mcp_server.py
```

Config sanitizada:

```text
rag/config/cline_step12_mcp_settings.example.json
```

Tools verificadas:

```text
consultar_ots_abiertas_activo(assetnum, siteid)
→ WORKORDER simulado
→ [MAXIMO]

buscar_documentacion_activo(assetnum, siteid, pregunta)
→ ASSET → DOCLINKS → DOCINFO
→ RAG
→ [FUENTE 1..N]
```

Problema técnico resuelto:

```text
carga normal MiniLM        → ~46,7 s
local_files_only=True      → ~20,8 s
```

La solución final publica las Tools inmediatamente, carga MiniLM de forma lazy desde caché local y reutiliza la instancia.

Validación final:

```text
Cline
→ reconoce 2 Tools
→ Tool transaccional ✅
→ Tool RAG ✅
→ selecciona ambas para una pregunta integrada ✅
```

---

## 9. Qué NO continuar por defecto

No reabrir sin una necesidad EAM concreta:

```text
reranking
hybrid retrieval
threshold tuning
RAGAS
LLM-as-judge
auto-evaluadores avanzados
comparación exploratoria de modelos
vector databases productivas
prompt tuning adicional
```

El objetivo es **AI-Driven EAM**, no especialización en optimización RAG.

---

## 10. Relación con AI-EAM-MAXIMO

Nada del Learning Lab pasa automáticamente al producto.

Regla:

```text
Learning Lab
→ aprendizaje verificado
→ 🟨 candidato
→ análisis explícito
→ decisión del Product Owner
→ 🟩 incorporación si se aprueba
```

Después de cerrar el Paso 12 se eligió iniciar una **consolidación de aprendizajes candidatos** en el repositorio de producto:

```text
jperdomo12/ai-driven-eam-copilot
branch: docs/learning-lab-transfer-assessment
```

Documentos candidatos creados allí:

```text
docs/project/LEARNING_LAB_TRANSFER_FAST_READING.md
docs/project/LEARNING_LAB_TRANSFER_ASSESSMENT.md
```

Su existencia no significa que los candidatos hayan sido aprobados o incorporados todavía.

---

## 11. Lectura recomendada al retomar

Mantenerlo simple:

```text
1. rag/docs/RAG_LAB_FAST_READING.md
   → recordar lo esencial

2. rag/docs/RAG_LIVING_DOCUMENTATION.md
   → estado canónico y detalle consolidado

3. rag/docs/RAG_LAB_HANDOFF.md
   → continuidad operativa / siguiente estado

4. LAB-STEP*.md o código
   → solo si la tarea necesita detalle técnico concreto
```

No reconstruir conversaciones anteriores.

---

## 12. Siguiente estado de trabajo

Los Pasos 01–12 están cerrados.

La continuación inmediata **no es crear automáticamente un Paso 13**. El trabajo abierto está en revisar la transferencia de aprendizajes al producto, manteniendo los Labs simples.

Después de esa revisión, los siguientes bloques de aprendizaje posibles se decidirán por valor real:

```text
- contraste con IBM Maximo MCP Server oficial;
- conceptos mínimos de agentes;
- otra necesidad EAM concreta.
```

No reabrir pasos ya verificados salvo nueva evidencia o una necesidad específica.
