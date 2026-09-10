# 🕰️ Laboratorio histórico — MCP + IBM Maximo

> ⚠️ **HISTÓRICO — material de referencia.** Este documento reconstruye el laboratorio realizado con Gemini, Claude Desktop, VS Code/Cline y un servidor MCP propio orientado a IBM Maximo. No constituye arquitectura vigente de AI-EAM-MAXIMO.
>
> 🎯 **Objetivo del documento:** permitir que dentro de meses pueda entenderse qué se quiso probar, qué se instaló, cómo se configuró, qué se construyó, qué se probó, qué funcionó, qué no se validó y qué se aprendió, sin depender del chat original.
>
> 📍 **Estado:** ✅ CERRADO para el alcance histórico de aprendizaje.
> 🗓️ **Actualizado:** 2026-09-10

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Se incorpora como evidencia primaria una copia del `claude_desktop_config.json` obtenida desde Claude Desktop → Configuración → Desarrollador → Editar configuración; se documenta y sanitiza su contenido MCP. |
| 2026-09-10 | Consolidación completa con cronología 2025–2026, Python 3.14, PATH, Windows Store, primera prueba, operación diaria, Tridente MCP y expansión 4→14 Tools. |
| 2026-09-10 | Se elimina toda dependencia del repositorio temporal de prueba que contenía `maximo_mcp.py`; dicho repositorio fue eliminado y no es una fuente válida del Learning Lab. |
| 2026-09-10 | Auditoría del código histórico `maximo_mcp.py`: lógica dual y catálogo efectivo de 14 Tools. |
| 2026-09-10 | Creación inicial desde HandOff, bitácora y guía histórica Gemini/Claude/Cline. |

---

# 1. Objetivo original

El laboratorio surgió de una idea profesional concreta: **explorar si un asistente de IA podía reducir fricción operativa en IBM Maximo permitiendo a supervisores interactuar mediante lenguaje natural**.

La pregunta técnica central fue:

> ¿Puede una aplicación de IA descubrir e invocar capacidades externas mediante MCP y utilizar esas capacidades para encapsular operaciones EAM/IBM Maximo?

Modelo mental:

```text
Usuario
   ↓ lenguaje natural
Aplicación de IA / MCP Host
   ↓
MCP Client
   ↓ MCP
MCP Server
   ↓ Tool
Lógica Python
   ↓
Datos simulados
   o
OSLC / REST previsto → IBM Maximo
```

No se buscaba una solución productiva. El objetivo era **aprender haciendo** y validar el mecanismo MCP sin depender inicialmente de una instancia real de Maximo.

---

# 2. Cronología reconstruida

| Fecha | Hito |
|---|---|
| **20-04-2025** | v1.0 — pivotaje desde exploración Google Cloud/Gemini hacia Claude Desktop + MCP local. |
| **01-03-2026** | v1.5 — adopción de VS Code + Cline para acelerar edición, prueba y operación. |
| **09-09-2026** | v2.0 — entorno multi-MCP (“Tridente”) y crecimiento documentado de 4 a 14 Tools. |
| **10-09-2026** | Traslado a `ai-eam-learning-lab`: auditoría de evidencias, corrección de inconsistencias y cierre documental. |

---

# 3. De Gemini/Google Cloud a Claude Desktop

La primera aproximación contempló Gemini y Google Cloud / Vertex AI. Para una PoC inicial, esa vía introducía demasiada infraestructura antes de validar el concepto: endpoints, servicios cloud, conectividad y configuración adicional.

Se simplificó el laboratorio usando **Claude Desktop** como MCP Host y un servidor Python local:

```text
Claude Desktop
      ↓ MCP / stdio
Python + FastMCP
      ↓
maximo_mcp.py
```

Gemini siguió siendo apoyo de razonamiento/desarrollo durante parte del trabajo, pero Claude Desktop se convirtió en la interfaz práctica de ejecución MCP.

---

# 4. Entorno utilizado

