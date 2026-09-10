# 🔌 MCP LAB — Documentación consolidada

> 🎯 **Propósito:** ser la fuente canónica, autosuficiente y vigente del Learning Lab para todo lo aprendido, construido, configurado y probado sobre **Model Context Protocol (MCP)** aplicado a EAM / IBM Maximo.
>
> 📍 **Estado del documento:** ✅ **APROBADO — baseline consolidada v1.1**
>
> 🧪 **Estado del laboratorio:** ✅ **CERRADO para el alcance actual de aprendizaje MCP**
>
> 🗓️ **Actualizado:** 2026-09-10
>
> ⚠️ **Conclusión que no debe perderse:** se validó una PoC MCP local con datos simulados y varias capacidades EAM; **no se validó una conexión viva ni operaciones reales contra IBM Maximo**.

## 🕘 Historial

| Versión | Fecha | Cambio |
|---|---:|---|
| **1.1** | 2026-09-10 | Mejora de recuperación rápida: índice descriptivo, aclaración JSON/JSON-RPC vs archivos `.json`, motivación Claude Desktop → Cline, explicación del “Tridente”, simplificación de fuentes, cronología consolidada, ubicación local histórica y referencia explícita al futuro laboratorio RAG. |
| **1.0** | 2026-09-10 | Consolidación integral y aprobada del laboratorio: se absorbe el conocimiento útil de Gemini / Claude / Cline, bitácoras, HandOffs, guía avanzada, notas locales, `MCP-Claude.zip`, código final e histórico, configuración real de Claude Desktop y revisión posterior en ChatGPT ↔ GitHub. Se corrigen contradicciones y conceptos con evidencia primaria y referencias MCP vigentes. |

---

## 🗺️ Índice de lectura

| Capítulo | Contenido en una frase |
|---|---|
| **0. Recuperación rápida** | Qué buscábamos, qué construimos, qué probamos y dónde está cada artefacto. |
| **1. Contexto, motivación y visión** | Problema EAM que originó la PoC y cómo MCP se complementa con RAG. |
| **2. Evidencia y fuentes** | Cómo distinguimos lo verificado, probado, documentado, inferido y no validado. |
| **3. Conceptos MCP** | Host, Client, Server, Tools, Resources, Prompts, transporte y flujo de mensajes. |
| **4. Evolución del laboratorio** | Recorrido Gemini → Claude Desktop → Cline → Tridente → ChatGPT ↔ GitHub. |
| **5. Cronología consolidada** | Hitos y fechas que sirven para recordar la secuencia del trabajo. |
| **6–8. Entorno, instalación y configuración** | Software, dependencias, rutas y configuración de Claude/Cline. |
| **9–16. PoC Maximo MCP** | Código, simulación, pruebas, 14 Tools y Working Set / confirmación. |
| **17–23. Aprendizajes y límites** | Multi-MCP, problemas encontrados, seguridad y aspectos no productivos. |
| **24–26. Continuidad técnica** | Ideas no implementadas, reproducción futura y relación con RAG. |
| **27–31. Cierre y mantenimiento** | Relación con AI-EAM-MAXIMO, ideas clave, fuentes y reglas futuras. |

> **Lectura sugerida:** para refrescar MCP en pocos minutos, leer primero el capítulo 0 y después [`MCP_LAB_FAST_READING.md`](MCP_LAB_FAST_READING.md).

---

# 0. Recuperación rápida — leer esto si vuelves dentro de varios meses

## 0.1 Qué queríamos aprender

Queríamos comprobar, **aprendiendo haciendo**, si una aplicación de IA podía recibir una petición en lenguaje natural, descubrir una capacidad externa y ejecutar una operación relacionada con EAM / IBM Maximo mediante MCP.

La idea de negocio que originó el experimento era reducir fricción en la gestión del mantenimiento: consultar OTs, inventario y activos, y eventualmente registrar o modificar información sin navegar manualmente por múltiples pantallas.

La cifra histórica de **~30 % de reducción del tiempo administrativo** fue una **hipótesis de valor**, no un beneficio medido.

## 0.2 Qué construimos

```text
Usuario
  ↓ lenguaje natural
Claude Desktop / VS Code + Cline
  ↓
MCP Client
  ↓ stdio
Servidor MCP local en Python
  ↓
maximo_mcp.py
  ├─ datos simulados
  └─ lógica HTTP/OSLC preparada → IBM Maximo (NO validada en vivo)
```

La PoC evolucionó además hacia un entorno multi-servidor, denominado informalmente **“Tridente MCP”**:

```text
Host de IA
   ├─ Maximo MCP      → lógica EAM / IBM Maximo
   ├─ Filesystem MCP  → archivos locales autorizados
   └─ GitHub MCP      → repositorios / investigación de código
```

## 0.3 Qué quedó probado

- un servidor MCP local en Python;
- descubrimiento e invocación de Tools desde Claude Desktop;
- pruebas EAM en `MODO_SIMULACION = True`;
- consulta de OTs e inventario;
- cambios de estado simulados;
- uso de Filesystem MCP para listar y escribir archivos;
- uso histórico de GitHub MCP para investigar implementaciones externas;
- evolución del servidor hasta **14 Tools**;
- patrón experimental de **Working Set / preview → confirmar o cancelar**;
- trabajo posterior con VS Code + Cline.

## 0.4 Qué NO quedó probado

- conexión a una instancia viva de IBM Maximo;
- lectura real desde Maximo;
- creación o modificación real de OTs;
- cambios de estado reales;
- workflow real;
- seguridad, autorización, observabilidad o resiliencia de producción;
- beneficio real del 30 %;
- RAG.

## 0.5 Dónde está lo importante ahora

```text
mcp/
├── README.md
├── src/
│   ├── maximo_mcp.py
│   └── history/
│       ├── connection_test.py
│       └── maximo_mcp_gemini_v1.py
├── config/
│   └── claude_desktop_config.example.json
└── docs/
    ├── MCP_LAB_DOCUMENTATION.md   ← ESTE DOCUMENTO
    └── MCP_LAB_HANDOFF.md
```

La documentación cruda procedente de Gemini/Claude/Cline fue utilizada como **fuente de reconstrucción**, no como documentación vigente. El lector futuro no debería necesitar volver a ella salvo para una auditoría histórica puntual.

## 0.6 Modelo mental de 60 segundos

> **MCP no es Maximo, no es RAG y no es un agente.**
>
> MCP es el protocolo que estandariza cómo una aplicación de IA se conecta con capacidades externas. En esta PoC, el MCP Server expone funciones EAM como Tools; esas funciones usan datos mock o, en una futura integración real, podrían invocar APIs/OSLC de Maximo.

---

# 1. Contexto, motivación y visión

## 1.1 Problema que originó el laboratorio

IBM Maximo es una plataforma EAM potente, pero muchas tareas cotidianas requieren navegar aplicaciones, pestañas, filtros y campos. La hipótesis de trabajo fue que una interfaz conversacional podría reducir esa fricción para planificadores, supervisores y personal de mantenimiento.

Ejemplos de necesidades imaginadas desde el principio:

- “¿Qué OTs abiertas siguen sin asignación?”
- “¿Cuántos rodamientos quedan en el almacén CENTRAL?”
- “¿Qué fallas ha tenido este equipo?”
- “Crea una OT correctiva para este activo.”
- “¿Cómo calibro este equipo según su manual?”
- “Revisa el historial y, si corresponde, propón un cambio de prioridad o estado.”

## 1.2 Visión más amplia

La visión inicial no se limitaba a MCP. Se imaginó una futura combinación:

```text
                    ┌─────────────────────────────┐
Usuario ───────────→│ Asistente / lógica de IA    │
                    └──────────────┬──────────────┘
                                   │
                  ┌────────────────┴────────────────┐
                  ↓                                 ↓
        MCP / datos transaccionales          RAG / conocimiento
        IBM Maximo Read & Write              manuales / procedimientos
                  ↓                                 ↓
             EAM estructurado                  texto no estructurado
```

Ejemplo conceptual:

> Una OT reporta alta temperatura en una bomba. El asistente consulta en Maximo si el problema ocurrió antes, recupera del manual los pasos de calibración y, si una regla lo justifica, **propone** una acción sobre la OT para confirmación humana.

En este laboratorio solo se trabajó la parte **MCP**. RAG quedó como línea posterior e independiente de aprendizaje. Cuando se inicie ese frente, su documentación viva y sus artefactos se mantendrán bajo la carpeta raíz `rag/` de este mismo repositorio. Hasta entonces no se crea esa carpeta, para evitar documentación prematura.

## 1.3 Contexto profesional

El laboratorio es una iniciativa de aprendizaje aplicada a la experiencia profesional en EAM / IBM Maximo. Su finalidad no era construir un producto final en esta etapa, sino comprender técnicamente el patrón y producir aprendizaje reutilizable para iniciativas AI-Driven EAM.

---

# 2. Cómo se construyó esta documentación y qué significa “evidencia”

## 2.1 Fuente vigente

A partir de esta consolidación, **este documento es la explicación vigente del laboratorio MCP**.

Los documentos previos de Gemini, Claude y Cline pasan a ser material fuente. Pueden conservarse temporalmente fuera o dentro de `history/`, pero no deben competir con esta documentación.

## 2.2 Jerarquía de evidencia

Cuando existen discrepancias se aplica este orden:

1. **Artefacto primario recuperado**: código, configuración real, salida o nota de sesión generada durante la prueba.
2. **Documentación contemporánea al experimento**: bitácoras, notas locales, HandOffs.
3. **Reconstrucciones posteriores**: resúmenes o documentos generados después.
4. **Inferencia**: conclusión razonable, siempre marcada como tal.

## 2.3 Etiquetas usadas

| Marca | Significado |
|---|---|
| ✅ **VERIFICADO** | Comprobado directamente en un artefacto primario recuperado. |
| 🧪 **PROBADO** | Comportamiento ejecutado durante el laboratorio y sustentado por evidencia de sesión/documentación. |
| 📘 **DOCUMENTADO** | Consta en las fuentes históricas, pero no se conserva evidencia primaria completa para repetir la comprobación. |
| 💡 **INFERIDO** | Conclusión obtenida al reconciliar varias evidencias. |
| ❌ **NO VALIDADO** | No existe prueba suficiente. |
| 🟨 **CANDIDATO AI-EAM-MAXIMO** | Aprendizaje potencialmente reutilizable en el producto; requiere decisión formal allí. |

## 2.4 Fuentes y ubicación de la evidencia

La consolidación utilizó **artefactos primarios** y **documentación histórica de transición**. Para la lectura normal no es útil mantener aquí el inventario completo de documentos antiguos; lo importante es saber dónde está la evidencia vigente:

| Evidencia | Ubicación vigente |
|---|---|
| Código final de la PoC | [`../src/maximo_mcp.py`](../src/maximo_mcp.py) |
| Código temprano recuperado | [`../src/history/`](../src/history/) |
| Configuración Claude sanitizada | [`../config/claude_desktop_config.example.json`](../config/claude_desktop_config.example.json) |
| Documentación completa | `MCP_LAB_DOCUMENTATION.md` — este documento |
| Resumen rápido | [`MCP_LAB_FAST_READING.md`](MCP_LAB_FAST_READING.md) |
| Estado / continuidad | [`MCP_LAB_HANDOFF.md`](MCP_LAB_HANDOFF.md) |

Las bitácoras, HandOffs, guías, notas y materiales provenientes de Gemini / Claude / Cline se usaron para reconstruir y contrastar el trabajo. Son **fuentes de referencia de transición**, no documentación vigente. Su conocimiento útil ya está absorbido aquí; solo es necesario volver a ellas ante una duda histórica o auditoría puntual.

---

# 3. MCP — conceptos que hay que recordar

## 3.1 Qué es MCP

**Model Context Protocol (MCP)** es un protocolo estándar para conectar aplicaciones de IA con capacidades y contexto externos de forma interoperable.

En términos prácticos, permite que una aplicación de IA descubra y utilice capacidades ofrecidas por uno o más MCP Servers sin que cada integración tenga que inventar un protocolo propio.

## 3.2 Host, Client y Server

### Host

Es la **aplicación o entorno de IA** con el que interactúa el usuario: por ejemplo, Claude Desktop, un IDE o un runtime agéntico.

> Corrección importante respecto de explicaciones antiguas: **el Host no es simplemente el PC físico**.

### Client

Es el componente dentro del Host que mantiene la comunicación MCP con un Server. Conceptualmente, existe una conexión cliente-servidor por cada MCP Server conectado.

### Server

Es el proceso que expone capacidades MCP. En nuestra PoC:

```text
maximo_mcp.py
```

era el MCP Server propio.

## 3.3 Tools, Resources y Prompts

### Tool

Capacidad invocable que permite ejecutar una operación.

Ejemplos del laboratorio:

```text
consultar_ot
consultar_inventario
crear_ot
cambiar_estado_ot
```

### Resource

Contenido o información que un Server puede exponer mediante una URI. No fue utilizado en nuestra PoC.

### Prompt

Plantilla de prompt expuesta por el Server. Tampoco fue utilizada en nuestra PoC.

> Nuestra implementación fue deliberadamente **Tool-centric**. Eso no significa que MCP sea únicamente un protocolo de Tools.

## 3.4 Transporte

El transporte lleva los mensajes entre Client y Server.

En este laboratorio se utilizó el patrón local **stdio**:

```text
Host
  ↓ lanza proceso hijo
python -u maximo_mcp.py
  ↓
stdin / stdout
  ↓
MCP
```

Para un servicio remoto, MCP contempla transporte HTTP. La PoC no necesitó desplegar un MCP Server HTTP.

## 3.5 Flujo de una Tool en nuestro laboratorio

```text
1. Usuario escribe una petición en lenguaje natural.
2. La aplicación de IA interpreta la intención.
3. El Host/Client conoce o descubre las Tools disponibles.
4. La IA decide que necesita una Tool.
5. El Client envía una invocación MCP al Server.
6. maximo_mcp.py ejecuta la función Python.
7. La función consulta mocks o intenta una llamada HTTP/OSLC.
8. El Server devuelve el resultado al Client.
9. La IA integra ese resultado y presenta la respuesta al usuario.
```

### ¿El intercambio entre componentes se realiza con archivos `.json`?

**No.** `claude_desktop_config.json` es un **archivo de configuración**: Claude Desktop lo lee para saber qué MCP Servers debe arrancar y con qué comandos. No se crea un archivo `.json` por cada solicitud o respuesta.

En nuestra PoC local se utilizó transporte **stdio**. Durante la ejecución, Client y Server intercambian **mensajes del protocolo serializados como JSON/JSON-RPC a través de `stdin` y `stdout`** del proceso:

```text
claude_desktop_config.json
        ↓ configura el arranque
Claude / MCP Client
        ↓ mensajes JSON-RPC por stdin
maximo_mcp.py
        ↓ ejecuta Tool
        ↑ respuesta JSON-RPC por stdout
Claude / MCP Client
```

Conviene recordar la diferencia:

- **archivo `.json`** → configuración persistida en disco;
- **mensaje JSON/JSON-RPC** → información que viaja durante la sesión MCP;
- **stdio** → canal local de transporte utilizado en esta PoC.

## 3.6 MCP no convierte por sí solo al LLM en agente

Una explicación histórica decía que MCP permite pasar de “asistente de chat” a “agente de acción”. La intuición era útil, pero técnicamente necesita precisión:

> **MCP proporciona acceso estandarizado a capacidades. La autonomía, planificación, permisos y decisión de usar esas capacidades dependen del Host o del sistema agéntico.**

Cline aportaba capacidades agénticas —edición de archivos, terminal, revisión de diffs y uso de Tools—; MCP era uno de los mecanismos de integración que Cline podía utilizar.

## 3.7 MCP no sustituye las APIs de Maximo

En esta PoC:

```text
MCP Tool
   ↓
función Python
   ↓
requests
   ↓
OSLC / REST de Maximo
```

Por tanto, MCP puede actuar como **frontera orientada a IA** mientras APIs/OSLC siguen siendo el mecanismo subyacente para comunicarse con Maximo.

## 3.8 “Local” no significa “automáticamente seguro”

El trabajo local redujo infraestructura y evitó tener que publicar un servicio web propio para la PoC, pero no garantiza seguridad por sí mismo.

Todavía deben gobernarse:

- qué carpetas puede leer el Filesystem MCP;
- qué permisos tiene un token GitHub;
- qué credenciales de Maximo se usan;
- qué Tools pueden escribir;
- qué información sale hacia el proveedor del modelo;
- auditoría y trazabilidad;
- autorización por usuario;
- exposición a contenido no confiable y prompt injection.

---

# 4. Evolución histórica consolidada

## 4.1 Fase 0 — idea funcional

La iniciativa comenzó con una pregunta de negocio: **¿podemos usar IA Generativa como interfaz conversacional sobre IBM Maximo para reducir trabajo administrativo y mejorar acceso a información de mantenimiento?**

La presentación conceptual ya anticipaba una arquitectura futura con:

```text
AI + MCP-MAXIMO + RAG Knowledge Base
```

y separaba implícitamente:

- datos EAM estructurados / transaccionales;
- conocimiento técnico no estructurado.

## 4.2 Fase 1 — exploración con Gemini / Google Cloud

Gemini fue utilizado inicialmente como entorno de razonamiento y desarrollo.

Se exploró una posible integración mediante Google Cloud / Vertex AI. Para una PoC local, se percibió como una vía con demasiado coste de entrada: despliegue, endpoints, red, certificados y configuración cloud antes de haber comprobado el mecanismo básico.

### Decisión

Reducir complejidad y llevar la primera prueba a un entorno local con Claude Desktop + MCP.

> La decisión fue apropiada para **aprender el mecanismo**. No implica que una arquitectura cloud sea incorrecta para producción.

## 4.3 Fase 2 — prueba mínima de conectividad MCP

Se creó un script mínimo cuyo único objetivo era responder:

> “¿Claude puede ver e invocar una Tool que yo expongo desde Python?”

Artefacto recuperado:

```text
src/history/connection_test.py
```

La Tool era:

```python
@mcp.tool()
def verificar_conexion() -> str:
    return "Conexión exitosa con el servidor de Maximo"
```

Esta frase histórica era engañosa: la prueba demostraba la ruta **Claude ↔ MCP Server local**, no una conexión con IBM Maximo.

## 4.4 Fase 3 — primera versión orientada a Maximo

Se recuperó una versión temprana desarrollada con apoyo de Gemini:

```text
src/history/maximo_mcp_gemini_v1.py
```

Contenía al menos:

- `consultar_ot`;
- `consultar_inventario`;
- `MODO_SIMULACION`;
- rama HTTP/OSLC prevista;
- `FastMCP`.

Esta versión permite ver cómo la PoC pasó de una Tool de conectividad a capacidades con semántica EAM.

## 4.5 Fase 4 — ampliación funcional

Las bitácoras describen una etapa intermedia de “4 Tools”. No se conserva un artefacto primario exactamente de cuatro Tools.

La nota de sesión del 20-04-2026 documenta ya el uso de:

- `verificar_conexion`;
- `consultar_ot`;
- `listar_transiciones_ot`;
- `cambiar_estado_ot`;
- `consultar_inventario`.

Por ello, **“4 Tools” se conserva como hito narrativo documentado**, no como inventario primario exacto.

## 4.6 Fase 5 — VS Code + Cline

Se instaló Cline en VS Code principalmente para **reducir la fricción del ciclo de desarrollo y prueba**.

Con Claude Desktop, cuando se modificaba la configuración MCP o era necesario recargar el servidor, el procedimiento documentado era más pesado: cerrar Claude Desktop completamente —incluyendo salir desde la bandeja del sistema—, volver a abrirlo, entrar en `Settings → Developer`, comprobar/activar el servidor y ejecutar otra prueba. Ese ciclo resultaba incómodo mientras se iteraba repetidamente sobre código y configuración.

Cline permitió concentrar edición, revisión y prueba dentro de VS Code:

```text
pedir cambio
   ↓
Cline abre/modifica código
   ↓
muestra diff
   ↓
usuario revisa/aprueba
   ↓
refresco/reinicio del MCP Server
   ↓
prueba desde el mismo entorno
```

La mejora no fue solo evitar copiar/pegar código: **redujo el coste de iterar sobre el servidor MCP durante el aprendizaje**.

## 4.7 Fase 6 — “Tridente MCP”

Se configuraron tres servidores:

```text
Maximo MCP + Filesystem MCP + GitHub MCP
```

El nombre informal **“Tridente MCP”** se utilizó precisamente porque un **tridente tiene tres puntas** y nuestro entorno combinaba tres MCP Servers especializados.

> El nombre **“Tridente MCP”** es propio del laboratorio; no pertenece al estándar MCP ni identifica un patrón oficial.

## 4.8 Fase 7 — investigación con GitHub MCP y expansión

Se documentó la petición:

> buscar en GitHub otros servidores MCP relacionados con Maximo y comparar capacidades que todavía no existieran localmente.

Las fuentes históricas registran, entre otros:

- `markusvankempen/maximo-mcp-ai-integration-options`;
- `soumyaprasadrana/maximo-mcp-server`.

Después se documentó una expansión hasta 14 Tools.

El código final recuperado permite verificar cuáles fueron realmente esas 14 funciones.

## 4.9 Fase 8 — traslado a ChatGPT ↔ GitHub

En septiembre de 2026 se decidió trasladar la memoria del trabajo a un modelo más organizado:

```text
Chat / razonamiento
       ↕
GitHub / persistencia
```

Se creó `jperdomo12/ai-eam-learning-lab` como repositorio de aprendizaje independiente del producto `ai-driven-eam-copilot`.

La documentación cruda de Gemini pasó a ser **fuente de reconstrucción**, y el objetivo cambió de “conservar documentos viejos” a **mantener documentación viva, revisada y autosuficiente**.

---

# 5. Cronología consolidada

Para recuperar el laboratorio meses después basta con conservar la secuencia consolidada. Las discrepancias encontradas durante la migración ya fueron analizadas al construir esta baseline y no forman parte de la lectura normal.

| Fecha | Hito | Evidencia principal |
|---|---|---|
| Abril 2026 | prueba mínima MCP local | script de conectividad + notas |
| 20-04-2026 | sesión funcional Claude + MCP Maximo en simulación | notas de sesión |
| 21-04-2026 | configuración de Cline y réplica de servidores MCP | notas contemporáneas |
| 09-09-2026 | consolidación del “Tridente” y expansión documentada a 14 Tools | bitácora + código final |
| 10-09-2026 | migración, auditoría y consolidación en `ai-eam-learning-lab` | GitHub + ChatGPT |

