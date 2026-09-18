# 🧪 AI-EAM Learning Lab

Hands-on learning and experimentation lab for AI applied to EAM: fundamentos de IA, MCP, RAG, agentes y tecnologías relacionadas.

> **Idea central:** aprender haciendo, registrar lo importante y mantener separados los experimentos del producto oficial.

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-18 | Cierre documental integral: el Learning Lab queda **congelado / bajo demanda**; MCP y RAG/EAM/MCP permanecen cerrados, los estudios transversales quedan consolidados y Agentes deja de ser un siguiente laboratorio automático. |
| 2026-09-18 | Se incorpora [`STUDY-LLM_BEYOND_THE_MODEL.md`](STUDY-LLM_BEYOND_THE_MODEL.md) como estudio transversal sobre cómo los LLM usan Connectors/Apps, Tools, MCP, RAG y sistemas externos; se actualiza además el estado del RAG/EAM/MCP hasta Paso 12 y su transferencia al producto. |
| 2026-09-14 | Se mueve `STUDY-AI_FOUNDATIONS_AND_HISTORY.md` a la raíz del repositorio y se amplía con historia de IA, IA simbólica/Turbo Prolog, nacimiento progresivo de los LLM, origen de MCP, entrenamiento/inferencia, cuantización, Fine-tuning vs. RAG y una definición más precisa de agente. |
| 2026-09-14 | Se incorpora la nota transversal [`STUDY-AI_FOUNDATIONS_AND_HISTORY.md`](STUDY-AI_FOUNDATIONS_AND_HISTORY.md), consolidando historia mínima de IA, LLM, tokenización, Transformer/Attention, modelos/runtimes/productos, RAG, MCP y agentes. Se actualiza además la situación 2026 de IBM Maximo: servidor MCP oficial en MAS 9.2, continuidad de OSLC y capacidades RAG/DocSearch documentadas en Maximo Assistant. |
| 2026-09-14 | Se actualiza el estado del RAG: fundamentos básicos **verificados y cerrados para el nivel actual de aprendizaje** tras los Pasos 01–08. El siguiente bloque práctico será la aplicación EAM mediante simulación Maximo/doclinks. |
| 2026-09-12 | Se inicia formalmente el **RAG Learning Lab** con pregunta guía, documentación viva y plan incremental de aprendizaje. |
| 2026-09-12 | Se simplifica la estructura documental: `DOCUMENTATION_STANDARD.md` pasa a la raíz del repositorio y se refuerza la regla de Historial obligatorio en toda documentación Markdown viva. |
| 2026-09-12 | MCP queda **cerrado/congelado en v1.2** tras la revalidación final de VS Code + Cline: configuración efectiva recuperada, Maximo/Filesystem probados y composición multi-MCP validada. |
| 2026-09-10 | MCP queda cerrado y consolidado en baseline v1.1 con documentación completa, Fast Reading y artefactos preservados; RAG queda como siguiente laboratorio. |
| 2026-09-10 | Se cierra y aprueba la baseline inicial del laboratorio MCP. |
| 2026-09-10 | Se inicializa el Learning Lab y se define MCP como primer tema. |

## 🎯 Para qué existe este repositorio

Este repositorio es un espacio de **estudio práctico, experimentación y memoria técnica personal**.

Aquí podemos:

- estudiar conceptos de IA;
- construir pruebas pequeñas;
- recuperar y consolidar experimentos previos;
- cometer errores sin convertirlos en decisiones de producto;
- registrar qué funcionó y qué no;
- relacionar los aprendizajes con EAM e IBM Maximo;
- identificar ideas que eventualmente merezcan incorporarse al proyecto AI-EAM-MAXIMO.

## ⚡ Forma de trabajo

El Learning Lab prioriza:

**estudiar → probar → entender → registrar → continuar**

No busca reproducir el proceso formal de un producto. La documentación y el Git workflow deben ser suficientemente rigurosos para no perder conocimiento, pero suficientemente ligeros para no frenar el aprendizaje.

La documentación se mantiene **viva en GitHub**. Materiales provenientes de chats, Gemini, Claude, Cline, notas personales u otras etapas son fuentes de reconstrucción; el conocimiento consolidado debe terminar en la documentación vigente del laboratorio.

