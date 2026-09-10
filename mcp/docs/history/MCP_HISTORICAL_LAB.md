# 🕰️ Laboratorio histórico — MCP + IBM Maximo

> ⚠️ **HISTÓRICO — material de referencia.** Reconstruye el laboratorio previo con Gemini, Claude Desktop y Cline. No constituye arquitectura vigente de AI-EAM-MAXIMO.

> 🎯 **Objetivo:** conservar qué se construyó, configuró y aprendió antes de continuar el estudio actual de MCP.
> 📍 **Estado:** documentación histórica revisada y `maximo_mcp.py` histórico localizado/auditado en `jperdomo12/Maximo-IA-Project`. Pendiente únicamente reproducir el laboratorio con el stack actual.
> 🗓️ **Actualizado:** 2026-09-10

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Verificado el artefacto real `maximo_mcp.py`: lógica dual y catálogo de 14 tools. |
| 2026-09-10 | Creación inicial desde HandOff, bitácora y guía histórica Gemini/Claude/Cline. |

---

## 🎯 1. Qué se quería probar

Explorar de forma práctica cómo una IA generativa podía interactuar con **IBM Maximo** mediante lenguaje natural usando MCP, primero sin depender de un Maximo real.

```text
Usuario → Claude/Cline → MCP → maximo_mcp.py → simulación / OSLC REST → IBM Maximo
```

La PoC comenzó con Claude Desktop y evolucionó a VS Code + Cline.

---

## 🧭 2. Evolución

**Gemini / Google Cloud.** Se exploró inicialmente una arquitectura cloud, descartada para la PoC por complejidad innecesaria.

**Claude Desktop.** Se configuró un servidor MCP Python local y se documentó la ejecución de `verificar_conexion` desde la conversación.

**VS Code + Cline.** Se trasladó el laboratorio al IDE para editar código, ejecutar comandos y refrescar servidores MCP con mayor agilidad.

**“Tridente MCP”.** Se configuraron tres servidores en paralelo:

```text
Cline
 ├─ Maximo MCP ─── maximo_mcp.py
 ├─ Filesystem MCP
 └─ GitHub MCP
```

“Tridente MCP” fue terminología informal del laboratorio, no del estándar MCP.

---

## 🧰 3. Productos y configuración

| Componente | Uso histórico |
|---|---|
| Gemini | Exploración inicial y apoyo al desarrollo |
| Claude Desktop | Primer host/aplicación usada para la PoC MCP |
| VS Code + Cline | Entorno posterior de desarrollo y experimentación |
| Python + FastMCP | Implementación del servidor MCP propio |
| `requests` + `urllib3` | Acceso HTTP previsto a OSLC/REST Maximo |
| Node.js / `npx` | Ejecución de servidores MCP adicionales |
| Filesystem MCP | Acceso controlado a archivos locales |
| GitHub MCP | Investigación y trabajo con repositorios |
| IBM Maximo | Sistema EAM objetivo; conexión viva no validada |

Configuraciones históricas relevantes:

- Claude Desktop: `claude_desktop_config.json` lanzaba `python -u <ruta>/maximo_mcp.py`.
- Cline: `cline_mcp_settings.json` registraba Maximo, Filesystem y GitHub MCP.
- El antiguo GitHub MCP utilizaba PAT en configuración; **ese patrón no se adopta como recomendación actual**.
- El repositorio público actual nunca debe contener secretos, endpoints privados ni datos corporativos.

---

## 🧠 4. Artefacto real localizado: `maximo_mcp.py`

El código histórico existe en `jperdomo12/Maximo-IA-Project` y confirma:

- `FastMCP("Maximo Enterprise")`;
- `MODO_SIMULACION = True`;
- mocks de OT, inventario, activos, workflow y Object Structures;
- rama de lógica real mediante HTTP/OSLC;
- `MAXIMO_URL` y `API_KEY` como placeholders, no credenciales reales;
- catálogo real de **14 tools**.

Por tanto, la anterior duda documental sobre si realmente se había llegado a 14 tools queda **resuelta por el código**.

### Las 14 tools verificadas