| Componente | Uso histórico |
|---|---|
| Windows | Sistema operativo local |
| Visual Studio Code | IDE principal |
| Extensión Python de Microsoft | Soporte Python |
| **Python 3.14** | Runtime documentado en el HandOff histórico |
| Claude Desktop | Primer MCP Host utilizado |
| Claude Desktop Windows Store | Tipo de instalación relevante para su ruta de configuración |
| Cline | Entorno posterior dentro de VS Code |
| FastMCP / MCP Python SDK | Implementación del MCP Server |
| `requests` / `urllib3` | Acceso HTTP y manejo SSL en la PoC |
| Node.js / `npx` | Ejecución de servidores MCP adicionales |
| Filesystem MCP | Acceso controlado a carpetas locales |
| GitHub MCP | Investigación de repositorios/código |
| IBM Maximo | Sistema objetivo; **sin conexión viva validada** |

---

# 5. Instalación y preparación

## 5.1 VS Code

Se instaló Visual Studio Code y la extensión oficial de Python.

## 5.2 Python

Se instaló Python 3.14. Durante la preparación Windows no reconocía inicialmente `python.exe` ni `pip` desde terminal.

### Solución

Se corrigieron las Variables de Entorno / `PATH` hasta obtener:

```bash
python --version
```

## 5.3 Dependencias Python

La documentación histórica recoge:

```bash
pip install mcp requests urllib3
```

El código auditado utilizaba:

```python
from mcp.server.fastmcp import FastMCP
```

## 5.4 Claude Desktop

Se instaló Claude Desktop desde Windows Store.

## 5.5 Node.js / npx

Se incorporó posteriormente para ejecutar Filesystem MCP y GitHub MCP.

## 5.6 Cline

Se instaló Cline en VS Code para reducir el ciclo manual de editar → reiniciar → probar.

---

# 6. Primer servidor MCP y primera Tool

El artefacto principal fue:

```text
maximo_mcp.py
```

La primera Tool utilizada para validar el mecanismo fue:

```text
verificar_conexion
```

Secuencia:

```text
1. Crear maximo_mcp.py
2. Inicializar FastMCP
3. Exponer verificar_conexion con @mcp.tool()
4. Configurar Claude Desktop para lanzar el script
5. Reiniciar Claude Desktop
6. Confirmar servidor MCP activo
7. Solicitar la ejecución desde el chat
8. Recibir la respuesta del servidor
```

🧪 **PROBADO HISTÓRICAMENTE:** Claude Desktop ejecutó una Tool del servidor MCP local y devolvió su resultado al usuario.

---

# 7. Configuración REAL de Claude Desktop

Esta sección quedó reforzada con **evidencia primaria aportada el 10-09-2026**: una copia del archivo de configuración obtenida directamente desde la instalación local de Claude Desktop.

## 7.1 Cómo se obtuvo el archivo

Ruta local indicada por el usuario:

```text
C:\Users\<USUARIO>\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json
```

La forma utilizada para llegar al archivo fue:

```text
Claude Desktop
→ Configuración
→ Desarrollador
→ Editar configuración
```

✅ **VERIFICADO COMO ARTEFACTO APORTADO:** ya no dependemos únicamente de una reproducción en la bitácora; existe una copia del archivo local usado por Claude Desktop.

> 🔐 El repositorio es público. Por eso aquí se sanitizan nombre de usuario, rutas personales, identificadores de cuenta/dispositivo y cualquier secreto.

## 7.2 Servidores MCP presentes en el archivo

El archivo confirma tres servidores MCP:

```text
maximo
filesystem
github
```

Es decir, confirma la configuración histórica denominada informalmente **“Tridente MCP”**.

## 7.3 Configuración sanitizada equivalente

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

### Observaciones verificadas

- `maximo` **no utilizaba simplemente `python`**; la copia aportada apunta a la ruta absoluta de `python.exe`.
- El script se lanzaba con `-u` seguido de la ruta local a `maximo_mcp.py`.
- `filesystem` autorizaba **dos directorios locales**.
- `github` se ejecutaba mediante `npx -y @modelcontextprotocol/server-github`.
- El token GitHub se suministraba mediante la variable de entorno `GITHUB_PERSONAL_ACCESS_TOKEN` dentro de la configuración.
- El archivo contiene además preferencias internas de Claude Desktop no relacionadas con MCP; no se conservan aquí porque no aportan al aprendizaje y pueden contener identificadores locales.

