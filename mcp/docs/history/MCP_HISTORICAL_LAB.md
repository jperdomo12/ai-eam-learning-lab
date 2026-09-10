# 🕰️ Laboratorio histórico — MCP + IBM Maximo

> ⚠️ **HISTÓRICO — material de referencia.** Este documento reconstruye el laboratorio realizado previamente con Gemini, Claude Desktop y Cline. No constituye por sí solo arquitectura vigente de AI-EAM-MAXIMO ni afirma que todo el código histórico siga funcionando actualmente.

> 🎯 **Objetivo:** dejar una fotografía comprensible de qué se construyó, qué productos se usaron/configuraron y qué quedó realmente validado antes de reiniciar el aprendizaje de MCP.
> 📍 **Estado:** reconstruido desde la documentación histórica; pendiente auditoría del código/configuración local original.
> 🗓️ **Actualizado:** 2026-09-10

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Creación inicial a partir del HandOff, bitácora y guía histórica del laboratorio Gemini/Claude/Cline. |

---

## 🎯 1. Qué queríamos aprender y probar

El laboratorio nació para explorar, de forma práctica, cómo una IA generativa podía interactuar con **IBM Maximo** mediante lenguaje natural y, posteriormente, para comprender **MCP (Model Context Protocol)** construyendo una PoC local.

Al no disponer de un entorno vivo de Maximo para estas pruebas, se adoptó un enfoque desacoplado con **datos simulados**. La meta inmediata dejó de ser construir un producto y pasó a ser comprobar el mecanismo completo:

```text
Usuario
  ↓ lenguaje natural
Aplicación de IA
  ↓ MCP
Servidor MCP local
  ↓ tool
Código Python
  ↓
Dato simulado / futura API Maximo
```

La primera prueba relevante fue deliberadamente sencilla: conseguir que Claude pudiera descubrir e invocar una tool local llamada `verificar_conexion`.

---

## 🧭 2. Evolución del laboratorio

### Etapa A — exploración inicial con Gemini / Google Cloud

El trabajo comenzó explorando una solución basada en Gemini y servicios Google Cloud / Vertex AI. La documentación histórica registra que este camino se percibió como innecesariamente complejo para una PoC personal por la infraestructura, endpoints y conectividad requeridos.

### Etapa B — Claude Desktop + servidor MCP local

Se cambió a una arquitectura local utilizando **Claude Desktop** como aplicación de IA con soporte MCP y un servidor propio escrito en Python.

El hito que sí quedó documentado como ejecutado fue:

```text
Claude Desktop
      ↓ MCP
maximo_mcp.py
      ↓
verificar_conexion()
      ↓
respuesta devuelta a Claude
```

Esta prueba demostró que una conversación podía terminar ejecutando una función Python expuesta como tool MCP.

### Etapa C — VS Code + Cline

Posteriormente el entorno de desarrollo se trasladó hacia **Visual Studio Code + Cline**. La motivación documentada fue acelerar el ciclo de aprendizaje: Cline podía inspeccionar archivos, proponer/realizar cambios, mostrar diffs y ejecutar comandos desde el entorno de desarrollo.

### Etapa D — “Tridente MCP”

La configuración se amplió a tres servidores MCP en paralelo:

```text
                  ┌─ Maximo MCP ───── maximo_mcp.py
Cline / Claude ───┼─ Filesystem MCP ─ archivos locales
                  └─ GitHub MCP ───── repositorios GitHub
```

El término **“Tridente MCP”** fue un nombre informal utilizado durante el laboratorio; no es terminología oficial del estándar MCP.

---

## 🧰 3. Productos y tecnologías utilizadas

