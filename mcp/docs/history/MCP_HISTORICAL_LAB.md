# 🕰️ Laboratorio histórico — MCP + IBM Maximo

> ⚠️ **HISTÓRICO — material de referencia.** Este documento reconstruye y documenta de forma reproducible el laboratorio realizado con Gemini, Claude Desktop, VS Code/Cline y un servidor MCP propio para IBM Maximo. No constituye arquitectura vigente de AI-EAM-MAXIMO.
>
> 🎯 **Objetivo del documento:** permitir que, meses después, sea posible entender qué se quiso probar, qué se instaló, cómo se configuró, qué código se construyó, qué pruebas se ejecutaron, qué resultados se observaron y qué quedó sin validar, sin depender del chat original.
>
> 📍 **Estado:** ✅ CERRADO para el alcance histórico de aprendizaje.
> 🗓️ **Actualizado:** 2026-09-10

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Reconstrucción integral del laboratorio histórico como memoria técnica paso a paso y corrección de inconsistencias mediante auditoría del código real. |
| 2026-09-10 | Verificación del artefacto real `maximo_mcp.py`, lógica dual y catálogo efectivo de 14 tools. |
| 2026-09-10 | Creación inicial a partir de HandOff, bitácora y guía histórica Gemini/Claude/Cline. |

---

# 1. Objetivo original del laboratorio

El laboratorio surgió de una idea concreta: **comprobar si una aplicación de IA podía interactuar con IBM Maximo mediante lenguaje natural y ejecutar capacidades externas a través de MCP (Model Context Protocol)**.

La visión funcional era similar a:

```text
Usuario
   ↓ lenguaje natural
Aplicación de IA
   ↓ MCP
Servidor MCP
   ↓ tools EAM
Lógica Python
   ↓
IBM Maximo / datos simulados
```

No se buscaba construir una solución productiva. El propósito era aprender haciendo y responder preguntas como:

- ¿cómo descubre una IA una capacidad externa?;
- ¿cómo invoca una función mediante MCP?;
- ¿cómo se implementa un MCP Server local?;
- ¿cómo se podría encapsular semántica EAM/Maximo en tools?;
- ¿cómo avanzar sin disponer de un Maximo real?;
- ¿cómo podrían convivir varios MCP Servers en un mismo entorno?;
- ¿qué cambia cuando el entorno de IA también puede editar código, ejecutar terminal y acceder a GitHub?

---

# 2. Alcance real alcanzado

El laboratorio llegó hasta una PoC funcional con un servidor MCP local en Python y una evolución posterior a varias capacidades.

Se alcanzó:

```text
Claude Desktop / Cline
        ↓ MCP
maximo_mcp.py
        ↓
14 tools EAM / Maximo
        ↓
modo simulación
        o
lógica OSLC/REST preparada
```

También se configuró un entorno multi-servidor:

```text
VS Code + Cline
   ├─ Maximo MCP
   ├─ Filesystem MCP
   └─ GitHub MCP
```

Lo que **no** se alcanzó fue la validación contra una instancia viva de IBM Maximo.

---

# 3. Evolución cronológica

## 3.1 Exploración inicial con Gemini / Google Cloud

La primera aproximación se estudió alrededor de Gemini y servicios de Google Cloud / Vertex AI.

El problema detectado fue que, para una PoC local, esa vía añadía infraestructura y configuración que no aportaban valor inmediato al aprendizaje: endpoints, servicios cloud, seguridad, conectividad y coste potencial.

### Decisión tomada

Para reducir fricción se buscó una vía local.

## 3.2 Pivotaje a Claude Desktop + MCP

Claude Desktop se utilizó porque permitía registrar servidores MCP locales y lanzar un proceso Python desde el propio entorno de escritorio.

La arquitectura pasó a ser:

```text
Claude Desktop
      ↓ stdio / MCP
Python + FastMCP
      ↓
maximo_mcp.py
```