| # | Tool | Qué hace |
|---:|---|---|
| 1 | `consultar_ot` | Consulta una OT y sus datos principales. |
| 2 | `consultar_inventario` | Consulta stock/ubicación de un artículo. |
| 3 | `listar_transiciones_ot` | Muestra cambios de estado permitidos. |
| 4 | `cambiar_estado_ot` | Cambia estado de una OT, validando transición. |
| 5 | `query_maximo` | Consulta genérica de Object Structures vía OSLC. |
| 6 | `consultar_activo` | Consulta datos de un activo. |
| 7 | `listar_object_structures` | Descubre Object Structures disponibles. |
| 8 | `crear_ot` | Crea una OT. |
| 9 | `ws_editar_ot` | Prepara cambios de OT mediante Working Set/preview. |
| 10 | `ws_confirmar_cambios` | Confirma un Working Set. |
| 11 | `ws_cancelar_cambios` | Descarta un Working Set. |
| 12 | `obtener_workflow_assignments` | Consulta asignaciones de workflow. |
| 13 | `enviar_workflow_response` | Responde a una asignación de workflow. |
| 14 | `verificar_conexion` | Verifica el servidor/conexión y presenta las tools. |

### Patrón técnico más interesante

El script no era solo una demo de lectura. Ya exploraba tres tipos de interacción:

```text
READ
consultar_ot / activo / inventario / query_maximo

WRITE
crear_ot / cambiar_estado_ot

HUMAN-IN-THE-LOOP EXPERIMENTAL
ws_editar_ot → preview → confirmar o cancelar
```

Este último patrón es especialmente relevante como aprendizaje EAM, aunque no debe asumirse automáticamente como diseño vigente del producto AI-EAM-MAXIMO.

---

## 🧪 5. Estado de evidencia

### ✅ VERIFICADO

- Existe el servidor histórico `maximo_mcp.py`.
- Usa FastMCP y `@mcp.tool()`.
- Contiene exactamente 14 tools.
- Implementa modo simulación con datos mock.
- Contiene lógica prevista para OSLC/REST real.
- La documentación registra ejecución MCP desde Claude Desktop.
- La documentación registra la evolución a Cline y configuración Maximo + Filesystem + GitHub MCP.

### ⚠️ DOCUMENTADO, NO REPRODUCIDO HOY

- Que la configuración histórica de Cline siga funcionando con las versiones actuales.
- Que los antiguos servidores Filesystem/GitHub MCP se configuren hoy de la misma forma.
- El comportamiento exacto de hot reload/refresh con la versión actual de Cline.

### ❌ NO VALIDADO HISTÓRICAMENTE

- Conexión con una instancia viva de IBM Maximo.
- Escrituras reales en Maximo.
- RAG sobre documentación técnica.

---

## 💡 6. Qué aprendimos y qué conservamos

📘 **MCP separa la conversación de las capacidades externas.** El modelo no necesita contener la lógica Maximo: descubre tools expuestas por un servidor MCP.

📘 **La simulación desacopla el aprendizaje de la infraestructura.** Fue posible estudiar MCP sin VPN ni Maximo disponible.

📘 **Una tool puede encapsular semántica EAM.** No se expuso únicamente HTTP genérico; aparecieron operaciones como consultar OT, transición de estado, inventario y workflow.

📘 **La confirmación antes de escribir ya apareció en el laboratorio.** El Working Set fue un primer experimento de preview → confirmar/cancelar.

📘 **Múltiples servidores MCP pueden aportar capacidades distintas al mismo entorno.** Maximo, filesystem y GitHub fueron combinados en Cline.

---

## 🔗 7. Relación con AI-EAM-MAXIMO

```text
Learning Lab
   ↓ aprender / reproducir / comparar
🟨 CANDIDATO A INCORPORAR
   ↓ decisión explícita
ai-driven-eam-copilot
```

El código histórico es evidencia y material didáctico. **No se copia automáticamente al producto.**

---

## 🚀 8. Siguiente paso

La reconstrucción histórica queda suficientemente cerrada. No necesitamos seguir documentándola antes de aprender.

**Siguiente experimento:** reproducir una PoC MCP mínima con el stack actual, empezando por una sola tool sencilla. A partir de esa ejecución iremos refrescando conceptos MCP modernos y comparándolos con lo que se hizo históricamente.

---

## 🔗 9. Fuentes

- Código histórico: `jperdomo12/Maximo-IA-Project/maximo_mcp.py`.
- `Bitácora de Proyecto: IA Generativa + MCP para IBM Maximo`.
- `Guía de Configuración Avanzada: Cline + MCP (Maximo, Filesystem y GitHub)`.
- HandOff histórico Gemini → ChatGPT.
