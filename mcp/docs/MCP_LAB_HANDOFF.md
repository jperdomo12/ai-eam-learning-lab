# 🧭 MCP_LAB_HANDOFF

> 📍 **Estado:** inicialización del laboratorio MCP
> 🗓️ **Actualizado:** 2026-09-10

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Creación del HandOff inicial del laboratorio MCP. |

## Dónde estamos

Se creó el repositorio público `jperdomo12/ai-eam-learning-lab` como espacio general de aprendizaje práctico de IA aplicada a EAM.

MCP es el primer tema activo.

El laboratorio adopta una forma de trabajo ágil: aprender, experimentar, registrar solo lo importante y mantener una separación explícita respecto al producto AI-EAM-MAXIMO.

## Qué ya entendimos

Conceptualmente se ha aclarado que:

- MCP no convierte por sí mismo a un LLM en un agente autónomo;
- un MCP Host es la aplicación de IA que administra las conexiones MCP, no el PC físico;
- un MCP Server expone capacidades que pueden incluir Tools, Resources y Prompts;
- MCP puede actuar como una capa estandarizada sobre APIs y servicios existentes;
- una integración MCP con Maximo no implica necesariamente sustituir OSLC, REST u otras APIs subyacentes.

## Qué ya probamos históricamente

La evidencia histórica disponible indica que se llegó a ejecutar al menos un flujo:

```text
AI / MCP Client
      ↓
MCP Server local en Python
      ↓
tool verificar_conexion
```

También existen documentos que describen una ampliación posterior del PoC, pero todavía deben ser auditados contra código y configuraciones reales.

## Qué NO está demostrado todavía

No se considera probado en este laboratorio:

- conexión real con IBM Maximo;
- operaciones reales de lectura o escritura en Maximo;
- vigencia de todas las tools históricas;
- validez técnica actual de toda la documentación histórica;
- RAG;
- ninguna incorporación automática al producto AI-EAM-MAXIMO.

## Archivos clave

- `README.md` — entrada general al Learning Lab.
- `docs/DOCUMENTATION_STANDARD.md` — estándar documental ligero.
- `mcp/README.md` — panel principal del estudio MCP.
- `mcp/docs/MCP_LAB_HANDOFF.md` — continuidad de esta línea de aprendizaje.

## Próximo paso

Importar y auditar el material histórico del PoC Gemini / Claude.

La prioridad será recuperar evidencia real —documentos, código y configuración sanitizada— y clasificar cada elemento como histórico, probado, diseñado, inferido o pendiente antes de iniciar nuevos experimentos.
