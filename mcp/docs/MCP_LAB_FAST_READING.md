# ⚡ MCP LAB — Fast Reading

> 🎯 **Objetivo:** recuperar en pocos minutos qué buscó el laboratorio MCP, qué se construyó, cómo se configuró, cómo se probó y qué quedó realmente demostrado.
>
> 📍 **Estado:** ✅ resumen vigente del laboratorio MCP cerrado para su alcance actual.
>
> 📘 **Documento completo:** [`MCP_LAB_DOCUMENTATION.md`](MCP_LAB_DOCUMENTATION.md)

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Se amplían las explicaciones de Node.js/`npx`, `@mcp.tool()`, Filesystem MCP, configuración general de Cline y JSON/JSON-RPC; se añaden ejemplos de GitHub MCP y una prueba mixta Maximo + Filesystem claramente marcada como propuesta. |
| 2026-09-10 | Creación del resumen de lectura rápida a partir de la baseline consolidada del laboratorio. |

---

## 1. El laboratorio en 60 segundos

La pregunta fue sencilla: **¿puede una aplicación de IA usar lenguaje natural para consultar y ejecutar capacidades EAM / IBM Maximo a través de MCP?**

La PoC respondió **sí para el mecanismo MCP y para operaciones simuladas**. Se construyó un MCP Server local en Python, se conectó primero con Claude Desktop y después se trabajó desde VS Code + Cline. El servidor final expuso **14 Tools** orientadas a Maximo y funcionó con `MODO_SIMULACION = True`.

La idea se amplió a tres MCP Servers trabajando en el mismo entorno:

```text
Maximo MCP + Filesystem MCP + GitHub MCP
```

A esa combinación se la llamó informalmente **“Tridente MCP”** porque estaba formada por tres servidores. No es un término del estándar MCP.

Lo que **no** se probó fue una conexión viva contra IBM Maximo. El código contiene una rama HTTP/OSLC prevista, pero no se validaron lecturas, escrituras ni workflow reales.

### Números para recordar

| Elemento | Resultado |
|---|---:|
| Entornos principales usados | **2** — Claude Desktop y VS Code + Cline |
| MCP Servers combinados | **3** — Maximo, Filesystem y GitHub |
| Tools del servidor Maximo final | **14** |
| Transporte local principal | **stdio** |
| Modo Maximo realmente probado | **Simulación** |
| Conexiones reales a IBM Maximo probadas | **0** |

---

## 2. Qué buscaba el laboratorio

El objetivo era **aprender MCP haciendo una PoC real**, no construir todavía una integración productiva.

Los casos de uso imaginados incluían:

- consultar una Orden de Trabajo;
- consultar inventario y activos;
- conocer transiciones de estado;
- cambiar el estado de una OT;
- crear una OT;
- revisar y confirmar cambios antes de aplicarlos;
- consultar y responder workflow;
- combinar datos transaccionales con conocimiento técnico en una etapa posterior.

Ejemplos de preguntas que motivaron el trabajo:

```text
“¿Cuántos rodamientos tenemos en el almacén CENTRAL?”
“Consulta la OT-1002.”
“¿A qué estados puedo mover esta OT?”
“Cambia la OT a completada.”
“Crea una OT correctiva para este activo.”
```

Una pregunta como:

```text
“¿Cómo calibro este equipo según su manual?”
```

pertenece principalmente al frente **RAG**, porque requiere recuperar conocimiento desde manuales o procedimientos. MCP y RAG pueden complementarse: MCP para acceder a sistemas/capacidades y RAG para recuperar conocimiento. Ese trabajo se documentará, cuando comience, bajo la carpeta raíz `rag/` de este repositorio.

---

## 3. Arquitectura que se probó

La arquitectura básica fue:

```text
Usuario
  ↓ lenguaje natural
Claude Desktop / VS Code + Cline
  ↓
MCP Client
  ↓ stdio
MCP Server Python
  ↓
maximo_mcp.py
  ├─ mocks EAM                         ← PROBADO
  └─ requests → OSLC/REST → Maximo    ← PREPARADO, NO VALIDADO
```

