# 📘 RAG Learning Lab — Documentación viva

> 🎯 **Propósito:** conservar el conocimiento vigente, decisiones de laboratorio, resultados y aprendizajes del frente **Retrieval-Augmented Generation (RAG)** aplicado a EAM / IBM Maximo.
>
> 📍 **Estado:** ✅ **RAG BÁSICO VERIFICADO — Pasos 01–08 cerrados; siguiente bloque: simulación Maximo / doclinks**
>
> 🗓️ **Actualizado:** 2026-09-14

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-14 | ✅ Se cierra el **Paso 08 — generación fundamentada**. Con Ollama + `llama3:latest`, el Caso D demuestra abstención correcta ante evidencia inexistente. El control reproducible 08C (`temperature=0`, `seed=42`, dos repeticiones por prompt) confirma que el prompt orientado a `completeness` produce una respuesta sustancialmente más completa que el baseline manteniendo fijo retrieval, contexto, modelo y parámetros. Se cierra la fase de RAG básico sin continuar optimizaciones de prompt/modelo en esta etapa. |
| 2026-09-14 | ♻️ Se reutiliza una instalación previa de **Ollama 0.34.0** con `llama3:latest` (`Llama 3`, `8B`, contexto `8192`, cuantización `Q4_0`) en lugar de instalar otro runtime/modelo. |
| 2026-09-14 | 🧪 La primera ruta de generación mediante OpenAI Responses API alcanzó al proveedor, pero quedó bloqueada por `credit_balance_exhausted`. Se decidió no realizar pagos adicionales para este LAB; la clave fue eliminada/revocada y la variable `OPENAI_API_KEY` eliminada del entorno local. |
| 2026-09-13 | ✅ Se completa la baseline de evaluación del retrieval (Casos A–D) y sensibilidad a `Top-k`; `k=4` queda como baseline pedagógica mínima para cubrir A–C en este corpus. |
| 2026-09-13 | ✅ Se verifican embeddings semánticos, índice vectorial persistente mínimo y construcción del contexto fundamentado. |
| 2026-09-12 | ✅ Se verifican fuente local, lectura, chunking visible y retrieval léxico. |
| 2026-09-12 | Creación inicial del RAG Learning Lab y definición de la ruta incremental de aprendizaje. |

---

## 1. Problema que queremos resolver

Un LLM puede manejar conocimiento general, pero no debe asumirse que conoce de forma fiable:

- el manual exacto de un equipo;
- la última revisión de un procedimiento;
- instrucciones internas de mantenimiento;
- documentación privada o específica de una organización.

Pregunta guía del LAB:

```text
¿Cómo calibro este equipo según su manual?
```

La respuesta debe depender de evidencia documental recuperada, no de memoria genérica del modelo.

---

## 2. Modelo mental de RAG

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
PROMPT FUNDAMENTADO
   ↓
LLM
   ↓
RESPUESTA
```

Idea esencial:

> **El LLM no necesita memorizar los documentos; necesita recibir la evidencia correcta cuando responde.**

---

## 3. Qué NO es RAG

RAG no implica necesariamente:

- reentrenar el LLM;
- fine-tuning;
- cargar documentos completos en cada consulta;
- usar una vector database dedicada;
- eliminar automáticamente las alucinaciones;
- convertir el sistema en un agente.

RAG es principalmente un patrón de:

```text
recuperación
+
contexto
+
generación
```

---

## 4. Fuente inicial del laboratorio

Las primeras prácticas usan:

```text
rag/data/source_documents/
```

Documentos sintéticos:

```text
manual_transmisor_PT201.md
procedimiento_seguridad_instrumentacion.md
```

Separación:

```text
rag/docs/                  → documentación del LAB
rag/docs/study/            → notas pedagógicas
rag/src/                   → código
rag/data/source_documents/ → documentos consumidos por RAG
rag/data/vector_index/     → artefactos generados localmente; no versionados
```

Los documentos son sintéticos y **no deben utilizarse como instrucciones reales de mantenimiento**.

---

## 5. Paso 01 — descubrimiento de documentos

Script:

```text
rag/src/step01_discover_documents.py
```

✅ Verificado.

Aprendizaje:

```text
fuente local
→ localizar archivos candidatos
→ todavía no hay retrieval
```

---

## 6. Paso 02 — lectura y chunking visible

Script:

```text
rag/src/step02_read_and_chunk.py
```

Baseline:

```text
Markdown → un chunk por sección/encabezado
TXT      → un chunk por bloque
```

El manual `PT-201` produjo 9 chunks.

Aprendizaje:

> **El retriever busca sobre unidades recuperables, no necesariamente sobre el documento completo.**

---

## 7. Paso 03 — retrieval léxico

Script:

```text
rag/src/step03_lexical_retrieval.py
```

✅ Verificado.

Mostró que coincidencia de palabras puede fallar cuando pregunta y documento usan expresiones equivalentes:

```text
ajustar
≈
calibrar
```

Aprendizaje:

> **BUEN LLM + BUEN DOCUMENTO + MAL RETRIEVAL = MALA RESPUESTA RAG**

---

## 8. Paso 04 — retrieval semántico

Scripts:

```text
rag/src/step04_semantic_retrieval.py
rag/src/step04b_semantic_retrieval_content_filter.py
```

Modelo pedagógico:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Características:

```text
384 dimensiones
vectores normalizados
cosine similarity mediante producto punto
```

Aprendizajes:

```text
formulación de la pregunta → cambia ranking
similarity alta            → no garantiza respuesta
score                       → no es probabilidad/confianza
```

Paso 04b mostró que separar estructura/metadata de contenido operativo puede mejorar la utilidad del ranking.

Ejemplo conceptual EAM:

```text
METADATA
assetnum / siteid / revision