Esta fue la etapa en la que se validó el mecanismo fundamental: una aplicación de IA podía descubrir e invocar una tool expuesta por el servidor local.

## 3.3 Evolución a VS Code + Cline

Posteriormente se trasladó la operativa a VS Code con Cline.

La razón fue acortar el ciclo de desarrollo:

```text
pedir cambio
   ↓
IA abre / modifica código
   ↓
usuario revisa diff
   ↓
se guarda
   ↓
se refresca / reinicia servidor MCP
   ↓
se prueba
```

Esto reducía pasos manuales frente al patrón anterior de copiar código desde un chat hacia el editor.

## 3.4 Expansión a varios servidores MCP

Se configuraron Maximo MCP, Filesystem MCP y GitHub MCP en paralelo.

A esta combinación se le llamó informalmente **“Tridente MCP”**. El término pertenece únicamente al laboratorio; no es parte del estándar MCP.

---

# 4. Entorno y componentes utilizados

| Componente | Función en el laboratorio |
|---|---|
| Windows | Sistema operativo local |
| Visual Studio Code | IDE principal |
| Extensión Python | Soporte de desarrollo Python |
| Cline | Entorno de IA dentro de VS Code usado posteriormente |
| Claude Desktop | Aplicación de IA usada inicialmente como host MCP |
| Python 3.10+ | Runtime del servidor MCP |
| MCP Python SDK / FastMCP | Implementación del MCP Server |
| `requests` | Llamadas HTTP hacia servicios de Maximo |
| `urllib3` | Gestión de SSL/warnings en la PoC |
| Node.js / `npx` | Ejecución de servidores MCP adicionales |
| Filesystem MCP | Acceso delimitado a archivos locales |
| GitHub MCP | Investigación y acceso a repositorios |
| IBM Maximo | Sistema EAM objetivo; no conectado realmente en esta PoC |

---

# 5. Instalación paso a paso

## 5.1 Visual Studio Code

Se instaló VS Code como entorno de desarrollo.

Después se instaló la extensión oficial de Python para facilitar edición, detección de errores y ejecución del script.

## 5.2 Python

Se instaló Python 3.10 o superior.

Durante la instalación era importante habilitar Python en el `PATH` de Windows.

La comprobación utilizada fue:

```bash
python --version
```

### Incidencia encontrada

Python no quedó inicialmente accesible desde terminal en algún momento del proceso.

### Resolución

Se corrigió la instalación / PATH hasta que el comando anterior funcionó.

## 5.3 Dependencias Python

Las dependencias documentadas fueron:

```bash
pip install mcp requests urllib3
```

Funciones:

- `mcp`: SDK MCP / FastMCP;
- `requests`: llamadas HTTP/HTTPS;
- `urllib3`: soporte de red y tratamiento de warnings SSL.

## 5.4 Node.js / npx

Node.js fue necesario en la etapa posterior para poder ejecutar servidores MCP distribuidos como paquetes Node mediante `npx`, concretamente Filesystem MCP y GitHub MCP.

## 5.5 Claude Desktop

Se instaló Claude Desktop como primera aplicación desde la que se probó el servidor MCP local.

## 5.6 Cline

Más adelante se instaló Cline en VS Code para convertir el entorno de desarrollo en el punto principal de experimentación.

---

# 6. Creación del servidor MCP

El artefacto principal fue:

```text
maximo_mcp.py
```

El archivo histórico real fue localizado posteriormente en:

```text
jperdomo12/Maximo-IA-Project/maximo_mcp.py
```

El código auditado confirma, entre otros elementos:

```python
from mcp.server.fastmcp import FastMCP

MODO_SIMULACION = True
MAXIMO_URL = "https://TU_SERVIDOR/maximo"
API_KEY = "TU_API_KEY_AQUÍ"

mcp = FastMCP("Maximo Enterprise")
```

Las tools se exponían con:

```python
@mcp.tool()
```

Y el servidor se ejecutaba mediante:

```python
if __name__ == "__main__":
    mcp.run()
```

### Resultado

✅ **VERIFICADO EN CÓDIGO:** existió un MCP Server real implementado con FastMCP.

---

# 7. Configuración de Claude Desktop

Claude Desktop necesitaba conocer el comando que iniciaba el MCP Server.

El archivo utilizado fue `claude_desktop_config.json`.

Durante el laboratorio se encontraron distintas rutas posibles en Windows según el tipo de instalación de Claude. La forma más fiable terminó siendo localizar el archivo desde:

```text
Claude Desktop
→ Settings
→ Developer
→ Edit configuration
```

Ejemplo sanitizado de la configuración:

```json
{
  "mcpServers": {
    "maximo": {
      "command": "python",
      "args": [
        "-u",
        "C:/RUTA/A/TU/PROYECTO/maximo_mcp.py"
      ]
    }
  }
}
```

### Qué hace esta configuración

Claude arranca el proceso:

```text
python -u maximo_mcp.py
```

Y se comunica con él mediante MCP.

> 🔐 Las rutas personales reales, tokens y credenciales no se reproducen en este repositorio público.

---

# 8. Lógica dual: simulación y real

Una de las decisiones más útiles del laboratorio fue separar explícitamente dos modos.

## 8.1 Modo simulación

```python
MODO_SIMULACION = True
```

Permitía:

- trabajar sin VPN;
- aprender MCP sin Maximo disponible;
- probar descubrimiento e invocación de tools;
- probar lenguaje natural;
- probar flujos de lectura y escritura sin riesgo;
- iterar rápidamente.

El código histórico contiene mocks de:

- órdenes de trabajo;
- inventario;
- activos;
- workflow;
- Object Structures.

## 8.2 Modo real previsto

```python
MODO_SIMULACION = False
```

El código estaba preparado para utilizar HTTP/OSLC contra Maximo.

Se verificó en el script:

- uso de `requests`;
- cabecera API Key;
- construcción de endpoints OSLC/Object Structures;
- timeout de 10 segundos;
- `verify=False`;
- desactivación de warnings SSL.

### Importante

⚠️ Esta rama de código **existía**, pero no demuestra que la conexión real funcionara.

`verify=False` y la desactivación de warnings SSL son decisiones aceptables únicamente como simplificación de laboratorio y no deben adoptarse como diseño de producción.

---

# 9. Primera prueba de extremo a extremo

La prueba inicial se diseñó deliberadamente simple.

Tool:

```text
verificar_conexion
```

Flujo:

```text
Usuario
   ↓
Claude Desktop
   ↓ descubre tool
verificar_conexion
   ↓ MCP
maximo_mcp.py
   ↓
resultado
   ↓
Claude Desktop
```

### Resultado

🧪 **PROBADO HISTÓRICAMENTE:** Claude pudo invocar una tool del servidor MCP local y devolver su respuesta al usuario.

Este fue el hito que demostró que el mecanismo MCP estaba funcionando de extremo a extremo.

---

# 10. Pruebas funcionales con lenguaje natural

Después de validar el mecanismo, se probaron capacidades EAM simuladas.

Ejemplos documentados:

```text
Consulta la información de la orden de trabajo OT-2025
```

```text
¿Cuántos rodamientos tenemos en el almacén CENTRAL?
```

La IA decidía utilizar la tool correspondiente y presentaba el resultado al usuario.

Se adoptó una convención visual para distinguir origen de datos:

```text
🧪 [SIMULACIÓN]
```

frente a:

```text
✅ [REAL]
```

El segundo modo fue diseñado, pero no llegó a comprobarse contra Maximo vivo.

---

# 11. Evolución de las tools

La PoC comenzó con pocas capacidades y fue ampliándose.

