# 🧪 AI-EAM Learning Lab

Hands-on learning and experimentation lab for AI applied to EAM: MCP, RAG, agents and related technologies.

> **Idea central:** aprender haciendo, registrar lo importante y mantener separados los experimentos del producto oficial.

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Se inicializa el Learning Lab y se define MCP como primer tema activo. |

## 🎯 Para qué existe este repositorio

Este repositorio es un espacio de **estudio práctico, experimentación y memoria técnica personal**.

Aquí podemos:

- estudiar conceptos de IA;
- construir pruebas pequeñas;
- reproducir PoCs anteriores;
- cometer errores sin convertirlos en decisiones de producto;
- registrar qué funcionó y qué no;
- relacionar los aprendizajes con EAM e IBM Maximo;
- identificar ideas que eventualmente merezcan incorporarse al proyecto AI-EAM-MAXIMO.

## ⚡ Forma de trabajo

El Learning Lab prioriza:

**estudiar → probar → entender → registrar → continuar**

No busca reproducir el proceso formal de un producto. La documentación y el Git workflow deben ser suficientemente rigurosos para no perder conocimiento, pero suficientemente ligeros para no frenar el aprendizaje.

El estándar documental del laboratorio está en [`docs/DOCUMENTATION_STANDARD.md`](docs/DOCUMENTATION_STANDARD.md).

## 🧭 Temas

| Tema | Estado | Entrada |
|---|---|---|
| MCP — Model Context Protocol | 🧪 Activo | [`mcp/README.md`](mcp/README.md) |
| RAG | ⏳ Futuro | Se creará cuando comience el estudio real. |
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

Los ejemplos que requieran configuración sensible deben utilizar variables de entorno o archivos de ejemplo sanitizados.

## 🚀 Ahora mismo

El primer frente activo es **MCP**.

La primera etapa consiste en reconstruir y auditar el PoC histórico realizado previamente con Gemini / Claude / Cline, separar lo realmente probado de lo diseñado o asumido y después reiniciar el aprendizaje de MCP de forma limpia y reproducible.