CONTENIDO RECUPERABLE
seguridad / inspección / calibración / troubleshooting
```

---

## 9. Paso 05 — índice vectorial persistente mínimo

Scripts:

```text
rag/src/step05_build_vector_index.py
rag/src/step05_query_vector_index.py
```

Artefactos locales:

```text
embeddings.npy
metadata.json
manifest.json
```

Resultado:

```text
11 chunks indexados
384 dimensiones
```

Aprendizaje:

```text
INDEXACIÓN
≠
CONSULTA
```

Persistir el índice evita recalcular embeddings de documentos en cada consulta, pero no cambia el significado ni mejora por sí solo el retrieval.

---

## 10. Paso 06 — contexto fundamentado

Script:

```text
rag/src/step06_build_grounded_context.py
```

Flujo verificado:

```text
vector de consulta
→ localizar chunks
→ volver al texto original
→ conservar procedencia
→ construir contexto
→ construir prompt
```

Reglas del prompt:

```text
- responder solo con el contexto recuperado;
- no inventar valores o condiciones;
- declarar evidencia insuficiente;
- citar fuentes.
```

Aprendizaje clave:

> **El embedding localiza evidencia; el LLM recibe texto original, no vectores.**

---

## 11. Paso 07 — evaluación del retrieval

Artefactos:

```text
rag/data/evaluation_cases.json
rag/src/step07_evaluate_retrieval_cases.py
rag/src/step07b_evaluate_topk_sensitivity.py
```

Casos:

```text
A. respuesta presente
B. formulación distinta
C. información repartida
D. respuesta inexistente
```

Resultados de sensibilidad:

```text
Caso A → cobertura completa desde k=2
Caso B → cobertura completa desde k=3
Caso C → cobertura completa desde k=4
Caso D → sigue sin respuesta aunque k aumente
```

Por ello se adopta para generación:

```text
Top-k = 4
```

solo como baseline pedagógica del LAB.

Aprendizajes:

```text
TOP-K ENCONTRADO ≠ RESPUESTA ENCONTRADA
similarity alta       ≠ evidencia suficiente
más k                 ≠ crear evidencia inexistente
```

---

## 12. Paso 08 — generación fundamentada

Scripts:

```text
rag/src/step08_generate_grounded_answer.py
rag/src/step08b_generate_grounded_answer_prompt_completeness.py
rag/src/step08c_compare_prompts_deterministic.py
```

### 12.1 Backend generativo

Ruta inicial:

```text
OpenAI Responses API
```

Llegó al proveedor, pero terminó en:

```text
429 / credit_balance_exhausted
```

Decisión:

```text
no añadir crédito API
→ usar generación local
```

Ruta activa del LAB:

```text
Ollama 0.34.0
+
llama3:latest
```

Configuración observada:

```text
Llama 3
8.0B parámetros
8192 contexto
Q4_0
completion
```

La elección es del LAB, no del producto AI-EAM-MAXIMO.

### 12.2 Caso C — información repartida

Pregunta:

```text
¿Qué debo verificar antes de ajustar el PT-201 y cómo debo calibrarlo?
```

Retrieval con `Top-k=4` recuperó correctamente:

```text
1. Inspección previa
2. Procedimiento de calibración
3. Criterio de aceptación
4. Seguridad antes de calibrar
```

La primera generación fue fundamentada pero incompleta.

Aprendizaje:

```text
RETRIEVAL COMPLETO
≠
GENERACIÓN COMPLETA
```

### 12.3 Caso D — respuesta inexistente

Pregunta:

```text
¿Cuál es el par de apriete de los bornes eléctricos del PT-201?
```

Los documentos no contienen ese dato.

Resultado:

```text
llama3:latest
→ declara evidencia insuficiente
→ no inventa un valor
```

✅ Abstención verificada en el caso probado.

### 12.4 Prompt orientado a completeness

El Paso 08B modifica únicamente las instrucciones del prompt para exigir:

```text
- identificar todas las partes de la pregunta;
- revisar todas las fuentes;
- responder cada parte respaldada;
- declarar partes sin evidencia;
- verificar que no se omitió evidencia aplicable.
```

Las primeras ejecuciones mostraron mejora, pero todavía existía variabilidad de generación.

### 12.5 Control reproducible 08C

Se fijan:

```text
temperature = 0
seed        = 42
2 repeticiones por prompt
```

Se comparan:

```text
Prompt A → baseline
Prompt B → completeness
```

manteniendo fijo:

```text
retrieval
Top-k
contexto
modelo
parámetros de generación
pregunta
```

Resultado:

```text
Prompt A → dos salidas idénticas
Prompt B → dos salidas idénticas
```

Prompt A continúa resumiendo demasiado la calibración.

Prompt B cubre de forma reproducible:

```text
inspección
seguridad
procedimiento completo
ZERO / SPAN
0 / 5 / 10 bar
±0,05 bar
as-left
criterios de aceptación
evaluación adicional
```

sin introducir valores técnicos externos al contexto.

Conclusión:

> **En este experimento, mejorar el prompt aumentó `completeness` sin modificar el retrieval.**

El formato exacto de citas no siempre se respeta literalmente: el modelo usa formas como `(FUENTE 2)` en lugar de `[FUENTE 2]`. Se considera una limitación menor para el objetivo de aprendizaje actual y no se optimiza más en esta fase.

Detalles completos:

```text
rag/docs/LAB-STEP08_GENERATION_EVALUATION.md
```

---

## 13. Resultado consolidado de RAG básico

```text
Fuente local / adquisición      → ✅
Chunking visible                → ✅
Retrieval léxico                → ✅
Embeddings / retrieval semántico→ ✅
Índice persistente              → ✅
Contexto fundamentado           → ✅
Evaluación retrieval A–D        → ✅
Generación fundamentada         → ✅
Abstención                      → ✅ caso probado
Reproducibilidad control 08C    → ✅
```

Aprendizajes principales:

```text
1. RAG no entrena al LLM; recupera evidencia en tiempo de consulta.
2. Embeddings ayudan a localizar chunks; no contienen la respuesta decodificable.
3. El LLM recibe texto original recuperado.
4. Similarity no equivale a confianza ni answerability.
5. Top-k encontrado no significa respuesta encontrada.
6. Retrieval correcto no garantiza generación completa.
7. Prompt y generación deben evaluarse como capas propias.
8. Un sistema correcto debe poder abstenerse cuando falta evidencia.
9. Retrieval y backend generativo están desacoplados.
10. Para comparar generación conviene controlar también parámetros de muestreo.
```

---

## 14. Fuentes futuras y arquitectura general

RAG no depende de una fuente concreta.

Ejemplos:

```text
filesystem
SharePoint
Documentum
object storage
web interna
IBM Maximo / doclinks
```

Arquitectura general:

```text
SOURCE
  ↓
