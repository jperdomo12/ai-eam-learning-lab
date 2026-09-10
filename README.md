# 🧪 AI-EAM Learning Lab

Hands-on learning and experimentation lab for AI applied to EAM: MCP, RAG, agents and related technologies.

> **Idea central:** aprender haciendo, registrar lo importante y mantener separados los experimentos del producto oficial.

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Se cierra y aprueba la baseline v1.0 del laboratorio MCP; RAG queda identificado como siguiente tema a iniciar. |
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

La documentación se mantiene **viva en GitHub**. Materiales provenientes de chats, Gemini, Claude, Cline u otras etapas son fuentes de reconstrucción; el conocimiento consolidado debe terminar en la documentación vigente del laboratorio.

El estándar documental está en [`docs/DOCUMENTATION_STANDARD.md`](docs/DOCUMENTATION_STANDARD.md).

## 🧭 Temas

| Tema | Estado | Entrada |
|---|---|---|
| MCP — Model Context Protocol | ✅ Cerrado · baseline v1.0 | [`mcp/README.md`](mcp/README.md) |
| RAG — Retrieval-Augmented Generation | ⏭️ Siguiente | Se creará al iniciar el estudio práctico. |
| Agentes | ⏳ Futuro | Se creará cuando comience el estudio real. |

> No se crean carpetas ni documentación de un tema hasta que realmente se empiece a trabajar en él.

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

El primer laboratorio, **MCP**, está consolidado y cerrado para el alcance actual. Su documentación principal está en:

[`mcp/docs/MCP_LAB_DOCUMENTATION.md`](mcp/docs/MCP_LAB_DOCUMENTATION.md)

El siguiente frente de aprendizaje será **RAG**, cuando se abra explícitamente ese laboratorio.