## 7.4 Nota sobre el Personal Access Token de GitHub

Históricamente, el GitHub MCP necesitaba un **Personal Access Token (PAT)**. El procedimiento general en GitHub es:

```text
GitHub
→ Settings
→ Developer settings
→ Personal access tokens
→ crear un token
→ seleccionar únicamente los permisos necesarios
→ copiarlo una sola vez
```

Para una configuración actual se debe **preferir un token fine-grained cuando sea compatible** y comprobar en la documentación vigente del servidor GitHub MCP qué permisos concretos necesita.

Reglas de seguridad:

- no guardar el token en Git;
- no incluirlo en documentación pública;
- conceder solo los permisos mínimos;
- revocarlo si deja de utilizarse o se sospecha exposición;
- usar `<SECRET>` o variables/secret stores en ejemplos.

> ⚠️ El archivo aportado al chat contiene la palabra `SECRETO` como marcador y una nota explicativa añadida por el usuario; por tanto, esa copia no debe tratarse como JSON listo para ejecutar byte por byte. Para documentación se conserva únicamente la estructura MCP válida y sanitizada.

---

# 8. Lógica dual: simulación y real

## 8.1 Modo simulación

```python
MODO_SIMULACION = True
```

Permitía trabajar sin Maximo real y probar descubrimiento de Tools, lenguaje natural, consultas, escrituras simuladas, lógica de estados y workflow.

El código histórico contenía mocks de:

- Órdenes de Trabajo;
- inventario;
- activos;
- workflow;
- Object Structures.

## 8.2 Modo real previsto

```python
MODO_SIMULACION = False
```

La rama real estaba preparada para OSLC/REST mediante `requests`, `apikey`, endpoints de Object Structures, timeout y conexión HTTPS.

❌ **NO VALIDADO:** no existe evidencia de conexión contra una instancia viva de IBM Maximo.

> ⚠️ `verify=False` y la supresión de warnings SSL eran simplificaciones de PoC, no patrones de producción.

---

# 9. Operación con Claude Desktop

Después de modificar `maximo_mcp.py`, el ciclo documentado era:

1. cerrar Claude Desktop completamente (`Quit Claude`);
2. volver a abrirlo;
3. ir a `Settings → Developer`;
4. comprobar el servidor MCP activo;
5. ejecutar una consulta de prueba.

---

# 10. Pruebas funcionales

Tras `verificar_conexion`, se probaron consultas EAM simuladas, por ejemplo:

```text
Consulta la información de la orden de trabajo OT-2025
```

```text
¿Cuántos rodamientos tenemos en el almacén CENTRAL?
```

La convención utilizada distinguía:

```text
🧪 [SIMULACIÓN]
```

de la rama prevista:

```text
✅ [REAL]
```

---

# 11. Evolución de 4 a 14 Tools

La bitácora v2.0 registra una evolución de **4 Tools → 14 Tools** después de utilizar GitHub MCP para investigar implementaciones externas y ampliar el servidor local.

Consulta documentada aproximada:

```text
Busca en GitHub otros servidores MCP de Maximo para ver si alguien ha programado funciones que nosotros no tenemos
```

---

# 12. Catálogo final auditado de 14 Tools

Antes de eliminar el repositorio temporal de prueba donde apareció el script, se auditó `maximo_mcp.py`. El catálogo observado directamente fue:

| # | Tool | Propósito |
|---:|---|---|
| 1 | `consultar_ot` | Consultar una Orden de Trabajo. |
| 2 | `consultar_inventario` | Consultar stock/ubicación de un artículo. |
| 3 | `listar_transiciones_ot` | Mostrar cambios de estado permitidos. |
| 4 | `cambiar_estado_ot` | Cambiar estado de una OT. |
| 5 | `query_maximo` | Consulta genérica sobre Object Structures. |
| 6 | `consultar_activo` | Consultar un activo. |
| 7 | `listar_object_structures` | Descubrir/listar Object Structures. |
| 8 | `crear_ot` | Crear una Orden de Trabajo. |
| 9 | `ws_editar_ot` | Preparar modificaciones en Working Set. |
| 10 | `ws_confirmar_cambios` | Confirmar cambios preparados. |
| 11 | `ws_cancelar_cambios` | Cancelar cambios preparados. |
| 12 | `obtener_workflow_assignments` | Consultar asignaciones de workflow. |
| 13 | `enviar_workflow_response` | Responder una asignación de workflow. |
| 14 | `verificar_conexion` | Verificar servidor/capacidades. |

