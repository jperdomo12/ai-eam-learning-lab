# 🧭 MCP_LAB_HANDOFF

> 📍 **Estado:** ✅ CERRADO — laboratorio MCP completado para el alcance actual y consolidado en el Learning Lab
> 🗓️ **Actualizado:** 2026-09-10

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Se adopta `MCP_LAB_DOCUMENTATION.md` como documento principal; el código `maximo_mcp.py` y la configuración sanitizada de Claude quedan preservados dentro del propio Learning Lab. |
| 2026-09-10 | Consolidación del trabajo previo realizado con Gemini / Claude Desktop / VS Code + Cline. |
| 2026-09-10 | Creación del HandOff inicial. |

## Dónde estamos

El laboratorio MCP está **cerrado para el alcance actual de aprendizaje**.

El traslado a `ai-eam-learning-lab` no inicia un proyecto nuevo: consolida y continúa el trabajo realizado previamente con Gemini, Claude Desktop y Cline bajo un modelo ChatGPT ↔ GitHub más organizado y persistente.

## Documento principal

La fuente documental vigente del laboratorio es:

```text
mcp/docs/MCP_LAB_DOCUMENTATION.md
```

Debe contener la versión consolidada y actualizada de todo el trabajo MCP realizado, independientemente del chat o herramienta donde se originó.

Los documentos previos de Gemini / Claude / Cline conservados bajo `history/` son **material de referencia y transición**, no la documentación vigente. Pueden eliminarse en el futuro cuando todo su conocimiento útil esté absorbido y verificado en la documentación principal.

## Artefactos preservados

### Código

```text
mcp/src/maximo_mcp.py
```

Es la copia recuperada de la PoC MCP orientada a IBM Maximo. Confirma:

- servidor Python/FastMCP;
- `MODO_SIMULACION = True`;
- datos mock de OT, inventario, activos, workflow y Object Structures;
- rama OSLC/REST preparada;
- 14 Tools MCP;
- Working Set temporal para preview → confirmar/cancelar.

### Configuración Claude Desktop

```text
mcp/config/claude_desktop_config.example.json
```

Es una versión sanitizada de la configuración real obtenida desde:

```text
Claude Desktop → Configuración → Desarrollador → Editar configuración
```

La copia real aportada por el usuario confirmó la configuración simultánea de:

- Maximo MCP;
- Filesystem MCP;
- GitHub MCP.

No se conserva en GitHub la copia cruda porque el repositorio es público y contiene rutas/personales y campos sensibles de entorno.

## Qué quedó probado / recuperado

- ejecución de un MCP Server local con Python/FastMCP;
- invocación histórica de Tools desde Claude Desktop;
- modo simulación para capacidades EAM;
- evolución a VS Code + Cline;
- entorno multi-MCP Maximo + Filesystem + GitHub;
- catálogo de 14 Tools recuperado en código;
- pruebas EAM simuladas;
- experimentación con Working Set / confirmación humana.

## Qué NO quedó validado

- conexión con una instancia viva de IBM Maximo;
- lectura/escritura real contra Maximo;
- workflow real contra Maximo;
- seguridad productiva;
- compatibilidad exacta actual de toda la configuración histórica.

## Relación con AI-EAM-MAXIMO

El Learning Lab conserva aprendizaje y evidencia. Cualquier patrón que deba trasladarse al producto `jperdomo12/ai-driven-eam-copilot` se tratará allí como **🟨 CANDIDATO A INCORPORAR** y seguirá su gobernanza formal.

## Próximo laboratorio

➡️ **RAG (Retrieval-Augmented Generation)**, una vez finalizada la depuración documental de MCP.