La documentación histórica describe una evolución de **4 tools a 14 tools** tras investigar implementaciones de terceros y ampliar `maximo_mcp.py`.

La afirmación “14 tools” quedó posteriormente comprobada directamente contra el código conservado.

## 11.1 Catálogo REAL verificado en `maximo_mcp.py`

| # | Tool | Propósito |
|---:|---|---|
| 1 | `consultar_ot` | Consultar una Orden de Trabajo. |
| 2 | `consultar_inventario` | Consultar stock y ubicación de un artículo. |
| 3 | `listar_transiciones_ot` | Mostrar cambios de estado permitidos. |
| 4 | `cambiar_estado_ot` | Cambiar el estado de una OT. |
| 5 | `query_maximo` | Consulta genérica sobre Object Structures. |
| 6 | `consultar_activo` | Consultar datos de un activo. |
| 7 | `listar_object_structures` | Listar / descubrir Object Structures. |
| 8 | `crear_ot` | Crear una Orden de Trabajo. |
| 9 | `ws_editar_ot` | Preparar modificaciones en un Working Set. |
| 10 | `ws_confirmar_cambios` | Confirmar cambios preparados. |
| 11 | `ws_cancelar_cambios` | Cancelar cambios preparados. |
| 12 | `obtener_workflow_assignments` | Consultar asignaciones pendientes de workflow. |
| 13 | `enviar_workflow_response` | Enviar una respuesta de workflow. |
| 14 | `verificar_conexion` | Verificar funcionamiento y presentar capacidades. |

### Corrección importante introducida al trasladar el trabajo

Algunos documentos históricos llegaron a listar como parte de las 14 tools nombres como `consultar_ubicacion` o `generar_reporte_local`.

La auditoría del **código real** demostró que esos nombres no forman parte del catálogo final conservado. La tabla anterior es la referencia correcta porque procede del artefacto implementado, no de una descripción posterior.

Este es un ejemplo concreto de por qué el traslado a un repositorio con código + documentación verificable aporta valor: permite corregir memoria documental con evidencia.

---

# 12. Tipos de interacción explorados

El servidor no se quedó en consultas.

## Lectura

```text
consultar_ot
consultar_inventario
consultar_activo
query_maximo
listar_object_structures
obtener_workflow_assignments
```

## Escritura / acción

```text
crear_ot
cambiar_estado_ot
enviar_workflow_response
```

## Human-in-the-loop experimental

```text
ws_editar_ot
   ↓
preview / Working Set
   ↓
confirmar o cancelar
```

Esto permitió explorar una idea que sigue siendo importante en EAM: **no toda acción sugerida por IA debería ejecutarse inmediatamente**.

---

# 13. Working Set experimental

El Working Set se implementó como memoria temporal en el propio proceso Python.

No era una característica nativa de IBM Maximo.

El patrón probado fue:

```text
proponer cambio
     ↓
previsualizar
     ↓
usuario / flujo decide
   ↙             ↘
confirmar       cancelar
```

### Valor del experimento

Permitió explorar de forma temprana el patrón de confirmación antes de operaciones de escritura.

### Limitación

El estado se mantenía únicamente en memoria. Reiniciar el proceso podía eliminarlo.

---

# 14. Investigación mediante GitHub MCP

Después de configurar GitHub MCP se realizó una prueba de investigación de implementaciones externas.

Consulta documentada:

```text
Busca en GitHub otros servidores MCP de Maximo para ver si alguien ha programado funciones que nosotros no tenemos
```

La documentación registra que se localizaron proyectos de terceros y que esa investigación sirvió como entrada para ampliar el servidor propio.

Posteriormente se solicitó incorporar capacidades faltantes o mejores y el código evolucionó de 4 a 14 tools.

### Aprendizaje

La IA ya no se limitaba a responder preguntas: podía utilizar una capacidad externa para investigar código y utilizar ese resultado como apoyo para modificar otro artefacto.

---