✅ **VERIFICADO EN CÓDIGO:** existían exactamente 14 decoradores `@mcp.tool()` correspondientes a estas funciones.

Una bitácora histórica llegó a listar nombres diferentes. Para describir lo implementado realmente prevalece el catálogo auditado contra código.

---

# 13. Working Set / Human-in-the-Loop experimental

El servidor exploró un patrón:

```text
ws_editar_ot
    ↓
preview / Working Set
    ↓
confirmar o cancelar
```

El Working Set era memoria temporal del proceso Python, no una función nativa de Maximo.

Aprendizaje:

```text
proponer → revisar → confirmar
```

---

# 14. Evolución a VS Code + Cline

Cline permitió acortar el ciclo:

```text
solicitar cambio
→ IA analiza/modifica código
→ usuario revisa diff
→ ejecutar/probar
→ refrescar MCP Server
```

MCP aportaba el protocolo de capacidades; la conducta agéntica/orquestada provenía del Host/entorno.

---

# 15. “Tridente MCP”

La configuración avanzada quedó confirmada tanto documentalmente como por la copia del archivo de Claude Desktop:

```text
Claude Desktop / Cline
   ├─ Maximo MCP
   ├─ Filesystem MCP
   └─ GitHub MCP
```

“Tridente MCP” es una denominación informal del laboratorio, no un término del estándar MCP.

---

# 16. Prueba destacada con GitHub MCP

La bitácora registra:

1. activar GitHub MCP;
2. pedir a la IA investigar MCP Servers relacionados con Maximo;
3. identificar capacidades interesantes;
4. solicitar mejoras del servidor local;
5. evolucionar hasta 14 Tools.

El código final auditado confirma las 14 Tools, aunque no permite atribuir cada función a un repositorio externo concreto.

---

# 17. Qué quedó realmente probado

## 🧪 PROBADO / suficientemente sustentado

- Python funcionando tras corregir PATH.
- MCP Server local en Python/FastMCP.
- `verificar_conexion` ejecutada desde Claude Desktop.
- modo simulación.
- consultas EAM simuladas desde lenguaje natural.
- evolución a 14 Tools.
- entorno multi-MCP Maximo + Filesystem + GitHub.
- uso histórico de GitHub MCP para investigar código.
- trabajo posterior con VS Code + Cline.

## ✅ VERIFICADO DIRECTAMENTE DURANTE LA RECONSTRUCCIÓN

- estructura del `maximo_mcp.py` histórico antes de eliminar el repo temporal;
- 14 Tools reales;
- `MODO_SIMULACION` y mocks;
- Working Set en memoria;
- lógica OSLC/REST prevista;
- **copia del `claude_desktop_config.json` real**, incluida la ruta absoluta de Python y los tres servidores MCP.

## ⚠️ DOCUMENTADO, NO AUDITADO COMO ARTEFACTO ORIGINAL

- `cline_mcp_settings.json` real;
- logs locales;
- comportamiento exacto de refresh/hot reload de la versión histórica de Cline.

## ❌ NO VALIDADO

- conexión viva con IBM Maximo;
- lectura real contra Maximo;
- escritura real contra Maximo;
- workflow real;
- seguridad productiva;
- beneficio cuantitativo de negocio;
- RAG.

---

# 18. Problemas encontrados y soluciones

| Problema | Solución / evolución |
|---|---|
| Python/PIP no reconocidos | Corrección del PATH de Windows. |
| Ruta incorrecta de configuración Claude | Usar `Configuración → Desarrollador → Editar configuración`. |
| No disponer de Maximo real | `MODO_SIMULACION` + mocks. |
| Ciclo lento de reinicio en Claude Desktop | Evolución a VS Code + Cline. |

---

# 19. Aspectos que NO deben copiarse a producción