> Si alguna vez fuese necesario auditar una discrepancia histórica concreta, se volverá a las fuentes de transición originales.

---

# 6. Entorno y componentes utilizados

| Componente | Papel en el laboratorio |
|---|---|
| Windows | sistema operativo local |
| Visual Studio Code | IDE |
| extensión Python | soporte de desarrollo |
| Python | runtime del MCP Server |
| Claude Desktop | primer Host utilizado para la PoC |
| Cline | entorno posterior dentro de VS Code |
| MCP Python SDK / FastMCP | servidor MCP en Python |
| `requests` | llamadas HTTP/HTTPS previstas hacia Maximo |
| `urllib3` | tratamiento/supresión de warnings SSL en la PoC |
| Node.js / `npx` | ejecución de MCP Servers adicionales |
| Filesystem MCP | acceso delimitado a carpetas locales |
| GitHub MCP | investigación/acceso a GitHub |
| IBM Maximo | sistema objetivo; **no conectado realmente** |

## 6.1 Python

El HandOff histórico especifica **Python 3.14** instalado en el equipo.

Otras guías usaron “Python 3.10+” como requisito general. Ambas afirmaciones pueden convivir:

- **entorno histórico usado:** Python 3.14 según el HandOff;
- **requisito general actual del SDK MCP v2:** Python 3.10+.

## 6.2 Dependencias Python

Comando documentado:

```bash
pip install mcp requests urllib3
```

El código recuperado importa:

```python
from mcp.server.fastmcp import FastMCP
```

Esto identifica el script como código de la línea histórica **MCP Python SDK v1.x**.

## 6.3 Node.js / npx

Se incorporó para ejecutar servidores distribuidos como paquetes Node, concretamente Filesystem MCP y el GitHub MCP usado en aquel momento.

## 6.4 Ubicación local histórica

La carpeta local utilizada para el laboratorio fue:

```text
C:\Users\jpperdomo\JP\Profesional\IA\MCP-Claude
```

El script principal se encontraba en:

```text
C:\Users\jpperdomo\JP\Profesional\IA\MCP-Claude\maximo_mcp.py
```

Esta ubicación se conserva como referencia de reconstrucción del entorno histórico; no es una ruta portable ni un requisito para futuras pruebas.

---

# 7. Instalación y configuración realizadas

## 7.1 Secuencia práctica reconstruida

```text
1. Instalar VS Code.
2. Instalar la extensión Python.
3. Instalar Python.
4. Corregir PATH porque python/pip no eran reconocidos.
5. Instalar dependencias MCP/HTTP.
6. Instalar Claude Desktop.
7. Crear el servidor MCP mínimo.
8. Localizar el archivo real de configuración de Claude.
9. Registrar el MCP Server Maximo.
10. Reiniciar Claude y ejecutar la primera Tool.
11. Añadir capacidades EAM simuladas.
12. Incorporar Node.js/npx.
13. Añadir Filesystem MCP.
14. Añadir GitHub MCP.
15. Instalar/configurar Cline en VS Code.
16. Investigar implementaciones externas y ampliar Tools.
17. Consolidar el trabajo en GitHub.
```

## 7.2 Incidencia: Python y pip no estaban en PATH

### Problema

Windows no encontraba:

```bash
python
pip
```

### Solución

Se actualizaron las Variables de Entorno de Windows para incluir Python y su directorio `Scripts`.

### Comprobación

```bash
python --version
```

## 7.3 Lección

Antes de depurar MCP, comprobar primero el runtime. Un error de PATH puede parecer un problema de MCP aunque ocurra antes de que el protocolo entre en juego.

---

# 8. Configuración de Claude Desktop

## 8.1 Cómo se localizó el archivo correcto

La instalación utilizada era la versión de Windows Store.

La forma que funcionó y que debe recordarse es:

```text
Claude Desktop
→ Configuración
→ Desarrollador
→ Editar configuración
```

La ubicación efectiva correspondía al patrón:

```text
%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json
```

Una ruta bajo `%APPDATA%\Anthropic\Claude` apareció en documentación anterior, pero **no era la ubicación efectiva de la instalación usada**.

## 8.2 Configuración real recuperada

El archivo real aportado posteriormente confirmó tres servidores MCP:

```json
{
  "mcpServers": {
    "maximo": {
      "command": "C:/Users/<USUARIO>/AppData/Local/Python/bin/python.exe",
      "args": [
        "-u",
        "C:/Users/<USUARIO>/<RUTA-LAB>/maximo_mcp.py"
      ]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:/Users/<USUARIO>/<DIRECTORIO-AUTORIZADO-1>",
        "C:/Users/<USUARIO>/<DIRECTORIO-AUTORIZADO-2>"
      ]
    },
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
}
```

La copia pública sanitizada está en:

```text
mcp/config/claude_desktop_config.example.json
```

## 8.3 Qué significa cada parte

### `command`

Programa que el Host debe ejecutar.

Para Maximo se utilizó una ruta absoluta a `python.exe`.

### `args`

Argumentos suministrados al proceso.

```text
-u
```

ejecuta Python en modo sin buffering de stdout/stderr, útil para un servidor que se comunica por stdio.

Después se indica la ruta absoluta al script:

```text
maximo_mcp.py
```

### Filesystem MCP

Los últimos argumentos son las carpetas a las que el servidor puede acceder. Esto constituye un **límite de permisos** y debe mantenerse tan reducido como sea posible.

### GitHub MCP

El servidor histórico recibía un PAT mediante:

```text
GITHUB_PERSONAL_ACCESS_TOKEN
```

Nunca debe publicarse un token real en Git.

## 8.4 Cómo se veía desde Claude

Las notas indican que desde un chat de Claude, usando el control `+` y la opción de conectores, podían visualizarse servicios como `maximo` y `filesystem`.

Esto es una nota de la interfaz histórica utilizada; la UI actual puede cambiar.

## 8.5 Reinicio de Claude

El flujo histórico para recargar cambios era:

```text
1. Cerrar Claude completamente.
2. Salir desde el icono de la bandeja del sistema (Quit).
3. Abrir Claude de nuevo.
4. Ir a Configuración → Desarrollador.
5. Comprobar que el MCP Server aparece activo.
6. Ejecutar una prueba.
```

---

# 9. Configuración de VS Code + Cline

## 9.1 Motivo de la transición

Claude Desktop era adecuado para usar Tools, pero el ciclo de desarrollo requería copiar/pegar o reiniciar con frecuencia.

Cline se adoptó para trabajar directamente dentro del IDE.

## 9.2 Ruta histórica de configuración

La nota local del 21-04-2026 indica:

```text
%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
```

Se copiaron manualmente los mismos servidores configurados en Claude.

📘 **DOCUMENTADO:** en esa sesión no se pudo realizar la configuración desde la interfaz gráfica y se editó el JSON directamente.

## 9.3 Evidencia disponible

El archivo real `cline_mcp_settings.json` **no fue recuperado** durante la consolidación.

Por tanto:

- la ruta y el procedimiento están documentados;
- la configuración exacta se infiere de las notas;
- no se presenta como artefacto primario actual.

## 9.4 “Hot reload” / refresh

La guía histórica describe que Cline permitía refrescar o reiniciar el servidor MCP desde el propio entorno, reduciendo la necesidad de cerrar VS Code.

Esto debe entenderse como comportamiento de la versión utilizada entonces, no como contrato del protocolo MCP ni garantía de versiones actuales.

---

# 10. El “Tridente MCP”

## 10.1 Qué era