CONNECTOR / ACCESS
  ↓
EXTRACTION / PARSING
  ↓
NORMALIZATION
  ↓
CHUNKING + METADATA
  ↓
EMBEDDINGS / INDEX
  ↓
RETRIEVAL
  ↓
LLM
```

Metadatos EAM potenciales:

```text
source_system
document_id
document_name
revision
assetnum
siteid
document_type
url / path
permissions
```

---

## 15. Relación futura con IBM Maximo

Siguiente bloque del LAB:

```text
Activo / contexto Maximo simulado
      ↓
doclinks / metadata
      ↓
localizar documento
      ↓
RAG
      ↓
respuesta fundamentada
```

Secuencia vigente:

```text
1. Carpeta local                              ✅
2. Chunking visible                           ✅
3. Retrieval léxico                          ✅
4. Retrieval semántico                       ✅
5. Índice persistente                        ✅
6. Contexto fundamentado                     ✅
7. Evaluación retrieval                      ✅
8. Generación fundamentada                   ✅
9. Simulación Maximo / doclinks              ← SIGUIENTE
10. Combinación contexto EAM + RAG
11. Integración real con Maximo               ← solo si procede
```

Ejemplo futuro:

```text
“La bomba B-201 presenta alta temperatura.
¿Tiene OTs abiertas y qué indica su manual que debo revisar?”

MCP → datos transaccionales / actuales de Maximo
RAG → manuales / procedimientos
LLM → respuesta integrada
```

---

## 16. Decisiones todavía NO tomadas

No se ha decidido para AI-EAM-MAXIMO:

- proveedor/modelo de embeddings;
- vector database;
- framework RAG;
- LLM productivo;
- ejecución local vs API;
- chunking definitivo;
- `Top-k` definitivo;
- threshold de relevancia/answerability;
- framework de evaluación productivo.

Las tecnologías usadas aquí son únicamente **baselines pedagógicas**:

```text
MiniLM multilingual
NumPy + JSON
Top-k = 4
Ollama
Llama 3 8B Q4_0
```

Nada de ello se convierte automáticamente en arquitectura del producto.

---

## 17. Cierre de esta etapa

La fase de **RAG básico** se considera suficientemente comprendida y verificada para el objetivo de aprendizaje actual.

No se continuará ahora con:

```text
más prompt tuning
más modelos locales
reranking
retrieval híbrido
threshold tuning
LLM-as-judge
evaluación automática avanzada
```

salvo que una necesidad posterior del proyecto justifique profundizar.

Próximo objetivo:

> **entender cómo entra el contexto EAM / IBM Maximo en el proceso de descubrimiento documental y cómo ese contexto alimenta el RAG ya comprendido.**
