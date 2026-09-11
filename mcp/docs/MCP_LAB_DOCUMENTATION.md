# 🔌 MCP LAB — Documentación consolidada

> 🎯 **Propósito:** ser la fuente canónica, autosuficiente y vigente del Learning Lab para todo lo aprendido, construido, configurado y probado sobre **Model Context Protocol (MCP)** aplicado a EAM / IBM Maximo.
>
> 📍 **Estado del documento:** ✅ **APROBADO — v1.2 final**
>
> 🧪 **Estado del laboratorio:** ✅ **CERRADO / CONGELADO para el alcance actual de aprendizaje MCP**
>
> 🗓️ **Actualizado:** 2026-09-12
>
> ⚠️ **Conclusión que no debe perderse:** se validó una PoC MCP local con datos simulados, 14 Tools EAM y composición entre varios MCP Servers; **no se validó una conexión viva ni operaciones reales contra IBM Maximo**.

## 🕘 Historial

| Versión | Fecha | Cambio |
|---|---:|---|
| **1.2** | 2026-09-12 | Cierre final del MCP LAB: revalidación completa en VS Code + Cline, recuperación de la configuración MCP efectiva, instalación/configuración de productos, pruebas Maximo y Filesystem individuales, prueba negativa/positiva de sandbox, composición Maximo + Filesystem, selección de Tools y comparación Claude Desktop vs Cline. Se incorpora configuración Cline sanitizada. |
| **1.1** | 2026-09-10 | Mejora de recuperación rápida: índice descriptivo, JSON/JSON-RPC, motivación Claude Desktop → Cline, “Tridente”, cronología consolidada y referencia al futuro laboratorio RAG. |
| **1.0** | 2026-09-10 | Consolidación integral del trabajo previo realizado con Gemini, Claude Desktop y Cline; preservación de código, configuración y aprendizaje histórico. |

---

# 0. Recuperación rápida

## 0.1 Qué queríamos aprender

Queríamos comprobar, **aprendiendo haciendo**, si una aplicación de IA podía recibir una petición en lenguaje natural, descubrir capacidades externas y ejecutar operaciones relacionadas con EAM / IBM Maximo mediante MCP.

La hipótesis de negocio original era reducir fricción administrativa en mantenimiento: consultar OTs, inventario y activos, y eventualmente registrar o modificar información sin navegar manualmente por múltiples pantallas.

La cifra histórica de **~30 % de reducción del tiempo administrativo** fue una hipótesis de valor, **no un beneficio medido**.

## 0.2 Qué construimos

```text
Usuario
  ↓ lenguaje natural
Host / entorno de IA
  ├─ Claude Desktop
  └─ VS Code + Cline
          ↓
       MCP Client
          ↓ stdio
  ┌───────┼───────────┐
  ↓       ↓           ↓
Maximo  Filesystem   GitHub
MCP     MCP          MCP histórico
  ↓
maximo_mcp.py
  ├─ datos simulados                ← PROBADO
  └─ HTTP/OSLC → IBM Maximo         ← PREPARADO, NO VALIDADO EN VIVO
```

La combinación de los tres servidores se llamó informalmente **“Tridente MCP”**. No es un término del estándar.

## 0.3 Qué quedó probado

- MCP Server local propio en Python/FastMCP;
- ejecución por transporte `stdio`;
- **14 Tools** Maximo visibles en Cline;
- `Resources (0)` y `Prompts (0)` en el servidor Maximo actual;
- consultas EAM sobre datos mock;
- selección autónoma de una Tool en una petición normal;
- selección controlada indicando explícitamente la Tool;
- Filesystem MCP con carpetas autorizadas;
- rechazo de acceso fuera del sandbox;
- ampliación del sandbox mediante configuración + `Restart Server`;
- composición **Maximo MCP + Filesystem MCP** en una sola tarea;
- creación de CSV desde Claude Desktop y desde Cline;
- uso histórico de GitHub MCP;
- Working Set experimental `preview → confirmar/cancelar`;
- diferencia entre capacidades MCP y capacidades nativas/terminal de un agente como Cline.

## 0.4 Qué NO quedó probado

- conexión a una instancia viva de IBM Maximo;
- lectura o escritura real contra Maximo;
- workflow real;
- seguridad/autorización empresarial;
- operación productiva;
- funcionamiento actual del GitHub MCP oficial en esta máquina;
- RAG.