# 15. Filesystem MCP

Filesystem MCP se incorporó para permitir acceso controlado a carpetas locales.

Ejemplo histórico conceptual:

```json
{
  "filesystem": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-filesystem",
      "<DIRECTORIO_AUTORIZADO>"
    ]
  }
}
```

### Idea importante

El servidor no recibía acceso ilimitado al PC; se configuraban directorios explícitamente autorizados.

---

# 16. GitHub MCP

GitHub MCP se utilizó para acceso a repositorios.

Ejemplo histórico sanitizado:

```json
{
  "github": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-github"
    ],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "<SECRET>"
    }
  }
}
```

### Seguridad

El patrón histórico dependía de un PAT.

Nunca debe publicarse el valor del token. Las configuraciones conservadas aquí utilizan placeholders.

---

# 17. Configuración del “Tridente MCP”

La configuración final histórica combinó los tres servidores.

Ejemplo sanitizado:

```json
{
  "mcpServers": {
    "maximo": {
      "command": "<PYTHON>",
      "args": ["-u", "<RUTA>/maximo_mcp.py"]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "<DIRECTORIO_AUTORIZADO>"
      ]
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

Arquitectura resultante:

```text
                 ┌─ maximo_mcp.py ── EAM / Maximo
Cline / Host ────┼─ Filesystem ───── archivos locales
                 └─ GitHub ───────── repositorios
```

---

# 18. Configuración de Cline

La guía histórica documentó el archivo:

```text
%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
```

La configuración registraba los tres servidores anteriores.

### Mejora operativa observada

Frente a Claude Desktop, Cline acercó en una sola interfaz:

- conversación;
- código;
- diff;
- terminal;
- servidores MCP;
- archivos;
- GitHub.

Esto hizo más corto el ciclo experimentar → cambiar → probar.

---

# 19. Ciclo de operación y refresco

## Claude Desktop

El procedimiento histórico documentado era:

1. modificar `maximo_mcp.py`;
2. cerrar Claude completamente, no solo la ventana;
3. volver a abrir Claude;
4. revisar `Settings > Developer`;
5. comprobar que el servidor estuviera activo;
6. ejecutar una consulta de prueba.

## Cline

La guía histórica describe un ciclo más corto mediante refresco/reinicio del servidor desde VS Code.

⚠️ El comportamiento exacto depende de la versión de Cline y no se considera una garantía vigente en 2026.

---

# 20. Problemas encontrados y cómo se resolvieron

## 20.1 Python no disponible desde terminal

**Síntoma:** `python` no se reconocía.

**Causa:** instalación / PATH.

**Resolución:** corregir la configuración y verificar con:

```bash
python --version
```

## 20.2 Ruta de configuración de Claude

**Problema:** distintas instalaciones de Claude podían utilizar rutas diferentes.

**Resolución práctica:** usar `Settings > Developer > Edit configuration` para localizar el archivo efectivo.

## 20.3 No disponer de Maximo real

**Problema:** el aprendizaje quedaba bloqueado por conectividad, VPN o credenciales.

**Resolución:** crear `MODO_SIMULACION` y datasets mock.

## 20.4 Reinicio frecuente del cliente

**Problema:** el ciclo editar → reiniciar Claude → probar era lento.

**Resolución posterior:** trasladar el trabajo a VS Code + Cline.

---

# 21. Evidencia: qué quedó demostrado y qué no

## ✅ VERIFICADO por artefacto real

- existe `maximo_mcp.py`;
- utiliza FastMCP;
- utiliza `@mcp.tool()`;
- contiene lógica dual simulación / real;
- contiene datasets mock;
- contiene exactamente 14 tools;
- contiene lógica HTTP/OSLC prevista;
- contiene operaciones de lectura, escritura, workflow y Working Set.

## 🧪 PROBADO / documentado en la ejecución histórica

- Claude Desktop ejecutó el MCP Server local;
- una tool MCP fue descubierta e invocada desde la conversación;
- se realizaron consultas simuladas de OT e inventario;
- se utilizó Cline posteriormente;
- se configuraron Maximo MCP, Filesystem MCP y GitHub MCP;
- GitHub MCP fue utilizado para investigar implementaciones relacionadas;
- el servidor propio evolucionó de 4 a 14 tools.

## ⚠️ DOCUMENTADO, pero no reproducido con versiones actuales

- rutas exactas actuales de configuración de Claude;
- configuración actual de Cline;
- paquetes MCP históricos de Filesystem/GitHub;
- comportamiento actual de refresh/hot reload.

## ❌ NO VALIDADO

- conexión a una instancia viva de IBM Maximo;
- lectura real desde Maximo;
- escritura real en Maximo;
- workflow real;
- seguridad productiva;
- despliegue empresarial;
- RAG.

---

# 22. Limitaciones técnicas del PoC

El script fue adecuado para aprendizaje, pero no debe considerarse código productivo.

Principales limitaciones observadas:

- `verify=False` en HTTPS;
- warnings SSL deshabilitados;
- API key representada como variable del script;
- transiciones de estado codificadas localmente;
- Working Set solo en memoria;
- respuestas fundamentalmente como strings;
- tratamiento de errores simplificado;
- `query_maximo` demasiado genérico para un entorno con controles estrictos;
- no hay autorización fina por tool;
- no hay auditoría empresarial;
- no hay validación contra dominios/configuración real de Maximo.

---

# 23. Modelo mental MCP que quedó consolidado

El laboratorio ayudó a separar correctamente responsabilidades:

```text
HOST
Aplicación de IA que coordina la experiencia
        ↓