### Concepto clave

MCP **no sustituye** las APIs de Maximo. En una integración real, una Tool MCP puede encapsular la intención EAM y por debajo utilizar OSLC/REST u otro servicio Maximo.

```text
“Consulta la OT”
      ↓
Tool MCP: consultar_ot
      ↓
función Python
      ↓
OSLC / REST Maximo
```

En la PoC, la última parte fue sustituida por mocks para poder aprender sin depender de una instancia Maximo disponible.

---

## 4. Herramientas y escenarios funcionales

El `maximo_mcp.py` final conserva **14 Tools**, agrupables en cuatro escenarios principales.

| Escenario | Tools principales | Qué se quería probar |
|---|---|---|
| **1. Consultar** | `consultar_ot`, `consultar_inventario`, `consultar_activo`, `query_maximo`, `listar_object_structures` | Obtener datos EAM mediante lenguaje natural. |
| **2. Ciclo de vida OT** | `listar_transiciones_ot`, `cambiar_estado_ot`, `crear_ot` | Ejecutar operaciones de mantenimiento y estados. |
| **3. Edición controlada** | `ws_editar_ot`, `ws_confirmar_cambios`, `ws_cancelar_cambios` | Probar `preview → confirmar/cancelar` antes de persistir. |
| **4. Workflow / diagnóstico** | `obtener_workflow_assignments`, `enviar_workflow_response`, `verificar_conexion` | Explorar aprobaciones y comprobar el servidor. |

### ¿Qué significa `@mcp.tool()`?

En Python, `@mcp.tool()` es un **decorador de FastMCP**. Su función práctica es registrar una función Python como una Tool que el MCP Server puede publicar para que el Host/Client la descubra y la invoque.

Ejemplo simplificado:

```python
@mcp.tool()
def verificar_conexion() -> str:
    return "Servidor MCP funcionando"
```

Sin el decorador, `verificar_conexion()` sería simplemente una función Python interna. Con `@mcp.tool()`, pasa a formar parte de las capacidades MCP expuestas por el servidor.

El flujo mental es:

```text
función Python
     +
@mcp.tool()
     ↓
Tool MCP publicada
     ↓
Claude/Cline puede descubrirla e invocarla
```

El patrón de **Working Set** fue especialmente útil como aprendizaje de Human-in-the-Loop:

```text
proponer cambio
     ↓
mostrar preview
     ↓
confirmar  /  cancelar
```

El Working Set era memoria temporal del script Python; no una funcionalidad nativa de Maximo.

---

## 5. Software usado — y para qué servía cada pieza

| Componente | Para qué se usó |
|---|---|
| Python + FastMCP | implementar el MCP Server Maximo |
| Claude Desktop | primer Host práctico de la PoC |
| VS Code + Cline | iterar sobre código/configuración con menos fricción |
| Node.js / `npx` | ejecutar los MCP Servers de Filesystem y GitHub usados en el laboratorio |
| Filesystem MCP | leer/escribir únicamente en carpetas autorizadas |
| GitHub MCP | investigar repositorios y código |
| `requests` / `urllib3` | preparar llamadas HTTP/OSLC hacia Maximo |

### Node.js y `npx` — por qué aparecieron si nuestro servidor era Python

Nuestro **Maximo MCP** estaba escrito en Python, pero los servidores MCP de **Filesystem** y **GitHub** utilizados en aquella etapa se distribuían como paquetes del ecosistema Node.js.

Por eso instalamos **Node.js**: era el runtime necesario para poder ejecutarlos. `npx` es una utilidad incluida en ese ecosistema que permite lanzar un paquete sin tener que desarrollar nosotros una aplicación Node.

Por ejemplo, en la configuración aparecía:

```text
npx -y @modelcontextprotocol/server-filesystem ...
```

Mentalmente:

```text
Python
  └─ ejecuta nuestro Maximo MCP

Node.js / npx
  ├─ ejecuta Filesystem MCP
  └─ ejecuta GitHub MCP histórico
```

