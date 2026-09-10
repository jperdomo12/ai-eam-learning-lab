# 🔌 MCP — Model Context Protocol

> 🎯 **Objetivo:** aprender MCP de forma práctica con foco EAM / IBM Maximo y conservar evidencia suficiente para poder reconstruir el trabajo meses después.
> 📍 **Estado:** ✅ CERRADO para el alcance actual de aprendizaje
> 🗓️ **Actualizado:** 2026-09-10

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Se establece `docs/history/MCP_HISTORICAL_LAB.md` como registro canónico completo del laboratorio MCP histórico. |
| 2026-09-10 | Cierre del laboratorio MCP y enlace al recorrido práctico. |
| 2026-09-10 | Creación del área MCP. |

## 📚 Por dónde empezar

Para entender qué se hizo, leer en este orden:

1. [`docs/history/MCP_HISTORICAL_LAB.md`](docs/history/MCP_HISTORICAL_LAB.md) — **documento canónico y autosuficiente**: objetivo, evolución, instalaciones, configuración, código, pruebas, 14 tools verificadas, incidencias, evidencia, reproducción, limitaciones, aprendizajes y razones del traslado al Learning Lab.
2. [`docs/MCP_PRACTICAL_WALKTHROUGH.md`](docs/MCP_PRACTICAL_WALKTHROUGH.md) — recorrido práctico más corto para repasar rápidamente la ejecución.
3. [`docs/MCP_LAB_HANDOFF.md`](docs/MCP_LAB_HANDOFF.md) — estado de cierre y continuidad hacia el siguiente laboratorio.
4. Código histórico real: `jperdomo12/Maximo-IA-Project/maximo_mcp.py` — evidencia principal de la implementación.

> **Regla:** si existe discrepancia entre una descripción histórica y el código conservado, prevalece la evidencia del código para describir qué se implementó realmente.

## ✅ Qué se logró

Existe evidencia suficiente de una PoC MCP real con:

- servidor local Python/FastMCP;
- ejecución de tools desde Claude Desktop;
- modo simulación para trabajar sin Maximo real;
- evolución a VS Code + Cline;
- configuración histórica de Maximo MCP + Filesystem MCP + GitHub MCP;
- catálogo de **14 tools verificado en el código real**;
- experimentación con lectura, escritura, workflow y preview/confirmación de cambios.

## ❌ Qué no se validó

No se considera probado:

- conexión con una instancia viva de IBM Maximo;
- lectura o escritura real contra Maximo;
- validez actual de todas las configuraciones históricas de Claude/Cline;
- seguridad productiva de la PoC;
- incorporación automática de estos patrones a AI-EAM-MAXIMO.

## 🧠 Aprendizaje central

MCP permite que una aplicación de IA descubra y utilice capacidades externas mediante un protocolo estándar. En el caso de Maximo, esas capacidades pueden encapsular operaciones EAM mientras OSLC/REST u otros servicios siguen ejecutando la integración real por debajo.

MCP no convierte por sí mismo a un LLM en un agente autónomo y no sustituye necesariamente las APIs existentes.

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

Nada de este laboratorio se convierte automáticamente en decisión o implementación del producto.

## 🚀 Siguiente paso

➡️ Abrir el laboratorio de **RAG (Retrieval-Augmented Generation)** manteniendo la misma filosofía: aprender haciendo, avanzar rápido y documentar de forma que el trabajo pueda retomarse meses después sin depender del chat.