## 0.5 Artefactos vigentes

```text
mcp/
├── README.md
├── src/
│   ├── maximo_mcp.py
│   └── history/
│       ├── connection_test.py
│       └── maximo_mcp_gemini_v1.py
├── config/
│   ├── claude_desktop_config.example.json
│   └── cline_mcp_settings.example.json
└── docs/
    ├── MCP_LAB_FAST_READING.md
    ├── MCP_LAB_DOCUMENTATION.md
    └── MCP_LAB_HANDOFF.md
```

---

# 1. Evolución del laboratorio

## 1.1 Gemini — exploración inicial

El trabajo comenzó explorando con Gemini una interfaz de IA sobre IBM Maximo. Para ejecutar herramientas locales se consideró una arquitectura con Google Cloud / Vertex AI, pero para una PoC local introducía más infraestructura, configuración y coste antes de haber validado el mecanismo básico.

La decisión fue mover la ejecución práctica a un Host con soporte MCP local más directo.

## 1.2 Claude Desktop — primera PoC MCP local

Claude Desktop permitió lanzar el servidor Python local y probar Tools sin desplegar un servicio web propio.

La primera prueba deliberadamente simple fue `verificar_conexion`: demostrar **Claude Desktop ↔ MCP Server Python**, no IBM Maximo real.

Después se añadieron capacidades de OTs, inventario, estados y otros escenarios EAM.

## 1.3 VS Code + Cline — desarrollo y experimentación

Cline se instaló como extensión de VS Code para reducir la fricción del ciclo:

```text
editar → revisar diff → aprobar → reiniciar MCP Server → probar
```

Cline añadió capacidades agénticas propias del IDE: lectura/escritura de archivos, terminal y comandos, además del uso de MCP.

Esto es importante:

> **Cline no es un modelo de IA y MCP no convierte por sí solo al modelo en agente.**

Cline es el entorno/agente; utiliza un modelo de IA seleccionado y puede ofrecerle varias herramientas, incluidas Tools MCP.

## 1.4 ChatGPT ↔ GitHub — consolidación

En septiembre de 2026 el laboratorio se trasladó a un esquema más organizado:

```text
ChatGPT → razonamiento / análisis
GitHub  → persistencia / fuente de verdad del Learning Lab
```

El repositorio `jperdomo12/ai-eam-learning-lab` continúa el mismo aprendizaje; no representa un proyecto MCP nuevo.

---

# 2. Conceptos MCP que deben recordarse

## 2.1 Host, Client y Server

- **Host:** aplicación/entorno de IA con el que interactúa el usuario, por ejemplo Claude Desktop o VS Code + Cline.
- **Client:** componente del Host que mantiene la conexión MCP.
- **Server:** proceso que expone capacidades MCP.

El PC físico **no** es el Host en la terminología MCP.

## 2.2 Tools, Resources y Prompts

La PoC fue deliberadamente **Tool-centric**.

En la revalidación final de Cline, `maximo` mostró:

```text
Tools (14)
Resources (0)
Prompts (0)
```

MCP soporta también Resources y Prompts aunque no se usaran en esta PoC.

## 2.3 Transporte

El laboratorio utilizó `stdio`:

```text
Host
  ↓ lanza proceso
python -u maximo_mcp.py
  ↕ stdin / stdout
mensajes MCP / JSON-RPC
```

Un archivo `.json` de configuración no es el mecanismo de intercambio de cada petición. El archivo configura cómo arrancar el servidor; durante la ejecución los mensajes viajan por el transporte.

## 2.4 MCP y OSLC/REST

MCP no sustituye las APIs de Maximo.

```text
petición natural
   ↓
Tool MCP
   ↓
función Python
   ↓
OSLC / REST
   ↓
IBM Maximo
```

En la PoC la última parte fue sustituida por mocks.

---

# 3. Productos y componentes utilizados

