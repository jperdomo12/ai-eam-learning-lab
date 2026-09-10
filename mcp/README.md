# 🔌 MCP — Model Context Protocol

> 🎯 **Objetivo:** aprender MCP de forma práctica, entendiendo primero lo realizado anteriormente y construyendo después experimentos reproducibles con foco EAM / IBM Maximo.
> 📍 **Estado:** reconstrucción y auditoría del trabajo histórico
> 🗓️ **Actualizado:** 2026-09-10

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Creación del área MCP y definición de la primera etapa de estudio. |

## 🧠 Qué queremos aprender

No buscamos únicamente saber “qué es MCP”. Queremos poder explicar y demostrar:

- qué problema resuelve MCP;
- qué responsabilidades tienen Host, Client y Server;
- qué son Tools, Resources y Prompts;
- cómo se descubre y ejecuta una capacidad;
- cómo funciona un transporte local como `stdio`;
- cómo se construye un MCP Server sencillo;
- cómo encaja MCP con APIs existentes;
- qué aporta —y qué no aporta— al uso de IA con IBM Maximo;
- qué decisiones del PoC histórico siguen siendo válidas hoy.

## 🗺️ Modelo de trabajo

El estudio se separa intencionalmente en cinco niveles:

```text
🟦 Trabajo histórico Gemini / Claude
              ↓
📘 Concepto general MCP
              ↓
🧪 Nuevo experimento reproducible
              ↓
🔧 Aplicación potencial a IBM Maximo
              ↓
🟨 Candidato a incorporar a AI-EAM-MAXIMO
```

Solo el último nivel puede llegar al producto y requiere revisión explícita allí.

## 🟦 Punto de partida histórico

Existe un PoC realizado anteriormente con herramientas como Python, Claude Desktop, VS Code + Cline y FastMCP.

La documentación histórica indica, entre otras cosas:

- ejecución de un MCP Server local en Python;
- uso de una herramienta `verificar_conexion`;
- estructura para trabajar en modo simulación / real;
- evolución hacia varias herramientas orientadas a Maximo;
- configuración posterior de Maximo MCP, Filesystem MCP y GitHub MCP.

Este material **todavía no se considera evidencia técnica vigente**. Antes de reutilizarlo debemos importar, revisar y clasificar código, configuraciones y resultados reales.

## ✅ Qué consideramos ya suficientemente sustentado

A partir del material disponible hasta ahora, existe evidencia histórica suficiente de que se logró al menos:

**AI/MCP client ↔ MCP Server local Python ↔ ejecución de una tool.**

Eso no demuestra todavía una integración real con IBM Maximo.

## ❌ Qué NO damos por demostrado

Por ahora no damos por verificado en este laboratorio:

- conexión contra una instancia real de IBM Maximo;
- operaciones reales de lectura o escritura en Maximo;
- validez actual de las 14 tools históricas;
- seguridad de configuraciones históricas;
- vigencia técnica de todas las explicaciones producidas en el trabajo anterior;
- RAG.

## 🧪 Primera etapa

La primera etapa será deliberadamente corta:

1. importar el material histórico útil;
2. separar documentación, código y configuración;
3. revisar secretos o datos sensibles antes de publicar;
4. auditar qué existe realmente;
5. reproducir el PoC mínimo;
6. registrar qué funciona hoy;
7. cerrar la reconstrucción histórica;
8. comenzar una secuencia limpia de aprendizaje MCP.

## 📂 Estructura inicial

```text
mcp/
├── README.md
├── docs/
│   └── MCP_LAB_HANDOFF.md
├── experiments/
└── history/
```

Las carpetas crecerán únicamente cuando exista contenido real que justificar.

## 🔧 Relación con IBM Maximo

IBM Maximo es nuestro contexto profesional principal, pero MCP se estudiará primero como tecnología general.

La pregunta no será solo “¿cómo conecto MCP a Maximo?”, sino también:

> **¿Qué capacidades EAM tiene sentido exponer mediante MCP y qué valor aporta frente a consumir directamente APIs/OSLC/servicios existentes?**

Las respuestas obtenidas aquí podrán convertirse en 🟨 **CANDIDATOS A INCORPORAR** al proyecto AI-EAM-MAXIMO, nunca en decisiones automáticas.

## 🚀 Siguiente paso

Importar y auditar el material histórico del PoC Gemini / Claude, empezando por los documentos y el código fuente disponible.