| Producto / tecnología | Papel en el laboratorio | Evidencia histórica |
|---|---|---|
| **Gemini** | Apoyo inicial de razonamiento/desarrollo y primera exploración cloud | Documentado |
| **Google Cloud / Vertex AI** | Arquitectura inicialmente considerada y luego abandonada para la PoC local | Documentado |
| **Claude Desktop** | Aplicación de IA utilizada para la primera ejecución MCP validada | ✅ Prueba documentada |
| **Visual Studio Code** | IDE principal en la etapa posterior | Documentado |
| **Cline** | Extensión/agente dentro de VS Code para trabajar con código y servidores MCP | Documentado |
| **Python** | Runtime del servidor MCP propio | ✅ Utilizado |
| **FastMCP / SDK MCP Python** | Framework para exponer las tools del servidor | ✅ Utilizado |
| **requests** | Cliente HTTP previsto para OSLC/REST de Maximo | Implementado en la estructura histórica |
| **urllib3** | Gestión de advertencias SSL en el código histórico | Implementado en la estructura histórica |
| **Node.js / npx** | Runtime usado para servidores MCP de comunidad | Documentado |
| **Filesystem MCP** | Acceso delimitado a archivos locales | Configurado según documentación histórica |
| **GitHub MCP** | Acceso a repositorios GitHub | Configurado según documentación histórica |
| **IBM Maximo** | Sistema EAM objetivo de la integración | ⚠️ No hubo conexión viva validada |

---

## ⚙️ 4. Configuraciones realizadas

### 4.1 Windows + Python

Se instaló Python y fue necesario corregir el `PATH` de Windows porque inicialmente `python`/`pip` no eran reconocidos desde terminal.

### 4.2 Claude Desktop

El cliente fue configurado mediante `claude_desktop_config.json` para arrancar el servidor Python local. La instalación utilizada provenía de Windows Store, por lo que la ruta real de configuración resultó distinta de la inicialmente esperada.

Configuración conceptual utilizada:

```json
{
  "mcpServers": {
    "maximo": {
      "command": "python",
      "args": ["-u", "<RUTA_LOCAL>/maximo_mcp.py"]
    }
  }
}
```

> 🔐 Las rutas personales y cualquier credencial real se omiten deliberadamente en este repositorio público.

### 4.3 Cline

La documentación histórica identifica como archivo de configuración de Cline:

```text
%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
```

Su configuración fue ampliada para registrar varios servidores MCP.

### 4.4 Configuración multi-servidor

La estructura conceptual del “Tridente” fue:

```json
{
  "mcpServers": {
    "maximo": {
      "command": "<PYTHON>",
      "args": ["-u", "<RUTA>/maximo_mcp.py"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "<DIRECTORIO_AUTORIZADO>"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<SECRET>"
      }
    }
  }
}
```

Este ejemplo solo preserva el patrón histórico. **No debe utilizarse como recomendación actual de seguridad o configuración** sin revisarlo contra la versión vigente de MCP y de los productos implicados.

---

## 🧠 5. Producto técnico principal: `maximo_mcp.py`

El artefacto central fue un servidor MCP local escrito en Python.

Su idea principal era una **lógica dual**:

```text
MODO_SIMULACION = True
        ↓
retorna datos simulados

MODO_SIMULACION = False
        ↓
llamada HTTP / OSLC / REST
        ↓
IBM Maximo
```

Esto permitía estudiar MCP y diseñar tools sin depender de una VPN o instancia Maximo disponible.

La estructura documentada utilizaba `FastMCP`, decoradores `@mcp.tool()` y `mcp.run()` para arrancar el servidor.

---

## 🛠️ 6. Tools Maximo documentadas

El laboratorio comenzó con pocas tools y la documentación posterior afirma una expansión hasta **14**. Sin embargo, las fuentes históricas presentan pequeñas inconsistencias en nombres/orden del catálogo. Por eso, hasta auditar el archivo real `maximo_mcp.py`, el número y catálogo final deben considerarse **documentados históricamente, no todavía verificados contra código**.

Entre las capacidades descritas aparecen:

- consultar órdenes de trabajo;
- consultar inventario;
- consultar activos;
- consulta genérica de Object Structures con filtros OSLC;
- listar Object Structures;
- crear OT;
- preparar, confirmar y cancelar cambios mediante un concepto de Working Set;
- consultar y responder asignaciones de Workflow;
- verificar la conexión/catálogo de tools.

