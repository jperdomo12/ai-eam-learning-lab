# 📚 RAG — Retrieval-Augmented Generation

> 🎯 **Objetivo:** aprender RAG de forma práctica con foco EAM / IBM Maximo, entendiendo primero el mecanismo básico y evolucionando después hacia casos técnicos reales basados en manuales, procedimientos y conocimiento de mantenimiento.
>
> 📍 **Estado:** 🟢 **EN CURSO — Pasos 01 y 02 verificados; Paso 03 retrieval mínimo**
>
> 🗓️ **Actualizado:** 2026-09-13

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-13 | ✅ Se verifica en el portátil el **Paso 02**: lectura y chunking visible correctos. El manual `PT-201` produjo 9 chunks. Se crea el **Paso 03** con una baseline de retrieval léxico antes de introducir embeddings. |
| 2026-09-12 | ✅ Se verifica en el portátil el **Paso 01**: descubrimiento correcto de los dos documentos fuente desde `rag/data/source_documents/`. Se crea el **Paso 02** para leer contenido y mostrar chunks de forma explícita antes de introducir embeddings. |
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
rag/src/                   → código del laboratorio
rag/data/source_documents/ → documentos QUE CONSUME el RAG
```

Artefactos actuales:

```text
rag/data/source_documents/manual_transmisor_PT201.md
rag/data/source_documents/procedimiento_seguridad_instrumentacion.md
rag/src/step01_discover_documents.py
rag/src/step02_read_and_chunk.py
rag/src/step03_lexical_retrieval.py
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
4. **Primer retrieval mínimo** — 🟢 recuperar chunks mediante coincidencia léxica y observar sus limitaciones.
5. **Embeddings y búsqueda semántica** — representar y recuperar significado, no solo palabras iguales.
6. **Vector store / índice** — dónde se guarda la representación recuperable.
7. **Retrieval** — `top-k`, metadatos y relevancia.
8. **Generación fundamentada** — responder solo con contexto recuperado y citar evidencia.
9. **Evaluación** — medir recuperación, respuestas correctas y casos sin evidencia.
10. **Mejoras** — filtros, búsqueda híbrida, reranking, query rewriting, etc., solo cuando aporten valor.
11. **Aplicación EAM** — manuales, procedimientos, troubleshooting, seguridad y mantenimiento.
12. **Maximo simulado** — usar contexto EAM para descubrir documentos asociados a un activo.
13. **MCP + RAG / Maximo real** — solo después de entender y validar lo anterior.

## 📚 Documentación

Documento vivo principal:

[`docs/RAG_LIVING_DOCUMENTATION.md`](docs/RAG_LIVING_DOCUMENTATION.md)

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

Sincronizar con **GitHub Desktop** y ejecutar en la terminal de **VS Code**:

```text
python rag/src/step03_lexical_retrieval.py
```

Primero se prueba una consulta con términos cercanos al documento:

```text
procedimiento calibracion PT-201
```

Después se repetirá con una formulación equivalente pero distinta:

```text
¿Cómo ajusto el transmisor de presión?
```

El objetivo es observar una limitación esencial: **la búsqueda por palabras puede funcionar cuando coinciden los términos, pero no entiende realmente el significado**. Esa comparación prepara el paso siguiente: embeddings + búsqueda semántica.