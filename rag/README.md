# 📚 RAG — Retrieval-Augmented Generation

> 🎯 **Objetivo:** aprender RAG de forma práctica con foco EAM / IBM Maximo, entendiendo primero el mecanismo básico y evolucionando después hacia casos técnicos reales basados en manuales, procedimientos y conocimiento de mantenimiento.
>
> 📍 **Estado:** 🟢 **EN CURSO — Pasos 01–06 verificados; Paso 07A baseline de evaluación del retrieval**
>
> 🗓️ **Actualizado:** 2026-09-13

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-13 | 🧪 Se prueba el **Caso D — respuesta inexistente** con la pregunta sobre el par de apriete de los bornes del `PT-201`. El retriever devuelve igualmente un `Top-3` (`0.5414`, `0.4098`, `0.3795`), pero ninguno contiene el dato solicitado. Se confirma que **Top-k encontrado ≠ respuesta encontrada** y que la `similarity` no demuestra por sí sola suficiencia de evidencia. Se crea `evaluation_cases.json` y el **Paso 07A** para ejecutar de forma reproducible los casos A–D antes de conectar un LLM. |
| 2026-09-13 | ✅ Se verifica el **Paso 06**: el LAB recupera el `Top-3` desde el índice persistido, vuelve desde los vectores al **texto original**, construye un contexto explícito con documento/sección/chunk y genera el **prompt fundamentado** que recibiría un LLM. Se confirma que los embeddings sirven para localizar evidencia, mientras que el LLM recibe la pregunta + instrucciones + texto recuperado. |
| 2026-09-13 | ✅ Se verifica el **Paso 05** completo: la indexación persiste 11 embeddings de 384 dimensiones y la consulta posterior reproduce exactamente el mismo `Top-3` del Paso 04b generando únicamente el embedding de la pregunta. Se confirma experimentalmente la separación entre **INDEXACIÓN** y **CONSULTA**. |
| 2026-09-13 | ✅ Se verifica el **Paso 04 / 04b**: los embeddings semánticos funcionan y el experimento demuestra que separar estructura/identificación del contenido operativo mejora la utilidad del `Top-k`. Con la misma consulta y el mismo modelo, el `Top-3` queda formado por seguridad antes de calibrar, seguridad previa y procedimiento de calibración. |
| 2026-09-13 | 🧪 Tras tres consultas del **Paso 04** se observa que el ranking semántico cambia con la formulación de la consulta, pero también que chunks de título/identificación pueden competir con conocimiento operativo. Se crea el **Paso 04b** como experimento controlado: mismo modelo, mismos chunks, misma consulta y `Top-k`, excluyendo únicamente estructura/identificación del conjunto elegible para retrieval. |
| 2026-09-13 | 🧪 Primera ejecución real del **Paso 04** con embeddings locales (`paraphrase-multilingual-MiniLM-L12-v2`): se evaluaron 14 chunks con vectores de 384 dimensiones. El retrieval semántico funcionó técnicamente, pero el chunk de calibración no apareció en el `Top-3`; se añade ranking completo como diagnóstico antes de cambiar modelo, chunking o estrategia. |
| 2026-09-13 | ✅ Se verifica el **Paso 03** con dos consultas: el retrieval léxico funciona por coincidencia de términos, pero una formulación semánticamente equivalente puede dejar fuera del `Top-k` el chunk realmente útil. |
| 2026-09-13 | Se crea `rag/docs/study/` y se trasladan allí las notas `STUDY-*`, separando el material pedagógico de la documentación canónica/viva del laboratorio. |
| 2026-09-13 | Se crea la nota de estudio **RAG — Conceptos esenciales**, con fundamentos y conceptos intermedios importantes como retrieval híbrido, reranking, reindexación, seguridad y evaluación. |
| 2026-09-13 | Se crea la nota de estudio **LLM vs. RAG — Cómo se relacionan técnicamente**, como apoyo conceptual vivo para comparar entrenamiento, inferencia, embeddings, retrieval y generación. |
| 2026-09-13 | ✅ Se verifica en el portátil el **Paso 02**: lectura y chunking visible correctos. El manual `PT-201` produjo 9 chunks. |
| 2026-09-12 | ✅ Se verifica en el portátil el **Paso 01**: descubrimiento correcto de los dos documentos fuente desde `rag/data/source_documents/`. |
| 2026-09-12 | Se separan claramente los documentos fuente del código y de la documentación del LAB usando `rag/data/source_documents/`. Se aclara además que la forma de obtener los documentos cambia según la fuente, mientras que el pipeline RAG posterior debe mantenerse lo más estable posible. |
| 2026-09-12 | Se corrige el alcance del primer experimento: la fuente inicial será una **carpeta local del portátil**. IBM Maximo queda como deseable posterior, primero mediante simulación y más adelante mediante integración real si procede. |
| 2026-09-12 | Inicio formal del RAG Learning Lab tras cerrar/congelar MCP. Se define la pregunta guía y el enfoque incremental de aprendizaje. |

