# 🧭 MCP_LAB_HANDOFF

> 📍 **Estado:** ⏸️ **PAUSADO — revalidación práctica MCP retomada; GitHub MCP pendiente (#1)**
> 🗓️ **Actualizado:** 2026-09-10

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Se reabre el laboratorio práctico para refrescar y revalidar la configuración histórica. Maximo MCP y Filesystem MCP continúan operativos; la recuperación de GitHub MCP en Claude Desktop queda **PENDIENTE** en el issue [#1](https://github.com/jperdomo12/ai-eam-learning-lab/issues/1). |
| 2026-09-10 | Se cierra la consolidación documental con `MCP_LAB_DOCUMENTATION.md` v1.1 y `MCP_LAB_FAST_READING.md` como entrada rápida. |
| 2026-09-10 | Se adopta `MCP_LAB_DOCUMENTATION.md` como documento principal; el código `maximo_mcp.py` y la configuración sanitizada de Claude quedan preservados dentro del propio Learning Lab. |
| 2026-09-10 | Consolidación del trabajo previo realizado con Gemini / Claude Desktop / VS Code + Cline. |
| 2026-09-10 | Creación del HandOff inicial. |

## Dónde estamos

La **baseline documental MCP está consolidada y cerrada**, pero posteriormente se retomó una **revalidación práctica** para refrescar el laboratorio histórico antes de continuar con nuevos temas.

Estado actual de esa revalidación:

- ✅ Maximo MCP continúa configurado y operativo en Claude Desktop.
- ✅ Filesystem MCP continúa configurado y operativo en Claude Desktop.
- ⏸️ GitHub MCP queda pendiente de recuperación/reconfiguración en la versión actual de Claude Desktop: issue [#1 — Recuperar GitHub MCP en Claude Desktop actual](https://github.com/jperdomo12/ai-eam-learning-lab/issues/1).
- ⏸️ No continuar todavía con la revalidación completa desde VS Code + Cline hasta cerrar o decidir conscientemente diferir el issue #1.

El traslado a `ai-eam-learning-lab` no inicia un proyecto nuevo: consolida y continúa el trabajo realizado previamente con Gemini, Claude Desktop y Cline bajo un modelo ChatGPT ↔ GitHub más organizado y persistente.

La documentación cruda previa queda como material de referencia de transición; el conocimiento vigente ya está absorbido en la documentación del Learning Lab.

## Issue activo

### #1 — Recuperar GitHub MCP en Claude Desktop actual

**Estado:** ⏸️ PENDIENTE / PAUSADO.

Durante la revalidación del 2026-09-10 se comprobó que la configuración histórica de GitHub MCP ya no se recupera de forma estable en Claude Desktop actual. Entre los hechos observados:

- el archivo efectivo sigue siendo el `claude_desktop_config.json` de la instalación Windows Store;
- Claude Desktop reescribe ese archivo al arrancar;
- antes de limpiar la configuración, reaparecía el PAT histórico ya revocado;
- se identificó y detuvo de forma aislada el árbol de procesos de GitHub MCP sin afectar Maximo ni Filesystem;
- al eliminar `github` desde `Configuración → Desarrollador`, Claude eliminó correctamente su bloque del JSON;
- tras reiniciar, GitHub MCP dejó de aparecer y el bloque sigue ausente;
- en `Configuración → Conectores` no aparece actualmente una opción GitHub;
- un intento posterior de reinserción manual contenía un JSON inválido por falta de una coma, por lo que no constituye una prueba válida de fallo de una reinserción limpia.

El detalle técnico, evidencias, hipótesis, próximos pasos y criterio de cierre están registrados en el issue #1. **No crear un PAT adicional ni modificar Maximo/Filesystem al retomar.**

## Documentos vigentes

Para recuperar el laboratorio:

```text
mcp/docs/MCP_LAB_FAST_READING.md      ← recuperación rápida
mcp/docs/MCP_LAB_DOCUMENTATION.md     ← fuente completa y canónica
mcp/docs/MCP_LAB_HANDOFF.md           ← estado y continuidad
```

`MCP_LAB_DOCUMENTATION.md` contiene el recorrido completo: objetivo, conceptos MCP, cronología, instalaciones, configuración, comunicación JSON-RPC/stdio, Claude Desktop, VS Code + Cline, Tridente MCP, código, 14 Tools, pruebas, Working Set, evidencia, límites y relación con RAG / AI-EAM-MAXIMO.

## Artefactos preservados

```text
mcp/src/maximo_mcp.py
mcp/src/history/connection_test.py
mcp/src/history/maximo_mcp_gemini_v1.py
mcp/config/claude_desktop_config.example.json
```

El código final confirma servidor Python/FastMCP, `MODO_SIMULACION = True`, datos mock, rama OSLC/REST preparada, 14 Tools y Working Set temporal.

La configuración Claude sanitizada deriva del archivo real obtenido desde:

```text
Claude Desktop → Configuración → Desarrollador → Editar configuración
```

y conserva como evidencia la configuración histórica Maximo MCP + Filesystem MCP + GitHub MCP. Su compatibilidad exacta con Claude Desktop actual está siendo revalidada y el punto pendiente concreto está en el issue #1.

## Qué quedó probado históricamente

- ejecución de un MCP Server local con Python/FastMCP;
- invocación histórica de Tools desde Claude Desktop;
- modo simulación para capacidades EAM;
- consultas y cambios de estado simulados;
- Filesystem MCP para listar/escribir archivos;
- uso histórico de GitHub MCP para investigar código;
- evolución a VS Code + Cline;
- entorno multi-MCP “Tridente”;
- catálogo final de 14 Tools recuperado en código;
- experimentación con Working Set / confirmación humana.

## Qué NO quedó validado

- conexión con una instancia viva de IBM Maximo;
- lectura/escritura real contra Maximo;
- workflow real contra Maximo;
- seguridad productiva;
- compatibilidad exacta actual de toda la configuración histórica;
- recuperación actual de GitHub MCP en Claude Desktop — **issue #1 pendiente**.

## Relación con AI-EAM-MAXIMO

El Learning Lab conserva aprendizaje y evidencia. Cualquier patrón que deba trasladarse al producto `jperdomo12/ai-driven-eam-copilot` se tratará allí como **🟨 CANDIDATO A INCORPORAR** y seguirá su gobernanza formal.

## Próximo paso

➡️ **Retomar el issue #1 con una sesión fresca**, investigando primero la documentación vigente de Claude Desktop / GitHub MCP y sin tocar Maximo MCP ni Filesystem MCP.

Después de cerrar o resolver conscientemente ese pendiente, continuar con la revalidación desde **VS Code + Cline** y posteriormente con el siguiente laboratorio de aprendizaje (**RAG**) cuando corresponda.