El estándar documental está en [`DOCUMENTATION_STANDARD.md`](DOCUMENTATION_STANDARD.md).

## 🧭 Temas

| Tema | Estado | Entrada |
|---|---|---|
| Fundamentos de IA e historia mínima | 📘 Consolidado / consulta | [`STUDY-AI_FOUNDATIONS_AND_HISTORY.md`](STUDY-AI_FOUNDATIONS_AND_HISTORY.md) |
| LLM más allá del modelo | 📘 Consolidado / consulta | [`STUDY-LLM_BEYOND_THE_MODEL.md`](STUDY-LLM_BEYOND_THE_MODEL.md) |
| MCP — Model Context Protocol | ✅ Cerrado / congelado · v1.2 | [`mcp/README.md`](mcp/README.md) |
| RAG — Retrieval-Augmented Generation | ✅ RAG/EAM/MCP verificado · Pasos 01–12 cerrados | [`rag/README.md`](rag/README.md) |
| Agentes | ⏸️ Bajo demanda | Solo se abrirá si una necesidad concreta de AI-EAM-MAXIMO justifica un estudio o Mini-LAB. |

> No se crean carpetas ni documentación de un tema hasta que realmente se empiece a trabajar en él.

## 🧠 Fundamentos transversales

Las dos notas transversales principales son:

- [`STUDY-AI_FOUNDATIONS_AND_HISTORY.md`](STUDY-AI_FOUNDATIONS_AND_HISTORY.md) → fundamentos generales e historia mínima.
- [`STUDY-LLM_BEYOND_THE_MODEL.md`](STUDY-LLM_BEYOND_THE_MODEL.md) → cómo el LLM accede a Tools, Connectors, MCP, RAG y sistemas externos.

Resume y relaciona:

```text
historia mínima de IA
→ IA simbólica / Machine Learning / Deep Learning
→ tokenización
→ Transformer / Attention
→ LLM
→ entrenamiento / inferencia / cuantización
→ prompting / Fine-tuning / RAG
→ Tools / MCP
→ agentes
→ aplicación EAM / IBM Maximo
```

Estas notas no sustituyen la documentación experimental de MCP o RAG; sirven como mapa conceptual común y puente hacia AI-EAM-MAXIMO.

## 🔗 Relación con AI-EAM-MAXIMO

Este repositorio **no es la fuente de verdad del producto AI-EAM-MAXIMO**.

```text
Learning Lab
   ↓ aprender / experimentar
aprendizaje útil
   ↓
🟨 CANDIDATO A INCORPORAR
   ↓ revisión y aprobación explícita
AI-EAM-MAXIMO
   ↓
🟩 implementación y documentación oficial
```

La fuente de verdad del producto continúa siendo:

`jperdomo12/ai-driven-eam-copilot`

Nada aprendido o probado aquí se convierte automáticamente en arquitectura, requisito o decisión del producto.

## 🔐 Repositorio público

No almacenar secretos, tokens, PATs, credenciales, endpoints privados, datos de clientes ni información confidencial.

Los ejemplos que requieran configuración sensible deben utilizar variables de entorno o archivos sanitizados.

## 🚀 Estado actual

> 🧊 **LEARNING LAB CONGELADO / BAJO DEMANDA.** No existe un siguiente laboratorio automático. El repositorio se reabre únicamente cuando AI-EAM-MAXIMO plantee una necesidad concreta que requiera aprendizaje o experimentación adicional.

El laboratorio **MCP** está cerrado y congelado para el alcance actual.

El bloque **RAG + EAM + MCP** también está cerrado para el alcance pedagógico actual. Se verificaron los Pasos 01–12, incluyendo Maximo simulado, Doclinks, datos transaccionales, RAG y composición de Tools MCP.

Los aprendizajes relevantes ya fueron evaluados y transferidos de forma controlada a `jperdomo12/ai-driven-eam-copilot`.

No existe un Paso 13 automático. El Lab se reabre solo cuando una necesidad EAM concreta justifique nueva experimentación.

Entrada RAG:

[`rag/README.md`](rag/README.md)

Documentación viva RAG:

[`rag/docs/RAG_LIVING_DOCUMENTATION.md`](rag/docs/RAG_LIVING_DOCUMENTATION.md)