## 🎯 Pregunta guía

```text
¿Cómo calibro este equipo según su manual?
```

La pregunta representa el tipo de problema que RAG debe resolver: la respuesta depende de conocimiento contenido en documentos externos que el modelo no debería inventar ni asumir.

## 🧠 Idea central

```text
Documento / manual
      ↓
preparación + fragmentación
      ↓
representación para búsqueda
      ↓
consulta del usuario
      ↓
recuperación de fragmentos relevantes
      ↓
contexto recuperado + pregunta
      ↓
LLM
      ↓
respuesta fundamentada
```

RAG no sustituye al LLM. Le aporta **contexto recuperado en el momento de la consulta** para que pueda responder usando evidencia externa.

## 🧪 Fuente del primer experimento

Para las primeras prácticas usamos una **carpeta local del portátil**:

```text
rag/data/source_documents/
```

Separación de responsabilidades:

```text
rag/docs/                  → documentación SOBRE el laboratorio
rag/docs/study/            → notas pedagógicas para estudiar y repasar
rag/src/                   → código del laboratorio
rag/data/source_documents/ → documentos QUE CONSUME el RAG
rag/data/vector_index/     → índice generado localmente; no versionado en Git
```

Artefactos actuales:

```text
rag/data/source_documents/manual_transmisor_PT201.md
rag/data/source_documents/procedimiento_seguridad_instrumentacion.md
rag/data/evaluation_cases.json
rag/requirements.txt
rag/src/step01_discover_documents.py
rag/src/step02_read_and_chunk.py
rag/src/step03_lexical_retrieval.py
rag/src/step04_semantic_retrieval.py
rag/src/step04b_semantic_retrieval_content_filter.py
rag/src/step05_build_vector_index.py
rag/src/step05_query_vector_index.py
rag/src/step06_build_grounded_context.py
rag/src/step07_evaluate_retrieval_cases.py
```

Los documentos son **sintéticos de laboratorio** y no deben utilizarse para mantenimiento real.

## 🔌 Las fuentes cambian; el pipeline RAG no debería reinventarse

La forma de **obtener** los documentos dependerá de la fuente:

```text
Carpeta Windows/Linux → acceso a filesystem
Documentum            → API/conector
SharePoint            → API/conector
IBM Maximo            → documentos enlazados + metadata + acceso al archivo/URL
Object storage        → SDK/API
```

Pero, una vez obtenido el documento, buscamos converger hacia un flujo común:

```text
FUENTE
  ↓ acceso específico
DOCUMENTO + METADATOS
  ↓
EXTRACCIÓN / NORMALIZACIÓN
  ↓
CHUNKING
  ↓
ÍNDICE / RETRIEVAL
  ↓
LLM
```

**Idea clave:** cambia principalmente la capa de acceso/adquisición; el núcleo del RAG debería ser reutilizable.

## 🏭 Papel futuro de IBM Maximo

IBM Maximo sigue siendo el ejemplo EAM deseable para una fase posterior:

```text
Activo en Maximo
      ↓
documentos enlazados / metadata
      ↓
localizar archivo o URL
      ↓
RAG
```

Primero se simulará esa capa de descubrimiento documental. Solo después, si aporta valor y existe una instancia disponible, se evaluará una integración real.

## 🧭 Ruta de aprendizaje

1. **Conceptos esenciales** — qué problema resuelve RAG y por qué un LLM por sí solo no basta.
2. **Fuente local** — ✅ descubrir documentos desde una carpeta del portátil.
3. **Lectura + chunking visible** — ✅ dividir los documentos en fragmentos observables y entendibles.
4. **Primer retrieval mínimo** — ✅ recuperar chunks mediante coincidencia léxica y comprobar sus limitaciones.
5. **Embeddings y búsqueda semántica** — ✅ representar pregunta y chunks como vectores, comparar similitud y comprobar el impacto de separar estructura/metadata del contenido recuperable.
6. **Índice vectorial persistente mínimo** — ✅ separar indexación y consulta guardando vectores + metadata localmente, todavía sin una vector database dedicada.
7. **Construcción de contexto fundamentado** — ✅ recuperar `Top-k`, volver al texto original y construir el contexto/prompt que recibiría el LLM.
8. **Baseline de evaluación y abstención** — 🟢 ejecutar casos A–D y distinguir retrieval relevante de evidencia suficiente.
9. **Generación fundamentada** — conectar un LLM solo después de disponer de casos reproducibles para evaluar respuesta, citas y abstención.
10. **Mejoras** — filtros, búsqueda híbrida, reranking, query rewriting, etc., solo cuando aporten valor.
11. **Aplicación EAM** — manuales, procedimientos, troubleshooting, seguridad y mantenimiento.
12. **Maximo simulado** — usar contexto EAM para descubrir documentos asociados a un activo.
13. **MCP + RAG / Maximo real** — solo después de entender y validar lo anterior.

## 📚 Documentación

Documento vivo principal:

[`docs/RAG_LIVING_DOCUMENTATION.md`](docs/RAG_LIVING_DOCUMENTATION.md)

Notas de estudio complementarias:

- [`docs/study/STUDY-RAG_CORE_CONCEPTS.md`](docs/study/STUDY-RAG_CORE_CONCEPTS.md) — **RAG — Conceptos esenciales**.
- [`docs/study/STUDY-LLM_VS_RAG_TECHNICAL_RELATIONSHIP.md`](docs/study/STUDY-LLM_VS_RAG_TECHNICAL_RELATIONSHIP.md) — **LLM vs. RAG — Cómo se relacionan técnicamente**.

## 🔗 Relación con MCP

```text
MCP → acceso a sistemas, datos y acciones
RAG → recuperación de conocimiento desde documentos
```

Más adelante podrán combinarse, pero el laboratorio RAG comienza de forma independiente para entender primero su mecanismo.

## 🔗 Relación con AI-EAM-MAXIMO

Nada aprendido aquí se convierte automáticamente en arquitectura o requisito del producto.

```text
RAG Learning Lab
      ↓
aprendizaje / evidencia
      ↓
🟨 CANDIDATO A INCORPORAR
      ↓ revisión explícita
AI-EAM-MAXIMO
```

## 🚀 Siguiente paso

Sincronizar con **GitHub Desktop** y ejecutar:

```text
python rag/src/step07_evaluate_retrieval_cases.py
```

El script ejecuta cuatro casos reproducibles:

```text
A. respuesta presente
B. formulación distinta
C. información repartida
D. respuesta inexistente
```

Para A–C comprueba de forma pedagógica si los headings de evidencia esperados aparecen en el `Top-k`. Para D **no intenta decidir automáticamente** que existe o no respuesta mediante un umbral de `similarity`: muestra el `Top-k` para que observemos que recuperar candidatos no equivale a disponer de evidencia suficiente. Este baseline se reutilizará después para evaluar un LLM real.