CLIENT
Conexión MCP gestionada por el Host
        ↓
SERVER
Proceso que publica capacidades
        ↓
TOOLS / RESOURCES / PROMPTS
Capacidades MCP
        ↓
SISTEMAS REALES
Maximo, archivos, GitHub, APIs, etc.
```

Puntos importantes:

- el Host no es el PC físico;
- MCP no convierte por sí solo a un LLM en agente autónomo;
- MCP no sustituye necesariamente OSLC/REST;
- un MCP Tool puede encapsular internamente una API tradicional;
- MCP también contempla capacidades distintas de Tools, como Resources y Prompts.

---

# 24. Qué aprendimos específicamente para EAM / IBM Maximo

📘 **Una tool puede hablar el lenguaje del negocio.** `consultar_ot` es más significativa para un usuario EAM que una llamada HTTP genérica.

📘 **La simulación es extremadamente valiosa.** Permite desarrollar interacción, seguridad y UX antes de disponer del backend real.

📘 **Lectura y escritura deben tratarse de forma distinta.** La PoC ya insinuó esta diferencia con Working Set y confirmación.

📘 **La integración MCP puede vivir por encima de OSLC/REST.** MCP estandariza cómo la IA accede a capacidades; OSLC/REST puede seguir siendo el mecanismo de integración con Maximo.

📘 **El catálogo de tools debe gobernarse.** Exponer una consulta genérica muy poderosa puede ser útil en laboratorio, pero requiere límites en producción.

---

# 25. Cómo reproducir conceptualmente este laboratorio

> Esta sección explica la reproducción del laboratorio histórico. No garantiza compatibilidad exacta con versiones actuales de Claude, Cline o MCP.

1. Instalar Python y comprobar `python --version`.
2. Instalar VS Code y soporte Python.
3. Instalar dependencias:

```bash
pip install mcp requests urllib3
```

4. Obtener una copia de `maximo_mcp.py` desde el repositorio histórico.
5. Mantener:

```python
MODO_SIMULACION = True
```

6. Registrar el servidor en un Host MCP con un comando equivalente a:

```text
python -u <RUTA>/maximo_mcp.py
```

7. Reiniciar/refrescar el servidor MCP.
8. Comprobar que las tools aparecen disponibles.
9. Ejecutar `verificar_conexion`.
10. Probar una consulta como `consultar_ot` o `consultar_inventario`.
11. Opcionalmente instalar Node.js y añadir Filesystem/GitHub MCP si se desea reproducir la etapa multi-servidor.
12. No configurar credenciales Maximo reales salvo que exista un laboratorio seguro específico para ello.

---

# 26. Artefactos que sustentan esta reconstrucción

## Código

- `jperdomo12/Maximo-IA-Project/maximo_mcp.py` — evidencia principal de la implementación real.

## Documentación histórica recuperada

- `Bitácora de Proyecto: IA Generativa + MCP para IBM Maximo`.
- `Guía de Configuración Avanzada: Cline + MCP (Maximo, Filesystem y GitHub)`.
- HandOff Gemini → ChatGPT.

## Documentación actual del Learning Lab

- `mcp/README.md` — entrada al tema.
- `mcp/docs/MCP_PRACTICAL_WALKTHROUGH.md` — recorrido práctico resumido.
- `mcp/docs/MCP_LAB_HANDOFF.md` — cierre y continuidad.

---

# 27. Por qué trasladar este trabajo a `ai-eam-learning-lab` sí aporta valor

El traslado no se justifica por cambiar de herramienta de chat. Se justifica si produce **mejor memoria técnica, mejor evidencia y menos dependencia de conversaciones pasadas**.

## 27.1 GitHub pasa a ser memoria persistente

Antes, una parte sustancial del conocimiento estaba repartida entre chats, documentos y archivos locales.

Ahora:

```text
Chat
  ↓ razonar