- `verify=False`;
- warnings SSL deshabilitados;
- secretos dentro de archivos de configuración versionados;
- Working Set solo en memoria;
- transiciones de estado codificadas localmente;
- respuestas principalmente como strings;
- Tool genérica demasiado amplia;
- ausencia de autorización/auditoría productivas;
- ausencia de integración real verificada.

---

# 20. Modelo mental MCP consolidado

```text
HOST
aplicación de IA que coordina
    ↓
CLIENT
conexión MCP con un Server
    ↓
SERVER
expone capacidades
    ↓
TOOLS / RESOURCES / PROMPTS
```

MCP **no crea autonomía por sí mismo**. Estandariza cómo el Host accede a capacidades externas.

---

# 21. Aprendizajes EAM / IBM Maximo

📘 Simular primero separó el aprendizaje de MCP de la disponibilidad de Maximo.

📘 Las Tools pueden expresar lenguaje EAM (`consultar_ot`, `crear_ot`, workflow) en lugar de exponer únicamente HTTP genérico.

📘 MCP y OSLC/REST no son excluyentes: MCP puede ser la frontera consumida por la IA y OSLC/REST la integración subyacente.

📘 Las acciones de escritura requieren controles; el Working Set anticipó un patrón Human-in-the-Loop.

📘 Varios servidores MCP especializados pueden coexistir en un mismo Host.

---

# 22. Fuentes y niveles de evidencia

## Evidencia primaria recuperada

- copia del `claude_desktop_config.json` local obtenida desde Claude Desktop → Configuración → Desarrollador → Editar configuración;
- código histórico `maximo_mcp.py`, auditado antes de eliminar el repositorio temporal de prueba donde estaba almacenado.

## Documentación histórica

- `MCP_HANDOFF_GEMINI_A_CHATGPT.md`;
- `Bitácora de Proyecto: IA Generativa + MCP para IBM Maximo`;
- `Guía de Configuración Avanzada: Cline + MCP (Maximo, Filesystem y GitHub)`;
- material complementario aportado durante la reconstrucción.

> 🔐 Los artefactos públicos deben estar sanitizados. El Learning Lab no almacena credenciales, PATs, API keys, rutas personales completas ni identificadores de cuenta/dispositivo.

---

# 23. Después de eliminar el repositorio temporal

El repositorio temporal que contenía `maximo_mcp.py` fue eliminado intencionalmente y **no es una fuente válida del proyecto**.

La memoria persistente del laboratorio queda en `ai-eam-learning-lab` mediante:

- este documento canónico;
- la configuración MCP sanitizada;
- README y HandOff;
- artefactos históricos documentados con su nivel de evidencia.

---

# 24. Cómo reproducir conceptualmente la PoC hoy

```text
1. Instalar Python
2. Instalar el SDK MCP/FastMCP vigente
3. Crear un MCP Server mínimo
4. Añadir una Tool
5. Configurar un MCP Host compatible
6. Conectar mediante stdio
7. Confirmar descubrimiento de la Tool
8. Ejecutarla desde lenguaje natural
9. Añadir datos EAM simulados
10. Incorporar capacidades progresivamente
11. Separar lectura de escritura
12. Añadir confirmación humana para acciones de impacto
```

Para repetir exactamente la configuración histórica habría que verificar antes la documentación vigente de Claude Desktop, Cline y los servidores MCP usados.

---

# 25. Relación con AI-EAM-MAXIMO

```text
AI-EAM Learning Lab
       ↓
aprender / experimentar
       ↓
🟨 CANDIDATO A INCORPORAR
       ↓ decisión explícita
AI-EAM-MAXIMO
```

Nada de esta PoC se convierte automáticamente en arquitectura o implementación del producto.

---

# 26. Resultado final

El objetivo de aprendizaje quedó cumplido para esta etapa:

```text
ENTENDER MCP
    +
CONSTRUIR UN MCP SERVER
    +
EJECUTAR TOOLS DESDE IA
    +
SIMULAR CAPACIDADES IBM MAXIMO
    +
EXPLORAR MULTI-MCP
    +
DOCUMENTAR QUÉ FUE REAL Y QUÉ NO
```

✅ **MCP queda cerrado como laboratorio histórico de aprendizaje.**

➡️ El siguiente laboratorio independiente será **RAG (Retrieval-Augmented Generation)**.
