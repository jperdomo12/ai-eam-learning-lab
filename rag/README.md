# 📚 RAG — Retrieval-Augmented Generation

> 🎯 **Objetivo:** aprender RAG de forma práctica con foco EAM / IBM Maximo.
>
> 📍 **Estado:** ✅ **RAG BÁSICO VERIFICADO / CERRADO** · ✅ **Aplicación EAM verificada hasta Paso 11**
>
> 🗓️ **Actualizado:** 2026-09-16

## 🕘 Historial

| Fecha | Cambio |
|---|---|
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
3. [`docs/RAG_LAB_HANDOFF.md`](docs/RAG_LAB_HANDOFF.md) — cierre y continuidad hacia Maximo simulado / doclinks.
4. [`docs/study/STUDY-MAXIMO_DOCLINKS_DATA_MODEL.md`](docs/study/STUDY-MAXIMO_DOCLINKS_DATA_MODEL.md) — base conceptual del bloque Maximo simulado + Doclinks + RAG.
5. [`docs/LAB-STEP09_MAXIMO_DOCLINKS_SIMULATION.md`](docs/LAB-STEP09_MAXIMO_DOCLINKS_SIMULATION.md) — práctica verificada: resolver documentos desde contexto EAM simulado.
6. [`docs/LAB-STEP10_EAM_CONTEXT_TO_RAG.md`](docs/LAB-STEP10_EAM_CONTEXT_TO_RAG.md) — práctica verificada: limitar RAG a documentos resueltos por contexto EAM y generar respuesta con LLM local.
7. [`docs/LAB-STEP11_TRANSACTIONAL_PLUS_RAG.md`](docs/LAB-STEP11_TRANSACTIONAL_PLUS_RAG.md) — práctica verificada: combinar OTs estructuradas con conocimiento documental RAG.
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
Datos transaccionales + RAG      ✅ Paso 11
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

Los Pasos 09–11 reutilizan conceptos y convenciones ya conocidas del MCP Lab, pero **no ejecutan MCP ni modifican el laboratorio MCP cerrado**.

## 🚀 Estado del bloque Maximo simulado + Doclinks + RAG

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

En el Paso 11 la respuesta integró correctamente las dos OTs abiertas y las verificaciones documentales previas a la intervención. El formato literal de citas no se respetó completamente (`[MAXIMO]`/`[FUENTE n]`), pero el origen de la evidencia se mantuvo distinguible; se considera limitación menor para el objetivo actual.

## 🚀 Siguiente incremento

Con la separación ya visible y verificada, el siguiente bloque debe estudiar el salto desde:

```text
orquestación fija en código
```

hacia:

```text
Tools / MCP
→ capacidades invocables
→ acceso estructurado a Maximo y/o conocimiento documental
```

sin introducir todavía agentes autónomos. La prioridad sigue siendo entender cada capa antes de añadir autonomía.

No se profundizará ahora en reranking, retrieval híbrido, thresholds, evaluación avanzada o tuning adicional salvo que una necesidad EAM concreta lo justifique.
