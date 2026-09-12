# 📚 RAG — Retrieval-Augmented Generation

> 🎯 **Objetivo:** aprender RAG de forma práctica con foco EAM / IBM Maximo, entendiendo primero el mecanismo básico y evolucionando después hacia casos técnicos reales basados en manuales, procedimientos y conocimiento de mantenimiento.
>
> 📍 **Estado:** 🟢 **EN CURSO — primer experimento iniciado**
>
> 🗓️ **Actualizado:** 2026-09-12

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-12 | Se inicia el primer experimento con IBM Maximo como referencia simulada para descubrir documentos enlazados a un activo antes de aplicar retrieval sobre su contenido. |
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

## 🏭 Enfoque EAM del primer experimento

Usaremos **IBM Maximo como referencia conceptual para localizar los documentos asociados a un activo**, sin afirmar integración con una instancia real.

```text
Activo PT-201 en Maximo (simulado)
        ↓
documentos enlazados + metadata
        ↓
manual / procedimiento sintéticos
        ↓
RAG
```

Artefactos iniciales:

```text
rag/data/maximo/asset_doclinks_mock.json
rag/data/documents/manual_transmisor_PT201.md
rag/data/documents/procedimiento_seguridad_instrumentacion.md
rag/src/step01_discover_documents.py
```

## 🧭 Ruta de aprendizaje

1. **Conceptos esenciales** — qué problema resuelve RAG y por qué un LLM por sí solo no basta.
2. **Descubrimiento de documentos** — localizar, desde contexto EAM/Maximo, qué fuentes corresponden al activo.
3. **Primer pipeline mínimo** — documentos pequeños, una pregunta y recuperación observable.
4. **Chunking** — cómo dividir documentos y por qué cambia la calidad.
5. **Embeddings y búsqueda semántica** — cómo representar y recuperar significado.
6. **Vector store / índice** — dónde se guarda la representación recuperable.
7. **Retrieval** — `top-k`, metadatos y relevancia.
8. **Generación fundamentada** — responder solo con contexto recuperado y citar evidencia.
9. **Evaluación** — medir recuperación, respuestas correctas y casos sin evidencia.
10. **Mejoras** — filtros, búsqueda híbrida, reranking, query rewriting, etc., solo cuando aporten valor.
11. **Aplicación EAM** — manuales, procedimientos, troubleshooting, seguridad y mantenimiento.
12. **MCP + RAG** — combinar datos transaccionales de Maximo con conocimiento documental.

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

Ejecutar el **Paso 01 — descubrimiento de documentos desde Maximo simulado** y observar qué documentación vigente queda asociada a `PT-201 / PLANTA1`.