| Producto / componente | Papel |
|---|---|
| **Windows** | sistema operativo local del laboratorio |
| **Visual Studio Code** | IDE donde se trabajó con Cline y código Python |
| **Cline** | extensión/agente para VS Code; Host/entorno desde el que se usaron MCP Servers |
| **Claude Desktop** | primer Host práctico del laboratorio MCP |
| **Modelo IA de Cline** | interpreta la petición y decide/ejecuta el tool calling disponible; puede cambiarse |
| **Python 3.14** | runtime realmente usado en el equipo para el servidor Maximo histórico |
| **MCP Python SDK / FastMCP** | framework del servidor Maximo histórico |
| **requests / urllib3** | rama HTTP/OSLC preparada hacia Maximo |
| **Node.js / npx** | runtime/lanzador usado para servidores MCP distribuidos como paquetes Node |
| **Filesystem MCP** | servidor MCP para leer/escribir dentro de carpetas explícitamente autorizadas |
| **GitHub MCP histórico** | tercer servidor usado durante el aprendizaje; implementación npm histórica hoy deprecated |
| **IBM Maximo** | sistema objetivo; no se conectó realmente durante este LAB |

### Cline y el modelo de IA

Cline **no es el modelo**. En la revalidación final:

- la configuración antigua intentaba usar `kwaipilot/kat-coder-pro` y falló con HTTP 404;
- se seleccionó **DeepSeek V4 Flash**, mostrado entonces en la pestaña `Free` de Cline;
- con ese modelo se completaron las pruebas MCP actuales.

Que un modelo aparezca `FREE` es una condición del servicio en ese momento, no una garantía permanente.

---

# 4. Instalación del entorno desde cero

Esta sección sirve como referencia de recuperación. No es necesario reinstalar el laboratorio actual.

## 4.1 Visual Studio Code

1. Instalar VS Code desde su distribución oficial.
2. Abrir `Extensions`.
3. Instalar la extensión **Python** de Microsoft.
4. Instalar la extensión **Cline**.

## 4.2 Python

El equipo histórico terminó usando Python **3.14**. Las guías iniciales hablaban de `Python 3.10+` como referencia general.

Durante la instalación debe garantizarse que Python sea accesible desde PATH.

Comprobación:

```bash
python --version
pip --version
```

Dependencias históricas:

```bash
pip install mcp requests urllib3
```

El script usa:

```python
from mcp.server.fastmcp import FastMCP
```

Por tanto representa la línea histórica del SDK usada en la PoC; no debe asumirse automáticamente como receta de una implementación productiva futura.

## 4.3 Node.js / npx

Node.js se necesitó porque Filesystem MCP —y el GitHub MCP histórico— se ejecutaban mediante paquetes del ecosistema Node.

Comprobaciones:

```bash
node --version
npm --version
npx --version
```

No fue necesario desarrollar JavaScript; Node.js actuó como runtime.

## 4.4 Cline

1. Abrir VS Code.
2. Ir a `Extensions` e instalar **Cline**.
3. Abrir el icono de Cline.
4. Iniciar sesión si Cline lo solicita.
5. En `Settings → API Configuration`, seleccionar un proveedor/modelo disponible.
6. Verificar que el modelo puede generar una respuesta básica antes de depurar MCP.

### Incidencia revalidada

La sesión histórica de Cline había quedado cerrada y el modelo antiguo había dejado de estar disponible. Antes de comprobar MCP fue necesario:

```text
Sign in to Cline
→ seleccionar un modelo vigente
→ iniciar una tarea nueva
```

Lección: un MCP Server puede estar bien configurado aunque el Host no pueda ejecutar una conversación por un problema independiente de autenticación o del modelo.

---

# 5. Configuración de Claude Desktop

La instalación utilizada era la versión Windows Store.

Ruta efectiva verificada históricamente:

```text
C:\Users\jpperdomo\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json
```

Acceso práctico:

```text
Claude Desktop
→ Settings / Configuración
→ Developer / Desarrollador
→ Edit Configuration / Editar configuración
```

Forma histórica del servidor Maximo:

```json
"maximo": {
  "command": "C:/.../python.exe",
  "args": [
    "-u",
    "C:/.../maximo_mcp.py"
  ]
}
```

Filesystem incluía las raíces autorizadas directamente después del nombre del paquete.

La versión sanitizada está en:

```text
mcp/config/claude_desktop_config.example.json
```

### Ciclo de cambios observado

Con Claude Desktop, para determinados cambios era necesario:

```text
Quit completo desde bandeja
→ abrir Claude
→ Developer
→ verificar servidor
→ probar
```

Esto fue una de las razones para experimentar después con Cline.

---

# 6. Configuración actual verificada de VS Code + Cline

## 6.1 Ruta real recuperada

La revalidación final permitió recuperar directamente la configuración efectiva de Cline:

```text
C:\Users\jpperdomo\.cline\data\settings\cline_mcp_settings.json
```

Esta ruta **supersede para el entorno actual** la ruta histórica documentada en abril de 2026:

```text
%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
```

La ruta antigua se conserva como evidencia de una versión/configuración previa, no como ubicación actual.

## 6.2 Cómo abrirla desde la interfaz actual

```text
VS Code
→ Cline
→ icono de herramientas / Customize
→ MCP
→ Installed
→ Edit Configuration
```

La interfaz también permite expandir cada servidor, ver Tools/Resources/Prompts y ejecutar `Restart Server`.

## 6.3 Forma actual del JSON

Cline usa en el entorno revalidado una envoltura `transport`:

```json
{
  "mcpServers": {
    "maximo": {
      "transport": {
        "type": "stdio",
        "command": "C:/.../python.exe",
        "args": [
          "-u",
          "C:/.../maximo_mcp.py"
        ]
      }
    },
    "filesystem": {
      "transport": {
        "type": "stdio",
        "command": "npx",
        "args": [
          "-y",
          "@modelcontextprotocol/server-filesystem",
          "C:/.../MCP-Claude",
          "C:/Users/<USUARIO>/Downloads"
        ]
      }
    }
  }
}
```

Ejemplo público sanitizado:

```text
mcp/config/cline_mcp_settings.example.json
```

### Nota sobre la ruta del script Maximo

La configuración local actual de Cline sigue apuntando al script histórico:

```text
C:\Users\jpperdomo\JP\Profesional\IA\MCP-Claude\maximo_mcp.py
```

GitHub conserva su artefacto de referencia en:

```text
mcp/src/maximo_mcp.py
```

No deben confundirse: uno es el proceso local actualmente configurado; el otro es el artefacto persistido del Learning Lab.

## 6.4 Filesystem MCP y permisos

Las rutas situadas después de:

```text
@modelcontextprotocol/server-filesystem
```

son las raíces que el servidor expone.

La prueba final comprobó este comportamiento explícitamente:

```text
ANTES
MCP-Claude   ✅ permitido
Downloads    ❌ rechazado

CAMBIO
se añade Downloads en args
→ guardar configuración
→ Restart Server de filesystem

DESPUÉS
MCP-Claude   ✅ permitido
Downloads    ✅ permitido
```

Esto confirmó el sandbox de Filesystem MCP.

---

# 7. Maximo MCP — artefacto y catálogo

El servidor final preservado está en:

```text
mcp/src/maximo_mcp.py
```

Utiliza:

```python
MODO_SIMULACION = True
```

Contiene exactamente 14 Tools:

| # | Tool | Propósito resumido |
|---:|---|---|
| 1 | `consultar_ot` | consulta una OT |
| 2 | `consultar_inventario` | consulta stock/ubicación |
| 3 | `listar_transiciones_ot` | muestra cambios de estado permitidos |
| 4 | `cambiar_estado_ot` | cambia estado en simulación / rama real prevista |
| 5 | `query_maximo` | consulta genérica por Object Structure |
| 6 | `consultar_activo` | consulta un activo |
| 7 | `listar_object_structures` | catálogo/introspección |
| 8 | `crear_ot` | crea OT simulada / rama real prevista |
| 9 | `ws_editar_ot` | prepara cambios en Working Set |
| 10 | `ws_confirmar_cambios` | confirma Working Set |
| 11 | `ws_cancelar_cambios` | cancela Working Set |
| 12 | `obtener_workflow_assignments` | consulta asignaciones workflow |
| 13 | `enviar_workflow_response` | responde workflow |
| 14 | `verificar_conexion` | diagnóstico del servidor / rama real prevista |

La rama HTTP/OSLC existe pero **no fue validada contra Maximo real**.

---

# 8. Selección de Tools — qué aprendimos realmente

## 8.1 Metadatos que ayudan

FastMCP expone información derivada de:

```text
nombre de función → nombre Tool
docstring         → descripción Tool
type hints        → esquema de argumentos
```

Ejemplo:

```python
@mcp.tool()
def consultar_ot(num_ot: str) -> str:
    """Consulta los detalles completos de una Orden de Trabajo (OT) en Maximo."""
```

Una descripción más rica ofrece más señales al modelo para diferenciar Tools similares.

Regla práctica:

> **Nombres claros + docstrings precisos + parámetros bien definidos aumentan la probabilidad de selección correcta.**

No la garantizan.

## 8.2 Prueba autónoma exitosa

En una tarea limpia se escribió sin mencionar MCP ni el nombre de la Tool:

```text
¿Cuántos SKF-6204 tenemos en el almacén CENTRAL?
```

Cline seleccionó correctamente la capacidad de inventario y devolvió:

```text
SKF-6204
CENTRAL
15 unidades
PASILLO-B2-ESTANTE4
```

Los datos eran mock.

## 8.3 Prueba donde el modelo se equivocó

En una tarea/contexto posterior, el modelo intentó utilizar una Tool inexistente y Cline devolvió:

```text
AI_NoSuchToolError: Model tried to call unavailable tool
```

El propio modelo concluyó erróneamente que el servidor `maximo` no estaba disponible, aunque la UI mostraba:

```text
maximo ●
Tools (14)
Resources (0)
Prompts (0)
```

Después, en una **tarea nueva**, indicando una Tool real:

```text
consultar_inventario
```

la consulta volvió a funcionar.

Conclusión:

> Un MCP Server puede estar operativo y el modelo todavía puede equivocarse en el tool calling. La calidad de selección del modelo forma parte del sistema completo.

---

# 9. Pruebas finales en Cline

## 9.1 Maximo MCP individual

✅ `consultar_inventario` devolvió 15 unidades de `SKF-6204` en `CENTRAL`, en modo simulación.

## 9.2 Filesystem — selección natural

Se pidió listar una carpeta sin indicar mecanismo.

Cline resolvió inicialmente la tarea mediante capacidades/terminal propias, no mediante Filesystem MCP.

Esto fue un aprendizaje importante:

```text
Cline puede disponer de varias rutas para resolver una tarea:
- herramientas nativas del IDE
- terminal / comandos
- MCP Tools
```

## 9.3 Filesystem — prueba controlada

Se indicó utilizar exclusivamente Filesystem MCP y no terminal.

Resultado:

```text
5 archivos + 1 carpeta (OLD)
```

✅ Filesystem MCP validado individualmente.

## 9.4 Sandbox — prueba negativa

Antes de autorizar `Downloads`, se solicitó a Filesystem MCP listar:

```text
C:\Users\jpperdomo\Downloads
```

Resultado: acceso rechazado porque la ruta estaba fuera de las raíces autorizadas.

✅ Control de alcance comprobado.

## 9.5 Cambio controlado de configuración

Se añadió:

```text
C:/Users/jpperdomo/Downloads
```

al `args` del servidor `filesystem`, se guardó el JSON y se ejecutó `Restart Server` solo para ese servidor.

La misma petición pasó a funcionar.

✅ Configuración + reinicio individual + nuevo permiso validados.

## 9.6 Composición Maximo + Filesystem

La prueba definitiva controlada indicó:

1. usar `query_maximo` sobre `MXWO`;
2. recuperar campos de OTs;
3. considerar abiertas las OTs fuera de `COMP`, `CLOSE` y `CAN`;
4. usar `write_file` de Filesystem MCP;
5. no usar terminal ni leer CSV previos;
6. crear:

```text
C:\Users\jpperdomo\Downloads\ots_abiertas_cline_mcp.csv
```

Resultado:

```csv
numero_ot,descripcion,estado,activo
OT-1001,Mantenimiento bomba centrífuga B-201,APPR,BOMBA-B201
OT-1002,Revisión compresor C-305,INPRG,COMP-C305
OT-1003,Cambio filtros HVAC zona norte,WAPPR,HVAC-ZN01
OT-1004,Reparación válvula V-102,WMATL,VALV-V102
```

✅ Composición entre **dos MCP Servers** confirmada en Cline.

### Matiz del mock `query_maximo`