```text
                   Host / entorno de IA
                           │
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
      Maximo MCP      Filesystem MCP     GitHub MCP
          │                │                │
          ↓                ↓                ↓
   lógica EAM/OSLC    archivos locales   repositorios
```

## 10.2 Maximo MCP

Servidor propio:

```text
mcp/src/maximo_mcp.py
```

Exponía funciones con semántica EAM.

## 10.3 Filesystem MCP

Permitía leer y escribir únicamente dentro de directorios autorizados.

Pruebas documentadas:

- listar archivos del laboratorio;
- escribir un archivo mediante la Tool del servidor.

## 10.4 GitHub MCP

Se utilizó para investigar repositorios y comparar implementaciones.

Prueba destacada:

```text
buscar otros MCP Servers relacionados con Maximo
→ identificar capacidades faltantes
→ proponer/incorporar mejoras
```

## 10.5 Qué aprendimos

MCP permite que un mismo Host combine servidores especializados. No es necesario construir un “super-servidor” que haga todo.

---

# 11. `maximo_mcp.py` — arquitectura del código

## 11.1 Artefacto vigente del laboratorio

```text
mcp/src/maximo_mcp.py
```

La copia adjuntada directamente durante la consolidación es idéntica, por SHA-256, al `maximo_mcp.py` contenido en `MCP-Claude.zip`.

SHA-256 comprobado durante la consolidación:

```text
1b0a61ba0882f4fe5a38c8a276464e8990a1117335c0a4e8d89d95fa28987aea
```

Esto elimina la dependencia del repositorio temporal de prueba que fue eliminado.

## 11.2 Estructura principal

```text
Configuración
  ↓
Datos mock
  ↓
Reglas de negocio simuladas
  ↓
helpers HTTP/OSLC
  ↓
14 Tools MCP
  ↓
mcp.run()
```

## 11.3 Configuración

```python
MODO_SIMULACION = True
MAXIMO_URL = "https://TU_SERVIDOR/maximo"
API_KEY = "TU_API_KEY_AQUÍ"
```

Los valores son placeholders, no credenciales reales.

## 11.4 Datos mock

El script final contiene datasets simulados para:

- OTs;
- inventario;
- activos;
- workflow;
- catálogo de Object Structures.

Ejemplos del dataset final:

```text
OT-1001 ... OT-1005
SKF-6204 / CENTRAL
BOMBA-B201
COMP-C305
WF-001 / WF-002
MXWO / MXWODETAIL / MXASSET / MXINVENTORY / ...
```

## 11.5 Reglas simuladas de estado

El código contiene un mapa local:

```text
WAPPR → APPR / CAN
APPR  → WMATL / INPRG / CAN
INPRG → COMP / WMATL
COMP  → CLOSE
WMATL → INPRG / CAN
CLOSE → terminal
CAN   → terminal
```

Estas reglas ayudaron a probar lógica de interacción, pero **no deben tratarse como verdad universal de una instalación Maximo**.

## 11.6 Helpers

El script define helpers para:

- cabeceras HTTP;
- construcción de URL OSLC;
- construcción de URL API.

La rama real usa `requests` y API key.

---

# 12. Lógica dual — simulación vs. Maximo real

## 12.1 Modo utilizado en las pruebas

```python
MODO_SIMULACION = True
```

Ese modo:

- no llama a Maximo;
- trabaja con diccionarios Python;
- permite probar selección de Tools;
- permite ejecutar lecturas y escrituras simuladas;
- evita riesgo sobre datos reales;
- desacopla aprendizaje MCP de infraestructura EAM.

## 12.2 Rama real prevista

```python
MODO_SIMULACION = False
```

El código contiene ramas HTTP que intentan operaciones sobre Maximo mediante OSLC/REST.

Aparecen, entre otros:

- `GET` para consultas;
- `POST` para creación/acciones;
- `x-method-override: PATCH` en algunas actualizaciones;
- API key en cabecera;
- `timeout`;
- `verify=False`.

## 12.3 Punto crítico

❌ **NO VALIDADO:** la existencia de código HTTP no demuestra que los endpoints, payloads, acciones o reglas sean correctos para una instancia real de Maximo.

En particular, deben verificarse contra una instancia concreta:

- Object Structures disponibles;
- nombres y paths;
- autenticación;
- permisos;
- acciones de workflow;
- transiciones de estado;
- comportamiento PATCH/POST;
- campos obligatorios;
- site/org;
- configuración de integración.

---

# 13. Catálogo final — 14 Tools verificadas

El código final contiene exactamente **14 funciones decoradas con `@mcp.tool()`**.

| # | Tool | Tipo | Simulación | Rama real prevista | Impacto |
|---:|---|---|---|---|---|
| 1 | `consultar_ot` | lectura | consulta `OT_MOCK` | `GET MXWODETAIL` | bajo |
| 2 | `consultar_inventario` | lectura | consulta `INVENTARIO_MOCK` | `GET MXINVENTORY` | bajo |
| 3 | `listar_transiciones_ot` | lectura/lógica | usa tabla local de estados | consulta OT + tabla local | bajo |
| 4 | `cambiar_estado_ot` | escritura | modifica estado mock | `GET` + `POST/PATCH override` | alto |
| 5 | `query_maximo` | lectura genérica | filtra mocks básicos | `GET` Object Structure parametrizada | medio/alto |
| 6 | `consultar_activo` | lectura | consulta `ACTIVOS_MOCK` | `GET MXASSET` | bajo |
| 7 | `listar_object_structures` | introspección | catálogo mock | `GET /api/meta/os` | bajo |
| 8 | `crear_ot` | escritura | crea OT mock | `POST MXWODETAIL` | alto |
| 9 | `ws_editar_ot` | preparación | crea Working Set en memoria | lee OT y prepara cambios | medio |
| 10 | `ws_confirmar_cambios` | escritura | aplica cambios mock | `POST/PATCH override` | alto |
| 11 | `ws_cancelar_cambios` | control | elimina Working Set | elimina Working Set local | bajo |
| 12 | `obtener_workflow_assignments` | lectura | consulta workflow mock | `GET` assignments | medio |
| 13 | `enviar_workflow_response` | acción | procesa workflow mock | `GET` + `POST action` | alto |
| 14 | `verificar_conexion` | diagnóstico | devuelve estado simulado | `GET /api/whoami` | bajo |

## 13.1 Tool 1 — `consultar_ot`

Objetivo: obtener información de una Orden de Trabajo.

Entrada:

```text
num_ot
```

En simulación devuelve descripción, estado, activo, sitio, tipo, prioridad y transiciones permitidas.

## 13.2 Tool 2 — `consultar_inventario`

Objetivo: consultar disponibilidad y ubicación de un artículo.

Entradas:

```text
item_num
almacen = CENTRAL
```

## 13.3 Tools 3 y 4 — estados

`listar_transiciones_ot` muestra los destinos permitidos según la tabla local.

`cambiar_estado_ot` valida la transición y modifica la OT mock; la rama real intenta persistir el cambio.

## 13.4 Tool 5 — `query_maximo`

Es una Tool genérica que recibe:

```text
object_structure
where
select
order_by
page_size
```

Fue útil para explorar flexibilidad OSLC, pero su amplitud requeriría controles estrictos en producción.

## 13.5 Tools 6 y 7 — activos y Object Structures

- `consultar_activo`: consulta un activo concreto.
- `listar_object_structures`: intenta descubrir el catálogo de Object Structures.

## 13.6 Tool 8 — `crear_ot`

Prueba el patrón de creación de una OT con:

- descripción;
- activo;
- sitio;
- tipo de trabajo;
- prioridad;
- memo.

