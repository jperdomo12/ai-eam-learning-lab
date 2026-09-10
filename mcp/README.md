# 🔌 MCP — Model Context Protocol

> 🎯 **Objetivo:** aprender MCP de forma práctica con foco EAM / IBM Maximo y conservar una memoria técnica completa, actualizada y reutilizable.
>
> 📍 **Estado:** ✅ **CERRADO para el alcance actual de aprendizaje**
>
> 🗓️ **Actualizado:** 2026-09-10

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Se aprueba `docs/MCP_LAB_DOCUMENTATION.md` v1.0 como fuente canónica y autosuficiente del laboratorio MCP y se simplifica la navegación eliminando documentación transitoria duplicada. |
| 2026-09-10 | Se incorporan al Learning Lab el código final, dos artefactos tempranos recuperados y la configuración sanitizada de Claude Desktop. |
| 2026-09-10 | Consolidación inicial del trabajo previo realizado con Gemini / Claude / Cline. |

## 📚 Por dónde empezar

Para recuperar el tema después de semanas o meses:

1. [`docs/MCP_LAB_DOCUMENTATION.md`](docs/MCP_LAB_DOCUMENTATION.md) — **fuente canónica**: concepto, historia completa, instalación, configuración, código, 14 Tools, pruebas, evidencias, problemas, aprendizajes, límites y estado tecnológico actual.
2. [`docs/MCP_LAB_HANDOFF.md`](docs/MCP_LAB_HANDOFF.md) — estado de cierre y continuidad.
3. [`src/maximo_mcp.py`](src/maximo_mcp.py) — artefacto final de la PoC.
4. [`src/history/`](src/history/) — dos versiones tempranas preservadas para entender la evolución del experimento.
5. [`config/claude_desktop_config.example.json`](config/claude_desktop_config.example.json) — copia sanitizada de la configuración histórica real de Claude Desktop.

> **Regla:** los documentos crudos provenientes de Gemini / Claude / Cline fueron fuentes de reconstrucción. El conocimiento vigente que aportaban está consolidado en `MCP_LAB_DOCUMENTATION.md`.

## ✅ Resultado en una frase

Se validó una **PoC MCP local** en Python/FastMCP que Claude Desktop pudo descubrir e invocar, se probaron capacidades EAM con datos simulados y el servidor evolucionó hasta **14 Tools**; **no se validó una conexión viva ni operaciones reales contra IBM Maximo**.

## 🧠 Cinco ideas para recordar

- MCP conecta una aplicación de IA con capacidades externas mediante un protocolo estándar.
- Host, Client y Server son roles distintos; el Host no es simplemente el PC.
- MCP no convierte por sí solo un LLM en agente autónomo.
- MCP puede situarse por encima de APIs/OSLC de Maximo; no las reemplaza necesariamente.
- El patrón `proponer → revisar → confirmar` explorado con Working Set es especialmente relevante para acciones EAM con impacto.

## 🔗 Relación con AI-EAM-MAXIMO

```text
Learning Lab MCP
      ↓
aprendizaje / evidencia
      ↓
🟨 CANDIDATO A INCORPORAR
      ↓ revisión explícita
AI-EAM-MAXIMO
```

Nada del laboratorio se convierte automáticamente en requisito, arquitectura o implementación del producto.

## 🚀 Siguiente tema

➡️ **RAG (Retrieval-Augmented Generation)** será el siguiente laboratorio independiente cuando se inicie su estudio práctico.