Learning Lab GitHub
  ↓ persistir
Código + documentación + historial
```

Dentro de tres o seis meses no debería ser necesario reconstruir la conversación original.

## 27.2 Podemos contrastar documentación contra código

Este traslado ya produjo un beneficio tangible: aparecieron documentos históricos que describían un catálogo de 14 tools diferente del realmente implementado.

Al localizar `maximo_mcp.py`, se pudo determinar el catálogo correcto.

Eso convierte GitHub en una herramienta de **verificación**, no solo de almacenamiento.

## 27.3 Se elimina la dependencia de una sola IA

El conocimiento deja de pertenecer a Gemini, Claude, Cline o ChatGPT.

La secuencia correcta pasa a ser:

```text
IA de turno
   ↓
GitHub / artefactos
   ↓
contexto recuperable por cualquier IA futura
```

## 27.4 Se separa aprendizaje de producto

`ai-eam-learning-lab` conserva experimentos.

`ai-driven-eam-copilot` conserva decisiones e implementación del producto.

Esto permite experimentar rápido sin contaminar la arquitectura oficial.

## 27.5 La IA puede trabajar directamente sobre la fuente persistente

En este entorno se pudo:

- leer el código histórico directamente desde GitHub;
- auditar la documentación existente;
- detectar inconsistencias;
- corregir archivos del Learning Lab directamente en `main`;
- mantener un HandOff persistente;
- evitar pedir al usuario que copie y edite manualmente documentación técnica.

Ese es el beneficio operativo que debemos exigir en adelante.

---

# 28. Criterio de cierre

El laboratorio MCP histórico se considera cerrado porque:

- el objetivo de aprendizaje MCP básico fue alcanzado;
- existe evidencia de una ejecución MCP real en modo simulación;
- el artefacto principal fue recuperado y auditado;
- las 14 tools fueron verificadas en código;
- las configuraciones históricas relevantes quedaron documentadas de forma sanitizada;
- los límites de la prueba están explícitos;
- no es necesario repetir una PoC mínima que ya fue realizada.

El siguiente laboratorio independiente será **RAG**.

Nada de este documento constituye automáticamente una decisión de producto para AI-EAM-MAXIMO.