## 13.7 Tools 9, 10 y 11 — Working Set

```text
ws_editar_ot
   ↓ preview
   ├─ ws_confirmar_cambios
   └─ ws_cancelar_cambios
```

Es una aproximación explícita a Human-in-the-Loop.

## 13.8 Tools 12 y 13 — Workflow

Permiten simular:

- consulta de asignaciones;
- aprobación/rechazo/respuesta.

La rama real debe tratarse como prototipo no validado.

## 13.9 Tool 14 — `verificar_conexion`

En simulación devuelve:

```text
“Conexión exitosa...”
Modo: SIMULACIÓN
Tools disponibles: 14
```

### Corrección conceptual

Cuando `MODO_SIMULACION = True`, esta Tool **no verifica IBM Maximo**. Verifica, de forma práctica, que el MCP Server se está ejecutando y que la Tool puede invocarse.

La rama real sí intenta:

```text
GET /api/whoami
```

pero no fue validada en una instancia viva.

---

# 14. Evolución del catálogo y contradicción de las “14 Tools”

Una bitácora histórica llegó a listar como Tools 13 y 14:

```text
consultar_ubicacion
generar_reporte_local
```

Otra memoria posterior incluyó nombres como:

```text
obtener_resumen_activos
obtener_status_server
```

Esos nombres **no aparecen en el código final recuperado**.

### Decisión documental

✅ Para afirmar qué estuvo implementado en el artefacto final, manda `mcp/src/maximo_mcp.py`.

El catálogo correcto es el de la sección anterior.

Las listas diferentes se conservan únicamente como evidencia de que la documentación histórica tuvo inconsistencias o describió propuestas/intermedios que no corresponden al archivo final.

---

# 15. Working Set y Human-in-the-Loop

## 15.1 Qué se quiso probar

Las operaciones de escritura sobre un EAM pueden tener impacto operacional. Se exploró la idea de no aplicar inmediatamente cualquier cambio propuesto por la IA.

## 15.2 Patrón

```text
Usuario pide modificación
       ↓
IA prepara cambio
       ↓
Working Set
       ↓
preview de antes / después
       ↓
  decisión humana
   ↙            ↘
confirmar      cancelar
```

## 15.3 Cómo se implementó

El Working Set era un diccionario en memoria:

```python
_working_set: dict = {}
```

Por tanto:

- desaparece si el proceso termina;
- no soporta persistencia real;
- no representa una función nativa de IBM Maximo;
- no resuelve concurrencia ni identidad de usuarios.

## 15.4 Aprendizaje

El patrón **proponer → revisar → confirmar** sí es reutilizable conceptualmente y resulta especialmente importante para futuras acciones de escritura EAM.

---

# 16. Pruebas realizadas y evidencia

## 16.1 Prueba 1 — conectividad MCP mínima

### Objetivo

Confirmar que Claude Desktop descubre una Tool expuesta por Python.

### Script

```text
src/history/connection_test.py
```

### Resultado

🧪 **PROBADO:** Claude pudo invocar `verificar_conexion`.

### Qué demostró

```text
Claude Desktop ↔ MCP ↔ Python
```

### Qué NO demostró

```text
Python ↔ IBM Maximo
```

## 16.2 Prueba 2 — consulta de OT

La documentación registra consultas como:

```text
“Consulta la información de la orden de trabajo OT-2025”
```

La nota de sesión del 20-04-2026 registra:

```text
OT-2025
Mantenimiento preventivo de motor principal
APROB
MOT-105
```

El dataset final ya no contiene `OT-2025`, lo que indica que los mocks evolucionaron entre versiones.

## 16.3 Prueba 3 — inventario

Consulta:

```text
SKF-6204
almacén CENTRAL
```

Resultado documentado:

```text
15 unidades
PASILLO-B2-ESTANTE4
```

El mismo dato existe en el mock final.

## 16.4 Prueba 4 — cambio de estado OT-1002

Documentado:

```text
INPRG → WMATL
memo: “Esperando por el proveedor”
```

Fue una modificación en memoria sobre datos simulados.

## 16.5 Prueba 5 — cambio de estado OT-1001

Documentado:

```text
APPR → INPRG
memo: “Técnico García asignado”
```

También fue simulada.

## 16.6 Prueba 6 — Filesystem MCP

Se documentó el listado de archivos del directorio del laboratorio, incluyendo:

```text
IA-Claude_Notas Varias.txt
maximo_mcp.py
OLD/
```

También se utilizó la capacidad de escritura de Filesystem MCP.

## 16.7 Prueba 7 — GitHub MCP

Se solicitó investigar otros MCP Servers de Maximo.

Resultado documentado:

- se encontraron repositorios de terceros;
- se compararon capacidades;
- se propuso ampliar el servidor;
- la bitácora registra evolución “4 → 14 Tools”.

✅ El estado final de **14 Tools** está verificado en el código.

📘 La atribución exacta de cada Tool a un repositorio externo concreto **no está demostrada**.

## 16.8 Convención visual utilizada

Se adoptó:

```text
🧪 [SIMULACIÓN]
```

para datos mock y se diseñó:

```text
✅ [REAL]
```

para la rama real.

La etiqueta `[REAL]` solo sería válida si la rama correspondiente hubiera ejecutado realmente contra Maximo; durante este laboratorio eso no ocurrió.

---

# 17. Operación cotidiana histórica

## 17.1 Con Claude Desktop

```text
modificar maximo_mcp.py
→ cerrar Claude completamente
→ abrir Claude
→ verificar servidor en Developer
→ ejecutar consulta de prueba
```

## 17.2 Con Cline

El flujo pasó a ser:

```text
pedir modificación
→ Cline edita
→ revisar diff
→ Approve
→ refrescar/reiniciar servidor MCP
→ probar
```

La guía utilizaba la analogía:

- Claude Desktop = “consultor” que entrega receta;
- Cline = “operario” que trabaja sobre el archivo.

La analogía ayuda a recordar la diferencia de experiencia, pero la formulación técnica preferida es:

> Cline añadía capacidades agénticas y de Computer/IDE tooling; MCP seguía siendo el protocolo para exponer o consumir determinadas capacidades.

---

# 18. Problemas encontrados y cómo se resolvieron

| Problema | Causa / contexto | Resolución |
|---|---|---|
| `python` / `pip` no reconocidos | PATH de Windows | añadir rutas correctas y validar con `python --version` |
| Claude no veía el MCP Server | se editó un config que no era el efectivo | usar `Configuración → Desarrollador → Editar configuración` |
| no había Maximo real disponible | dependencia de infraestructura | `MODO_SIMULACION = True` + mocks |
| ciclo de cambios lento en Claude | recarga del servidor al arrancar | evolución a VS Code + Cline |
| necesidad de trabajar con archivos | chat por sí solo no tenía ese acceso | Filesystem MCP con carpetas explícitas |
| necesidad de investigar código | comparar implementaciones externas | GitHub MCP |
| riesgo de aplicar cambios sin revisión | operaciones EAM de escritura | Working Set experimental |

---

# 19. Decisiones y aprendizajes consolidados

## 19.1 Empezar por una Tool mínima

Fue acertado separar primero:

```text
¿funciona MCP?
```

de:

```text
¿funciona Maximo?
```

La Tool `verificar_conexion` permitió aislar el primer problema.

## 19.2 Simular antes de integrar

El modo simulación permitió aprender:

- Tool discovery;
- parámetros;
- respuestas;
- flujos de lectura;
- flujos de escritura;
- workflow;
- confirmación.

sin depender de VPN, API keys ni Maximo.

## 19.3 Usar semántica EAM en las Tools