El mock devolvió inicialmente cinco OTs. Cline excluyó `OT-1005` porque estaba en estado `COMP`.

La simulación de `query_maximo` no implementa toda la expresividad OSLC compleja de un servidor real; por tanto el filtrado final fue completado por el modelo.

`COMP` significa **Completada**; `CLOSE` significa **Cerrada**.

---

# 10. Prueba equivalente en Claude Desktop

Claude Desktop ya había validado una tarea combinada:

```text
Maximo MCP → obtener OTs abiertas simuladas
Filesystem MCP → crear ots_abiertas.csv
                en Downloads
```

Esta prueba demostró que el mismo patrón de composición no depende exclusivamente de Cline.

---

# 11. Claude Desktop vs VS Code + Cline

| Tema | Claude Desktop | VS Code + Cline |
|---|---|---|
| Tipo de entorno | aplicación de IA | extensión/agente dentro de VS Code |
| Modelo | Claude integrado | modelo seleccionable según proveedor/configuración |
| MCP | soportado | soportado |
| Config efectivo del LAB | `claude_desktop_config.json` | `cline_mcp_settings.json` |
| Forma JSON observada | `command/args/env` directamente bajo servidor | `transport.type/command/args/env` |
| Maximo | mismo script histórico local | mismo script histórico local |
| Filesystem | MCP explícito | MCP + además Cline puede tener herramientas nativas/terminal |
| Recarga observada | a veces Quit/reabrir | `Restart Server` individual |
| Visibilidad Tools | UI del Host, variable por versión | muy explícita: Tools / Resources / Prompts |
| Edición de código | principalmente chat | edición/diff/Approve dentro del IDE |
| Prueba mixta Maximo + Filesystem | ✅ | ✅ |

La diferencia conceptual principal:

```text
Claude Desktop
= Host + modelos Claude integrados

Cline
= Host/agente desacoplado del modelo
  + el usuario selecciona un modelo compatible
```

---

# 12. GitHub MCP — estado final

Históricamente se utilizó:

```text
npx -y @modelcontextprotocol/server-github
```

con un PAT local.

Ese paquete quedó deprecated/archivado. El servidor oficial actual pertenece a:

```text
github/github-mcp-server
```

Durante la revalidación se decidió **no gastar más esfuerzo reinstalándolo**. El incidente quedó cerrado en el issue #1 del Learning Lab.

En Cline, la UI seguía mostrando `github` en verde y con texto moderno, pero el JSON recuperado reveló que esa instancia local todavía apuntaba al **paquete histórico deprecated**. Por tanto:

> una etiqueta verde o una descripción de UI no prueba que una configuración antigua se haya migrado automáticamente al servidor oficial actual.

No se reabre este frente salvo nueva necesidad real.

Nunca publicar PAT reales en GitHub, documentación o capturas.

---

# 13. Working Set y Human-in-the-Loop

La PoC exploró:

```text
IA propone cambio
   ↓
Working Set temporal
   ↓
preview
   ├─ confirmar
   └─ cancelar
```

Es un patrón útil para operaciones EAM de impacto, pero la implementación actual es solo memoria Python y no resuelve persistencia, concurrencia, identidad ni auditoría.

🟨 Puede considerarse un **candidato conceptual** para AI-EAM-MAXIMO, nunca una decisión automática del producto.

---

# 14. Seguridad y límites productivos

No copiar directamente a producción:

```python
verify=False
urllib3.disable_warnings(...)
API_KEY = "..."
```

La PoC tampoco implementa suficientemente:

- secret management;
- autorización por usuario;
- allow-lists robustas para `query_maximo`;
- auditoría de Tools;
- trazabilidad de cambios;
- observabilidad;
- sesiones/concurrencia de Working Set;
- validación real de endpoints y payloads Maximo.

Filesystem MCP debe mantener el principio de **mínimo directorio necesario**.

Las Tools de escritura deberían seguir un patrón de confirmación humana mientras el riesgo lo justifique.

---

# 15. Fuentes históricas y reconciliación documental

Se utilizaron como fuentes de transición, entre otras:

- Bitácora de Proyecto: IA Generativa + MCP para IBM Maximo;
- Guía de Configuración Avanzada / Aprendizaje: Cline + MCP;
- notas de Claude/Cline;
- HandOff Gemini → ChatGPT;
- código y configuraciones recuperadas;
- capturas y revalidación práctica de septiembre de 2026.