La documentación también describe una investigación con GitHub MCP sobre otros servidores Maximo MCP y una posterior ampliación del script local. Esa evolución debe auditarse antes de tratarla como código reproducible.

---

## 🧪 7. Qué quedó realmente probado

### ✅ COMPROBADO por la documentación histórica

- Python quedó operativo después de corregir el `PATH`.
- Se creó y ejecutó un servidor MCP local en Python.
- Claude Desktop descubrió/invocó al menos la tool `verificar_conexion`.
- Se utilizó el patrón de modo simulación para responder sin Maximo real.

### 🟦 DOCUMENTADO / CONFIGURADO, pendiente de reproducir

- VS Code + Cline como entorno operativo posterior.
- Configuración conjunta Maximo MCP + Filesystem MCP + GitHub MCP.
- Expansión del servidor hasta un catálogo histórico de 14 tools.
- Uso de GitHub MCP para investigar implementaciones externas y evolucionar el script.

### ❌ NO VALIDADO

- Conexión real con una instancia viva de IBM Maximo.
- Escrituras reales en Maximo.
- Funcionamiento actual del código con las versiones actuales de MCP/Cline/Claude.
- RAG sobre manuales técnicos.

---

## 🧯 8. Problemas encontrados y aprendizajes

**PATH de Python.** La instalación no quedó inicialmente disponible desde terminal; se corrigieron las variables de entorno.

**Ruta de configuración de Claude Desktop.** Se editó inicialmente una ubicación incorrecta. La ruta correcta se identificó desde la propia opción de edición de configuración de Claude Desktop.

**Simulación antes que integración real.** El modo simulado permitió separar el aprendizaje del protocolo de la disponibilidad de Maximo.

**IDE + agente para iterar.** Cline permitió un ciclo de modificación/prueba más cómodo que trabajar exclusivamente desde una interfaz de chat.

---

## 🔐 9. Nota de seguridad actual

Los documentos históricos contenían ejemplos de PAT, API keys y rutas locales. En este Learning Lab público:

- nunca se versionarán secretos reales;
- las configuraciones se sanitizarán antes de incorporarlas;
- los tokens se representarán mediante variables de entorno o placeholders;
- no se publicarán endpoints internos ni datos corporativos.

---

## 🔗 10. Relación con AI-EAM-MAXIMO

Este laboratorio histórico es **antecedente y material de aprendizaje**, no la arquitectura oficial del producto actual.

```text
Laboratorio histórico MCP
          ↓
comprender + reproducir + auditar
          ↓
aprendizajes válidos
          ↓
🟨 CANDIDATO A INCORPORAR
          ↓ aprobación explícita
AI-EAM-MAXIMO
```

No debe copiarse mecánicamente el antiguo `maximo_mcp.py` al producto.

---

## 🚀 11. Próximo paso del Learning Lab

Antes de iniciar nuevos conceptos MCP, cerrar correctamente esta experiencia previa:

1. localizar los artefactos originales disponibles (`maximo_mcp.py` y configuraciones);
2. sanitizarlos antes de incorporarlos al repositorio público;
3. auditar qué contiene realmente el código;
4. reproducir la PoC mínima;
5. registrar qué sigue funcionando y qué quedó obsoleto;
6. cerrar el laboratorio histórico y comenzar el estudio MCP actual desde una base limpia.

---

## 🔗 12. Fuentes históricas utilizadas

- `MCP_HANDOFF_GEMINI_A_CHATGPT.md` — HandOff generado para transferir el trabajo previo.
- `Bitácora de Proyecto: IA Generativa + MCP para IBM Maximo` — evolución histórica del laboratorio.
- `Guía de Configuración Avanzada: Cline + MCP (Maximo, Filesystem y GitHub)` — configuración y operación del entorno posterior.

Estas fuentes se conservan fuera de este documento como evidencia histórica y deberán importarse sanitizadas únicamente si aportan valor al aprendizaje futuro.