Es más comprensible exponer:

```text
consultar_ot
crear_ot
consultar_inventario
```

que obligar al modelo a razonar siempre en términos de endpoints HTTP.

Esta idea debe equilibrarse con no proliferar cientos de Tools demasiado específicas.

## 19.4 Separar servidores por responsabilidad

El Tridente mostró que cada MCP Server puede tener un ámbito distinto:

```text
EAM
archivos
GitHub
```

Eso favorece composición y separación de permisos.

## 19.5 Controlar las escrituras

El Working Set fue una primera aproximación al principio:

```text
IA propone
humano valida
sistema ejecuta
```

## 19.6 MCP + OSLC/REST es una composición natural

MCP no elimina el conocimiento de Maximo. El servidor sigue necesitando:

- Object Structures;
- reglas de negocio;
- autenticación;
- autorización;
- API semantics;
- validación de payloads.

## 19.7 La documentación debe distinguir lenguaje atractivo de evidencia

Expresiones históricas como:

- “conexión directa y segura”;
- “agente autónomo”;
- “conexión exitosa con Maximo”;

eran útiles como narrativa, pero podían sobreafirmar lo probado.

La documentación actual separa con rigor:

```text
hecho / probado / verificado / inferido / no validado
```

---

# 20. Marco de adopción de IA explorado históricamente

Una memoria de Gemini introdujo una progresión atribuida a un marco de adopción/confianza de IA:

```text
Guide → Observer → Collaborator → Delegate
```

y la usó para pensar la evolución de la solución:

- **Guide:** consulta y presentación de información;
- **Observer:** análisis y detección de patrones;
- **Collaborator:** propuesta/escritura con confirmación humana;
- **Delegate:** automatización más autónoma bajo reglas.

### Estado de esta idea

📘 **DOCUMENTADO COMO MARCO DE REFLEXIÓN HISTÓRICO.**

No se conserva en el corpus una fuente primaria de IBM que permita afirmar que esta taxonomía exacta sea un estándar oficial de IBM EAM. Por ello no se adopta como marco normativo del Learning Lab ni de AI-EAM-MAXIMO sin verificación independiente.

La idea sí sigue siendo útil para razonar sobre **niveles crecientes de autonomía y confianza**.

---

# 21. Estado tecnológico actual a septiembre de 2026

Esta sección diferencia **lo que usamos históricamente** de **cómo está hoy el ecosistema**.

## 21.1 MCP Python SDK

El script histórico usa:

```python
from mcp.server.fastmcp import FastMCP
```

Eso corresponde a MCP Python SDK v1.x.

A septiembre de 2026, la documentación oficial del SDK indica que **v2 es la línea estable** y que:

```text
FastMCP → MCPServer
```

Por tanto, el script conservado es un **artefacto histórico funcional para el aprendizaje**, no un ejemplo actualizado de API v2.

## 21.2 Si se ejecutara el script histórico sin modificar

La documentación oficial de la línea v1 recomienda fijar una versión `<2` para evitar que la importación antigua deje de funcionar.

Conceptualmente:

```text
mcp>=1.x,<2
```

La versión exacta debería elegirse/reproducirse en un experimento dedicado, no asumirla desde esta documentación.

## 21.3 Si se modernizara

La migración principal comenzaría por:

```python
from mcp.server import MCPServer
```

o la ruta vigente indicada por el SDK v2, sustituyendo la antigua clase `FastMCP`.

Después habría que revisar:

- transporte;
- tipos;
- autenticación;
- pruebas;
- cambios de comportamiento de v2.

## 21.4 Transportes vigentes

El ecosistema actual mantiene:

- **stdio** para integraciones locales donde el Host lanza el proceso;
- **Streamable HTTP** para servidores remotos.

La PoC histórica utilizó **stdio**.

## 21.5 GitHub MCP

La configuración histórica usó:

```text
@modelcontextprotocol/server-github
```

La documentación actual del **GitHub MCP Server oficial** indica que aquel paquete npm ya no es la opción soportada.

Por tanto:

> conservarlo en `claude_desktop_config.example.json` sirve para reproducir **qué configuramos históricamente**, no para recomendar una instalación nueva en 2026.

Una recreación moderna debería consultar la implementación oficial `github/github-mcp-server` y usar su autenticación/configuración vigente.

---

# 22. Seguridad y PAT de GitHub

## 22.1 Cómo se usó históricamente

El config contenía:

```json
"env": {
  "GITHUB_PERSONAL_ACCESS_TOKEN": "<SECRET>"
}
```

El archivo público conserva únicamente `<SECRET>`.

## 22.2 Regla actual

Nunca:

- pegar un PAT real en documentación pública;
- guardar un PAT en Git;
- reutilizar tokens excesivamente privilegiados;
- exponer tokens en capturas o chats sin necesidad.

## 22.3 Generar un token si una integración vigente lo requiere

En GitHub:

```text
Settings
→ Developer settings
→ Personal access tokens
→ Fine-grained tokens
→ Generate new token
```

Aplicar:

- repositorios mínimos necesarios;
- permisos mínimos;
- expiración razonable;
- rotación;
- revocación cuando deje de utilizarse.

> Antes de crear un PAT, revisar si el MCP Server/Host vigente soporta OAuth u otro mecanismo más adecuado.

---

# 23. Qué NO debe copiarse a producción

El código fue válido como laboratorio, pero contiene deuda deliberada.

## 23.1 TLS

```python
verify=False
```

y:

```python
urllib3.disable_warnings(...)
```

eliminan validaciones/avisos importantes.

## 23.2 Credenciales

```python
API_KEY = "..."
```

es un modelo demasiado simple para producción.

Se requeriría, como mínimo:

- secret management;
- identidad por usuario/servicio;
- rotación;
- scopes/roles;
- separación de entornos.

## 23.3 Autorización

El MCP Server no implementa un modelo robusto que determine qué usuario puede:

- ver una OT;
- crear una OT;
- cambiar estado;
- aprobar workflow.

## 23.4 Working Set

Está solo en memoria y no soporta:

- persistencia;
- sesiones múltiples;
- concurrencia;
- expiración;
- auditoría;
- recuperación tras reinicio.

## 23.5 Reglas de estado

Las transiciones están codificadas localmente y pueden no coincidir con la configuración real de Maximo.

## 23.6 `query_maximo`

Una Tool genérica y potente aumenta superficie de acceso. En producción necesitaría:

- allow-list de Object Structures;
- campos permitidos;
- filtros permitidos;
- límites;
- control de coste/volumen;
- autorización.

## 23.7 Respuestas como strings

La mayoría de Tools devuelve texto ya formateado. Para una solución más robusta convendría preferir resultados estructurados cuando aplique.

## 23.8 Observabilidad

Faltan:

- logs estructurados;
- correlation IDs;
- métricas;
- auditoría de Tools;
- trazabilidad de cambios;
- gestión consistente de errores.

## 23.9 Integración Maximo real

Los endpoints y payloads de escritura deben validarse funcional y técnicamente contra una instancia concreta antes de considerarse utilizables.

---

# 24. Ideas exploradas pero no implementadas

## 24.1 RAG

Se propuso incorporar una base de conocimiento con manuales y procedimientos para complementar los datos estructurados de Maximo.

No fue construido en este laboratorio.

## 24.2 Playwright MCP

Una nota histórica dejó como posible extensión futura un MCP Server con capacidades de navegación web, por ejemplo para consultar portales de soporte.

No se implementó ni se aprobó como arquitectura.

## 24.3 UI final

Se discutieron posibilidades futuras:

- interfaz web;
- Teams/Slack;
- Streamlit/FastAPI;
- Cline/IDE para desarrollo.