Dos puntos de esas fuentes quedaron explícitamente actualizados:

1. **Ruta Cline:** la guía histórica indicaba `%APPDATA%\Code\User\globalStorage\...`; la revalidación actual recuperó directamente `C:\Users\jpperdomo\.cline\data\settings\cline_mcp_settings.json`.
2. **GitHub MCP:** el paquete npm histórico formó parte real del laboratorio, pero ya no es la referencia vigente para reinstalación.

La documentación de transición no compite con este documento. Su conocimiento útil queda absorbido aquí.

---

# 16. Qué conservar en la cabeza

1. **MCP conecta una aplicación de IA con capacidades externas mediante un protocolo estándar.**
2. **Host ≠ PC.**
3. Un MCP Server puede exponer Tools, Resources y Prompts.
4. Nuestro Maximo MCP expone 14 Tools; Resources y Prompts quedaron en 0.
5. Cline es el entorno/agente; DeepSeek/Claude/GPT/Gemini son modelos o familias de modelos, según el caso.
6. El modelo decide qué Tool invocar y puede equivocarse incluso si el servidor está activo.
7. Para pruebas controladas conviene indicar explícitamente Tool/MCP; en uso normal no debería ser obligatorio.
8. Filesystem MCP solo accede a raíces autorizadas.
9. Cline puede resolver una tarea mediante MCP o mediante capacidades nativas/terminal si no se restringe la ruta.
10. Maximo MCP y Filesystem MCP se compusieron con éxito tanto en Claude Desktop como en Cline.
11. Los datos Maximo fueron **simulados**.
12. MCP y OSLC/REST son complementarios.
13. El paquete GitHub MCP histórico quedó obsoleto sin invalidar el patrón MCP.
14. El patrón `proponer → revisar → confirmar` es especialmente relevante para escrituras EAM.

---

# 17. Estado final

## ✅ CERRADO / CONGELADO

Queda cerrado para este alcance:

- conceptos MCP fundamentales;
- evolución Gemini → Claude Desktop → VS Code + Cline;
- instalación y configuración de productos principales;
- configuración efectiva de Claude Desktop y Cline;
- Maximo MCP individual;
- Filesystem MCP individual;
- sandbox Filesystem antes/después;
- selección autónoma y controlada de Tools;
- error de tool calling observado y diagnosticado;
- composición Maximo + Filesystem;
- 14 Tools preservadas;
- GitHub MCP histórico documentado y conscientemente diferido;
- límites de producción explicitados.

## ❌ Fuera de alcance / no validado

- Maximo real;
- hardening productivo;
- servidor MCP remoto;
- GitHub MCP oficial actual instalado;
- RAG.

## Próximo paso

➡️ **RAG — nuevo laboratorio independiente dentro de `ai-eam-learning-lab`.**

Una pregunta guía para ese frente será:

```text
¿Cómo calibro este equipo según su manual?
```

MCP seguirá representando acceso a capacidades/sistemas; RAG se estudiará como recuperación de conocimiento desde documentos.

---

# 18. Relación con AI-EAM-MAXIMO

`ai-eam-learning-lab` conserva aprendizaje y evidencia.

`ai-driven-eam-copilot` es el producto y su fuente de verdad.

```text
Learning Lab
   ↓
aprendizaje / evidencia
   ↓
🟨 CANDIDATO A INCORPORAR
   ↓ evaluación explícita
AI-EAM-MAXIMO
```

Nada de este laboratorio convierte automáticamente en arquitectura de producto:

- Cline;
- Claude Desktop;
- “Tridente”;
- las 14 Tools;
- Working Set;
- configuración local;
- código histórico.

---

# 19. Regla de mantenimiento

Si MCP se reabre en el futuro:

1. actualizar primero esta documentación canónica;
2. actualizar `MCP_LAB_FAST_READING.md`;
3. actualizar `MCP_LAB_HANDOFF.md`;
4. preservar ejemplos sanitizados en `mcp/config/`;
5. no crear documentación narrativa paralela salvo necesidad clara;
6. no publicar secretos;
7. distinguir siempre entre **histórico**, **revalidado**, **propuesto** y **productivo**.