No fue necesario aprender o programar JavaScript para esta PoC; Node.js actuó principalmente como **runtime de esos servidores adicionales**.

---

## 6. Dónde se configuraban las carpetas de Filesystem MCP

Las carpetas autorizadas estaban declaradas en los **argumentos (`args`) del servidor Filesystem MCP** dentro del archivo de configuración del Host.

En la configuración histórica de Claude Desktop se utilizaron:

```text
C:\Users\jpperdomo\JP\Profesional\IA\MCP-Claude
C:\Users\jpperdomo\Downloads
```

Conceptualmente:

```json
"filesystem": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "C:/RUTA/CARPETA-AUTORIZADA-1",
    "C:/RUTA/CARPETA-AUTORIZADA-2"
  ]
}
```

Las rutas que aparecen **después del nombre del paquete** son las carpetas que el servidor puede exponer. Esto es importante porque Filesystem MCP no debería recibir acceso indiscriminado a todo el disco.

La versión pública sanitizada de esta configuración está en:

```text
mcp/config/claude_desktop_config.example.json
```

---

## 7. JSON, JSON-RPC y stdio — qué significa cada cosa

### JSON

**JSON** es simplemente un formato de datos estructurados basado en pares `clave: valor`.

Ejemplo:

```json
{
  "num_ot": "OT-1002"
}
```

### JSON-RPC

**JSON-RPC** añade unas reglas para usar JSON como mensajes de llamada y respuesta entre programas. Por ejemplo, una llamada conceptual a una Tool MCP puede verse así:

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/call",
  "params": {
    "name": "consultar_ot",
    "arguments": {
      "num_ot": "OT-1002"
    }
  }
}
```

Y la respuesta mantiene el mismo `id` para relacionarla con la petición:

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "OT-1002 ..."
      }
    ]
  }
}
```

No teníamos que escribir estos mensajes manualmente: el SDK MCP y el Client los gestionaban.

### stdio

`stdio` significa **standard input / standard output**. Fue el canal local por el que estos mensajes viajaban entre el MCP Client y nuestro proceso Python.

```text
Claude / MCP Client
     ↓ JSON-RPC por stdin
maximo_mcp.py
     ↑ JSON-RPC por stdout
Claude / MCP Client
```

La diferencia que conviene recordar es:

```text
archivo .json       = configuración guardada en disco
JSON                = formato de representación de datos
JSON-RPC            = reglas de petición/respuesta usando JSON
stdio               = canal por el que viajaron esos mensajes en nuestra PoC
```

---

## 8. Cómo se probó desde Claude Desktop

La primera Tool deliberadamente simple fue:

```text
verificar_conexion
```

La secuencia fue aproximadamente:

```text
1. Crear maximo_mcp.py.
2. Definir verificar_conexion() en Python.
3. Añadir @mcp.tool() para publicarla como Tool MCP.
4. Registrar el servidor en claude_desktop_config.json.
5. Cerrar Claude Desktop completamente.
6. Abrirlo nuevamente.
7. Ir a Settings → Developer.
8. Comprobar/activar el servidor MCP.
9. Pedir desde el chat que ejecutara la prueba.
10. Recibir la respuesta del MCP Server.
```

Este hito confirmó **Claude Desktop ↔ MCP Server local**, no una conexión a IBM Maximo real.

Después se probaron operaciones EAM simuladas, por ejemplo consulta de OTs, inventario y cambios de estado.

### Fricción detectada

Para que Claude Desktop recogiera ciertos cambios de configuración/servidor, el flujo documentado implicaba salir completamente —incluyendo `Quit` desde la bandeja del sistema—, volver a entrar y comprobar otra vez el servidor en Developer. Esto hacía lenta la iteración frecuente.

---

## 9. Cómo se configuró y utilizó Cline, en líneas generales

Cline se instaló como extensión de **VS Code**. La configuración MCP se mantuvo en un archivo propio de Cline, documentado históricamente en:

```text
%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
```

El archivo seguía la misma idea general que Claude Desktop: una sección `mcpServers` declaraba qué proceso arrancar para cada servidor.

Conceptualmente:

```json
{
  "mcpServers": {
    "maximo": {
      "command": "<PYTHON>",
      "args": ["-u", "<RUTA>/maximo_mcp.py"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "<CARPETA>"]
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

El archivo local original de Cline **no fue recuperado directamente** durante esta consolidación; esta estructura procede de la guía y notas históricas.

La operación habitual documentada era:

```text
1. Abrir VS Code + Cline.
2. Revisar en el panel MCP que los servidores aparecieran activos (puntos verdes).
3. Pedir cambios sobre maximo_mcp.py desde Cline.
4. Cline abría/editaba el archivo y mostraba un Diff.
5. Juan aprobaba el cambio.
6. Usar el botón de refresco/reinicio del MCP Server.
7. Volver a ejecutar una prueba desde Cline sin reiniciar todo VS Code.
```

Ese flujo fue la razón principal para pasar de Claude Desktop a Cline durante el desarrollo: **menos fricción para editar → refrescar → probar**.

---

## 10. Ejemplos de pruebas y resultados

### 10.1 Maximo MCP — consulta de inventario

Petición típica:

```text
“¿Cuántos SKF-6204 tenemos en CENTRAL?”
```

Resultado del mock disponible en el código:

```text
Artículo: SKF-6204
Almacén: CENTRAL
Cantidad disponible: 15
```

### 10.2 Maximo MCP — cambio de estado

Se probaron cambios simulados de estado respetando una tabla local de transiciones válidas. El script devolvía estado anterior, estado nuevo, memo y timestamp.

### 10.3 Working Set

Se podía preparar un cambio de campos, obtener un preview y después confirmar o cancelar.

### 10.4 Filesystem MCP

Se documentaron pruebas para:

- listar archivos de una carpeta autorizada;
- escribir un archivo dentro de una carpeta autorizada.

La configuración limitaba explícitamente las carpetas a las que el servidor podía acceder.

### 10.5 GitHub MCP — prueba histórica realizada

Una prueba documentada fue aproximadamente:

```text
“Busca en GitHub otros servidores MCP de Maximo para ver si alguien
ha programado funciones que nosotros no tenemos.”
```

El objetivo no era preguntar algo sobre Maximo directamente, sino comprobar que la IA podía usar **otro MCP Server** para investigar repositorios GitHub y utilizar el resultado como apoyo al desarrollo.

Las notas históricas registran repositorios encontrados como:

```text
markusvankempen/maximo-mcp-ai-integration-options
soumyaprasadrana/maximo-mcp-server
```

La comparación de capacidades contribuyó al proceso que terminó ampliando nuestro servidor Maximo hasta el catálogo final de 14 Tools.

### 10.6 Prueba mixta Maximo MCP + Filesystem MCP — propuesta útil

Esta prueba **no queda registrada como una prueba histórica ya realizada**. Es un buen ejemplo para reproducir en el futuro cómo un Host puede combinar dos MCP Servers en una misma tarea:

```text
“Consulta las OTs abiertas, genera un archivo CSV con wonum,
descripción, estado y activo, y guarda el archivo en la carpeta autorizada XXXX.”
```

Flujo esperado:

```text
Usuario
  ↓
IA / Host
  ├─ Maximo MCP → obtiene las OTs
  │
  └─ Filesystem MCP → crea y guarda el CSV
```

El valor de esta prueba sería demostrar **composición de capacidades**: un servidor obtiene información EAM y otro persiste un artefacto local.

> En nuestro laboratorio actual, como Maximo continúa en simulación, el contenido del CSV vendría de los mocks, no de IBM Maximo real.

---

## 11. “Tridente MCP”

La configuración avanzada combinó:

```text
                Host / entorno de IA
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
     Maximo MCP   Filesystem MCP   GitHub MCP
      EAM/data       archivos       repos/código