No se decidió una UI de producto dentro de este laboratorio.

## 24.4 Automatización autónoma

La idea de llegar a niveles tipo “Delegate” fue exploratoria. No se implementó una autonomía de producción.

---

# 25. Cómo reproducir el aprendizaje hoy

No hay necesidad de repetir esta PoC para darla por cerrada. Esta sección existe para poder reconstruirla si en el futuro queremos practicar otra vez.

## 25.1 Opción A — fidelidad histórica

Objetivo: reproducir el comportamiento del script sin modernizarlo.

```text
1. Crear un entorno Python aislado.
2. Instalar una versión compatible de MCP Python SDK v1.x.
3. Instalar requests y urllib3.
4. Usar mcp/src/maximo_mcp.py.
5. Mantener MODO_SIMULACION = True.
6. Configurar un Host MCP local para lanzar:
      python -u maximo_mcp.py
7. Verificar que descubre las 14 Tools.
8. Ejecutar primero verificar_conexion.
9. Probar consultar_ot / consultar_inventario.
10. Probar Working Set únicamente sobre mocks.
```

## 25.2 Opción B — aprendizaje actualizado

Objetivo: repetir la idea usando el SDK actual.

```text
1. Crear un nuevo servidor MCP v2.
2. Implementar una Tool mínima.
3. Probarla con un cliente/Inspector.
4. Migrar progresivamente capacidades útiles.
5. Mantener mock y real separados.
6. Usar stdio para local o Streamable HTTP para remoto.
7. Añadir pruebas automatizadas.
8. Incorporar seguridad desde el diseño.
```

No deberíamos “modernizar” silenciosamente `maximo_mcp.py`, porque su valor actual es también histórico: documenta exactamente el tipo de PoC que se construyó.

---

# 26. Relación con RAG y el siguiente laboratorio

MCP y RAG resuelven problemas diferentes.

```text
MCP
→ acceso a capacidades / sistemas / acciones

RAG
→ recuperación de conocimiento relevante para enriquecer una respuesta
```

En una futura solución EAM pueden complementarse:

```text
pregunta
   ↓
orquestación de IA
   ├─ MCP → consultar datos de Maximo
   └─ RAG → recuperar manual/procedimiento
   ↓
respuesta fundamentada
   ↓
si hay acción → confirmación humana
```

El siguiente laboratorio podrá estudiar RAG desde cero sin reabrir decisiones MCP ya cerradas. Cuando comience, su documentación y artefactos se crearán bajo la carpeta raíz `rag/` de `ai-eam-learning-lab`. Allí se documentarán y probarán preguntas como **“¿Cómo calibro este equipo según su manual?”** desde la perspectiva de recuperación de conocimiento, mientras MCP seguirá cubriendo acceso a capacidades, sistemas y acciones.

---

# 27. Relación con AI-EAM-MAXIMO

`ai-eam-learning-lab` es un repositorio de aprendizaje.

`ai-driven-eam-copilot` es el producto y su fuente de verdad.

```text
Learning Lab
   ↓
aprendizaje / evidencia
   ↓
🟨 CANDIDATO A INCORPORAR
   ↓ evaluación explícita
AI-EAM-MAXIMO
   ↓
arquitectura / implementación / documentación oficial
```

Nada de este documento convierte automáticamente en requisito del producto:

- el “Tridente”;
- las 14 Tools;
- Cline;
- Claude Desktop;
- el Working Set;
- la configuración local;
- el código histórico.

Lo que sí puede reutilizarse son **principios y aprendizajes** después de verificarlos contra la arquitectura vigente del producto.

---

# 28. Qué conservar en la cabeza

Si solo recuerdas diez ideas después de meses:

1. **MCP conecta una aplicación de IA con capacidades externas mediante un protocolo estándar.**
2. **Host ≠ PC**; el Host es la aplicación/entorno de IA.
3. Un **MCP Server** expone capacidades; nuestra PoC expuso principalmente **Tools**.
4. MCP **no crea autonomía** por sí solo.
5. MCP y **OSLC/REST son complementarios**, no rivales.
6. La PoC funcionó **en simulación**, no contra Maximo real.
7. `maximo_mcp.py` terminó con **14 Tools verificadas en código**.
8. El **Tridente** fue Maximo MCP + Filesystem MCP + GitHub MCP.
9. El **Working Set** probó el patrón `proponer → revisar → confirmar`.
10. La mejor lección metodológica fue **aislar el aprendizaje del protocolo de la disponibilidad del sistema real**.

---

# 29. Estado final y cierre

## ✅ Cerrado / aprobado

- conceptos MCP fundamentales consolidados;
- historia completa recuperada;
- artefactos técnicos principales preservados;
- configuración Claude recuperada y sanitizada;
- código final preservado;
- catálogo de 14 Tools auditado;
- pruebas históricas identificadas;
- contradicciones documentales reconciliadas;
- límites de la PoC explicitados;
- relación MCP ↔ Maximo ↔ RAG comprendida.

## ❌ No cerrado porque nunca formó parte de esta prueba

- conexión Maximo viva;
- hardening productivo;
- autenticación/seguridad empresarial;
- despliegue remoto;
- RAG;
- UI final.

## Próximo paso

➡️ **RAG — nuevo laboratorio independiente dentro de `ai-eam-learning-lab`.**

---

# 30. Registro de fuentes

## 30.1 Artefactos conservados en el Learning Lab

- [`../src/maximo_mcp.py`](../src/maximo_mcp.py)
- [`../src/history/connection_test.py`](../src/history/connection_test.py)
- [`../src/history/maximo_mcp_gemini_v1.py`](../src/history/maximo_mcp_gemini_v1.py)
- [`../config/claude_desktop_config.example.json`](../config/claude_desktop_config.example.json)

## 30.2 Fuentes de transición utilizadas

- `MCP-Claude.zip`
- `notas_sesion.md`
- `IA-Claude_Notas Varias.txt`
- `MCP_HANDOFF_GEMINI_A_CHATGPT.md`
- Bitácora de Proyecto: IA Generativa + MCP para IBM Maximo
- Guía de Configuración Avanzada: Cline + MCP
- memoria técnica generada previamente en Gemini
- presentación conceptual de IA Generativa + IBM Maximo

Estas fuentes sirven como respaldo histórico. El conocimiento vigente que aportaron ya está absorbido en este documento.

## 30.3 Referencias técnicas actuales consultadas

- MCP Python SDK: `https://py.sdk.modelcontextprotocol.io/`
- MCP Python SDK — migración v1 → v2: `https://py.sdk.modelcontextprotocol.io/migration/`
- MCP Python SDK — Host real / stdio: `https://py.sdk.modelcontextprotocol.io/get-started/real-host/`
- MCP Python SDK — transporte stdio / JSON-RPC: `https://py.sdk.modelcontextprotocol.io/client/transports/`
- GitHub MCP Server oficial: `https://github.com/github/github-mcp-server`

> Estas referencias se usan para actualizar conceptos y distinguir el estado tecnológico actual del entorno histórico de la PoC.

---

# 31. Regla de mantenimiento futuro

Este documento debe actualizarse si el laboratorio MCP se reabre.

No crear un nuevo documento narrativo para cada continuación. Actualizar primero esta fuente canónica y mantener:

```text
README → orientación
MCP_LAB_DOCUMENTATION → conocimiento completo
MCP_LAB_HANDOFF → continuidad
src/config → evidencia técnica
```

La documentación histórica cruda puede eliminarse cuando deje de aportar valor de auditoría, siempre que la información útil ya esté incorporada aquí y los artefactos primarios relevantes permanezcan preservados.
