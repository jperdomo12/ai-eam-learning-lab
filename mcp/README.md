# 🔌 MCP — Model Context Protocol

> 🎯 **Objetivo:** aprender MCP de forma práctica con foco EAM / IBM Maximo y conservar una memoria técnica completa, actualizada y reutilizable.
> 📍 **Estado:** ✅ CERRADO para el alcance actual de aprendizaje
> 🗓️ **Actualizado:** 2026-09-10

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Se adopta `docs/MCP_LAB_DOCUMENTATION.md` como documentación principal y vigente del laboratorio; se incorporan al Learning Lab el código `src/maximo_mcp.py` y la configuración sanitizada en `config/`. |
| 2026-09-10 | Consolidación inicial del laboratorio MCP trasladado desde Gemini / Claude / Cline. |
| 2026-09-10 | Creación del área MCP. |

## 📚 Por dónde empezar

Para entender el laboratorio MCP, leer en este orden:

1. [`docs/MCP_LAB_DOCUMENTATION.md`](docs/MCP_LAB_DOCUMENTATION.md) — **documentación principal y vigente**. Integra todo el recorrido desde Gemini / Claude / Cline hasta la consolidación actual en ChatGPT ↔ GitHub.
2. [`docs/MCP_LAB_HANDOFF.md`](docs/MCP_LAB_HANDOFF.md) — estado de cierre y continuidad.
3. [`src/maximo_mcp.py`](src/maximo_mcp.py) — código de la PoC MCP orientada a IBM Maximo recuperado como artefacto del propio Learning Lab.
4. [`config/claude_desktop_config.example.json`](config/claude_desktop_config.example.json) — versión sanitizada de la configuración real de Claude Desktop.

La carpeta `docs/history/` contiene únicamente material de referencia usado para reconstruir el trabajo anterior. **No es la documentación vigente del laboratorio** y podrá reducirse o eliminarse cuando dejemos de necesitarla como respaldo de transición.

## ✅ Qué se logró

Existe evidencia de una PoC MCP con:

- servidor local Python/FastMCP;
- ejecución de Tools desde Claude Desktop;
- modo simulación para trabajar sin Maximo real;
- evolución a VS Code + Cline;
- configuración de Maximo MCP + Filesystem MCP + GitHub MCP;
- catálogo de **14 Tools** recuperado en el código;
- experimentación con lectura, escritura simulada, workflow y preview/confirmación de cambios.

## ❌ Qué no se validó

No se considera probado:

- conexión con una instancia viva de IBM Maximo;
- lectura o escritura real contra Maximo;
- workflow real contra Maximo;
- seguridad productiva de la PoC;
- compatibilidad actual exacta de todas las configuraciones históricas;
- incorporación automática de estos patrones a AI-EAM-MAXIMO.

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

Nada del laboratorio se convierte automáticamente en decisión o implementación del producto.

## 🚀 Siguiente paso

➡️ Tras cerrar la consolidación documental de MCP, abrir el laboratorio de **RAG (Retrieval-Augmented Generation)** con el mismo modelo: aprender haciendo y mantener la documentación actualizada directamente en GitHub.