```

Cada servidor resolvía un dominio distinto. El aprendizaje fue que un Host puede combinar **varios servidores especializados** en lugar de construir un único servidor gigantesco.

“Tridente” solo fue nuestro nombre informal para recordar los **tres** servidores.

---

## 12. Lo más importante que aprendimos

1. **Host ≠ PC.** El Host es la aplicación/entorno de IA.
2. Un MCP Server expone capacidades; nuestra PoC se centró en **Tools**.
3. `@mcp.tool()` registra una función Python para que FastMCP la publique como Tool.
4. MCP también contempla otras primitivas como **Resources** y **Prompts**.
5. MCP no convierte por sí solo a un LLM en agente autónomo.
6. En local, **stdio** permite conectar Client y Server sin desplegar un servicio HTTP.
7. **JSON** es un formato de datos; **JSON-RPC** define mensajes de llamada/respuesta; no significa intercambiar archivos `.json`.
8. **MCP y OSLC/REST son complementarios**: MCP puede ser la frontera orientada a IA y OSLC/REST la integración real con Maximo.
9. **Node.js / npx** fueron necesarios para ejecutar los MCP Servers adicionales usados en aquella PoC, no para programar nuestro servidor Maximo.
10. Filesystem MCP recibe explícitamente las **carpetas autorizadas** en su configuración.
11. **Simular primero** permitió aprender MCP sin depender de la infraestructura Maximo.
12. Para escrituras EAM, el patrón **proponer → revisar → confirmar** es más seguro que ejecutar cambios silenciosamente.
13. Combinar servidores especializados —Maximo, Filesystem y GitHub— permite componer tareas más ricas.

---

## 13. Qué no debemos confundir con una solución productiva

La PoC contiene simplificaciones deliberadas:

- `MODO_SIMULACION = True`;
- `verify=False` y warnings SSL deshabilitados;
- credenciales modeladas de forma simple;
- reglas de transición de estados codificadas localmente;
- Working Set solo en memoria;
- respuestas principalmente como strings;
- Tool genérica `query_maximo` con alcance amplio;
- sin autorización empresarial por usuario;
- sin observabilidad/auditoría robusta;
- sin pruebas contra una instancia Maximo real.

Por ello, el resultado correcto es:

> **PoC MCP orientada a Maximo probada en simulación; integración viva con IBM Maximo no validada.**

---

## 14. Relación con RAG y AI-EAM-MAXIMO

MCP y RAG resuelven necesidades diferentes:

```text
MCP → acceder a sistemas, datos y acciones
RAG → recuperar conocimiento desde documentos
```

Una futura experiencia EAM podría combinarlos:

```text
“¿Cómo debo atender esta alarma?”
          ↓
IA / orquestación
   ├─ MCP → consulta activo, OT, historial
   └─ RAG → recupera manual/procedimiento
          ↓
respuesta fundamentada
          ↓
si hay acción → confirmación humana
```

El laboratorio RAG será independiente y se documentará bajo `rag/` cuando se inicie.

Nada de esta PoC pasa automáticamente al producto **AI-EAM-MAXIMO**. Cualquier patrón reutilizable debe evaluarse allí como **🟨 CANDIDATO A INCORPORAR**.

---

## 15. Dónde continuar si vuelves meses después

Leer/utilizar en este orden:

```text
1. mcp/docs/MCP_LAB_FAST_READING.md      ← este resumen
2. mcp/docs/MCP_LAB_DOCUMENTATION.md     ← detalle completo
3. mcp/src/maximo_mcp.py                 ← código final recuperado
4. mcp/config/claude_desktop_config.example.json
5. mcp/src/history/                       ← código temprano, solo si hace falta historia
6. mcp/docs/MCP_LAB_HANDOFF.md           ← estado y continuidad
```

Si solo necesitas recuperar el concepto, recuerda esta frase:

> **MCP permitió conectar la aplicación de IA con capacidades EAM externas mediante Tools; nosotros validamos el mecanismo con un servidor Python y datos simulados, no con IBM Maximo real.**
