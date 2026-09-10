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
| 2026-09-10 | Consolidación completa con nueva evidencia aportada: cronología 2025–2026, Python 3.14, PATH, rutas Windows Store, primera prueba, operación diaria, Tridente MCP y expansión 4→14 Tools. |
| 2026-09-10 | Se elimina toda dependencia del repositorio temporal de prueba donde apareció `maximo_mcp.py`; dicho repositorio fue eliminado y no es una fuente válida del Learning Lab. |
| 2026-09-10 | Auditoría del código histórico `maximo_mcp.py`: lógica dual y catálogo efectivo de 14 Tools. |
| 2026-09-10 | Creación inicial desde HandOff, bitácora y guía histórica Gemini/Claude/Cline. |

---

# 1. Objetivo original

El laboratorio surgió de una idea profesional concreta: **explorar si un asistente de IA podía reducir fricción operativa en IBM Maximo permitiendo a supervisores interactuar mediante lenguaje natural**.

La visión inicial contemplaba consultas y, posteriormente, registro de datos en tiempo real sin obligar al usuario a navegar continuamente por interfaces complejas.

La documentación histórica llegó a plantear como hipótesis de valor una reducción aproximada del **30 % del tiempo administrativo**. Ese porcentaje debe entenderse como **objetivo/hipótesis inicial**, no como beneficio medido o validado.

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

---

# 2. Cronología real reconstruida

La documentación histórica permite reconstruir tres hitos principales:

| Fecha | Hito |
|---|---|
| **20-04-2025** | v1.0 — pivotaje desde la exploración Google Cloud/Gemini hacia Claude Desktop + MCP local. Se documenta la lógica dual y el primer conjunto reducido de Tools. |
| **01-03-2026** | v1.5 — adopción de VS Code + Cline para acelerar edición, prueba y operación del servidor MCP. |
| **09-09-2026** | v2.0 — expansión al entorno multi-MCP (“Tridente”) y crecimiento documentado de 4 a 14 Tools mediante investigación de repositorios. |
| **10-09-2026** | Traslado y consolidación en `ai-eam-learning-lab`: auditoría de evidencias, corrección de inconsistencias y cierre documental. |

---

# 3. De Gemini/Google Cloud a un laboratorio local

## 3.1 Exploración inicial

Se comenzó explorando Gemini y una posible arquitectura sobre Google Cloud / Vertex AI.

Para una PoC inicial, esta vía introducía demasiada infraestructura antes de validar el concepto: servicios cloud, endpoints, certificados, conectividad y configuración adicional.

## 3.2 Decisión de simplificación

Se decidió mover la ejecución práctica a **Claude Desktop**, aprovechando su capacidad de conectarse con MCP Servers locales.

La arquitectura se simplificó a:

```text
Claude Desktop
      ↓ MCP / stdio
Servidor Python + FastMCP
      ↓
maximo_mcp.py
```

Gemini quedó como apoyo durante parte del razonamiento y desarrollo, mientras Claude Desktop se convirtió en la interfaz práctica de ejecución MCP.

> 📘 Aprendizaje: la principal ventaja del enfoque local no es que “MCP sea automáticamente seguro”, sino que permite validar el mecanismo sin desplegar inicialmente un servicio web propio. Seguridad, credenciales, red y gobierno siguen siendo responsabilidades de la solución.

---

# 4. Entorno utilizado

La evidencia histórica más específica aportada indica:

| Componente | Estado / uso histórico |
|---|---|
| Windows | Sistema operativo local |
| Visual Studio Code | IDE principal |
| Extensión Python de Microsoft | Soporte Python en VS Code |
| **Python 3.14** | Versión indicada en el HandOff histórico como instalada y configurada |
| Claude Desktop | Aplicación utilizada para la primera PoC MCP |
| Claude Desktop Windows Store | Tipo de instalación relevante para localizar su configuración |
| Cline | Extensión utilizada posteriormente dentro de VS Code |
| FastMCP / paquete MCP Python | Framework del MCP Server |
| `requests` | Peticiones HTTP/HTTPS hacia Maximo previstas |
| `urllib3` | Gestión de warnings SSL en la PoC |
| Node.js / `npx` | Necesario posteriormente para servidores MCP adicionales |
| Filesystem MCP | Acceso controlado a directorios locales |
| GitHub MCP | Investigación de repositorios y código |
| IBM Maximo | Sistema objetivo; **sin conexión viva validada** |

> ⚠️ Algunas bitácoras anteriores usan de forma genérica “Python 3.10+”. Para describir la máquina realmente utilizada, el HandOff aporta el dato más específico: **Python 3.14**.

---

# 5. Instalación y preparación — paso a paso

## 5.1 Visual Studio Code

Se instaló VS Code y la extensión oficial de Python.

## 5.2 Python

Se instaló Python 3.14.

La instalación presentó un problema importante: Windows no reconocía inicialmente `python.exe` ni `pip` desde terminal.

### Solución aplicada

Se corrigieron manualmente las Variables de Entorno / `PATH`, incluyendo las rutas necesarias de Python y `Scripts`.

### Verificación

```bash
python --version
```

El objetivo de esta prueba era confirmar que Python quedaba disponible globalmente desde CMD/terminal.

## 5.3 Dependencias Python

La documentación histórica recoge la instalación de las piezas necesarias mediante `pip`. Aparecen dos formulaciones en los documentos históricos (`fastmcp` y `mcp`); el código auditado utiliza:

```python
from mcp.server.fastmcp import FastMCP
```

La instalación documentada de dependencias fue:

```bash
pip install mcp requests urllib3
```

Y el HandOff también registra explícitamente la instalación de FastMCP durante la fase inicial.

## 5.4 Claude Desktop

Se instaló Claude Desktop desde Windows Store.

## 5.5 Node.js / npx

Se incorporó posteriormente para ejecutar servidores MCP adicionales como Filesystem y GitHub.

## 5.6 Cline

Se instaló Cline en VS Code cuando el laboratorio evolucionó hacia un ciclo de desarrollo más operativo.

---

# 6. Primer servidor MCP y primera Tool

El archivo principal fue:

```text
maximo_mcp.py
```

La primera prueba tuvo un propósito deliberadamente simple: **demostrar que Claude Desktop podía descubrir y ejecutar una Tool del servidor local**.

La Tool usada para ese hito fue:

```text
verificar_conexion
```

La secuencia histórica fue:

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

✅ **HECHO histórico suficientemente sustentado:** la prueba de conectividad MCP fue ejecutada con éxito desde Claude Desktop.

---

# 7. Configuración de Claude Desktop

## 7.1 Problema encontrado

Una de las incidencias reales fue utilizar inicialmente una ruta de configuración que no correspondía a la instalación de Claude Desktop usada.

## 7.2 Ruta efectiva documentada para Windows Store

La evidencia histórica identifica:

```text
%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json
```

La forma práctica que permitió localizar la configuración correcta fue desde Claude Desktop:

```text
Settings → Developer → Edit configuration
```

También se había considerado la ruta convencional:

```text
%APPDATA%\Anthropic\Claude\claude_desktop_config.json
```

pero la bitácora registra que para la instalación efectiva desde Windows Store fue necesario trabajar con la ruta empaquetada bajo `Packages`.

## 7.3 JSON del servidor Maximo

La configuración histórica reproducida en las bitácoras fue equivalente a:

```json
{
  "mcpServers": {
    "maximo": {
      "command": "python",
      "args": [
        "-u",
        "C:/RUTA/AL/LABORATORIO/maximo_mcp.py"
      ]
    }
  }
}
```

### Nivel de evidencia

⚠️ **DOCUMENTADO HISTÓRICAMENTE:** el JSON está reproducido en los documentos aportados.

⚠️ **NO AUDITADO COMO ARCHIVO ORIGINAL:** el `claude_desktop_config.json` local real no fue incorporado al Learning Lab ni revisado directamente durante esta reconstrucción.

Se sanitizan aquí rutas personales y cualquier secreto.

---

# 8. Lógica dual: simulación y real

Una decisión central de la PoC fue permitir trabajar sin disponer de un Maximo real.

## 8.1 Modo simulación

```python
MODO_SIMULACION = True
```

Permitía devolver datos ficticios y probar:

- descubrimiento de Tools;
- invocación desde lenguaje natural;
- presentación de resultados;
- flujos de lectura;
- flujos de escritura simulada;
- lógica de estados;
- workflow simulado.

El código auditado contenía mocks de:

- Órdenes de Trabajo;
- inventario;
- activos;
- workflow;
- Object Structures.

## 8.2 Modo real previsto

```python
MODO_SIMULACION = False
```

El script contenía una rama preparada para llamadas HTTP/OSLC REST a Maximo.

Se observaron en el código:

```python
MAXIMO_URL = "https://TU_SERVIDOR/maximo"
API_KEY = "TU_API_KEY_AQUÍ"
```

así como:

- `requests.get(...)` y otras operaciones HTTP;
- cabeceras `apikey`;
- endpoints OSLC/Object Structures;
- timeout de 10 segundos;
- `verify=False`;
- supresión de warnings SSL.

❌ **NO VALIDADO:** no existe evidencia de que esta rama se haya probado contra una instancia real de IBM Maximo.

> ⚠️ `verify=False` y la supresión de warnings SSL son simplificaciones de laboratorio, no patrones recomendables para producción.

---

# 9. Operación diaria con Claude Desktop

La bitácora documenta el siguiente ciclo después de modificar `maximo_mcp.py`:

1. cerrar Claude Desktop completamente, no solo la ventana;
2. salir desde la bandeja del sistema (`Quit Claude`);
3. abrir nuevamente Claude Desktop;
4. ir a `Settings → Developer`;
5. localizar el servidor “Maximo Enterprise”;
6. comprobar que el servidor aparecía en estado activo/Running;
7. ejecutar una consulta funcional de prueba.

Este reinicio era necesario porque Claude cargaba la configuración MCP al arrancar.

---

# 10. Pruebas funcionales documentadas

Tras validar `verificar_conexion`, se probaron consultas relacionadas con mantenimiento.

Ejemplos históricos:

```text
Claude, consulta la información de la orden de trabajo OT-2025
```

```text
¿Cuántos rodamientos tenemos en el almacén CENTRAL?
```

El resultado esperado era que Claude seleccionara la Tool adecuada y devolviera información obtenida del modo simulación.

Se utilizó una convención visual:

```text
🧪 [SIMULACIÓN]
```

para datos mock, y se diseñó:

```text
✅ [REAL]
```

para la rama real prevista.

---

# 11. Evolución: de pocas Tools a 14

La bitácora v2.0 registra explícitamente una evolución de **4 Tools → 14 Tools**.

La ampliación ocurrió después de utilizar GitHub MCP para investigar implementaciones externas relacionadas con Maximo y solicitar mejoras al servidor local.

Una consulta documentada fue aproximadamente:

```text
Busca en GitHub otros servidores MCP de Maximo para ver si alguien ha programado funciones que nosotros no tenemos
```

La bitácora registra que se localizaron, entre otros, repositorios de terceros como:

- `markusvankempen/maximo-mcp-ai-integration-options`;
- `soumyaprasadrana/maximo-mcp-server`.

Posteriormente se solicitó incorporar capacidades útiles que todavía no estuvieran disponibles.

---

# 12. Catálogo final de 14 Tools — verificado contra el código histórico

Durante el traslado al Learning Lab se auditó el código histórico antes de eliminar el repositorio temporal donde se encontraba.

El catálogo observado directamente fue:

| # | Tool | Propósito |
|---:|---|---|
| 1 | `consultar_ot` | Consultar una Orden de Trabajo. |
| 2 | `consultar_inventario` | Consultar stock/ubicación de un artículo. |
| 3 | `listar_transiciones_ot` | Mostrar cambios de estado permitidos. |
| 4 | `cambiar_estado_ot` | Cambiar estado de una OT. |
| 5 | `query_maximo` | Consulta genérica sobre Object Structures. |
| 6 | `consultar_activo` | Consultar un activo. |
| 7 | `listar_object_structures` | Descubrir/Listar Object Structures. |
| 8 | `crear_ot` | Crear una OT. |
| 9 | `ws_editar_ot` | Preparar modificaciones en Working Set. |
| 10 | `ws_confirmar_cambios` | Confirmar cambios preparados. |
| 11 | `ws_cancelar_cambios` | Cancelar cambios preparados. |
| 12 | `obtener_workflow_assignments` | Consultar asignaciones de workflow. |
| 13 | `enviar_workflow_response` | Responder una asignación de workflow. |
| 14 | `verificar_conexion` | Verificar servidor/capacidades. |

✅ **VERIFICADO EN CÓDIGO:** existían exactamente 14 decoradores `@mcp.tool()` correspondientes a estas funciones.

## 12.1 Inconsistencia documental detectada

Una versión de la bitácora histórica lista `consultar_ubicacion` y `generar_reporte_local` como Tools 13 y 14.

Sin embargo, el código histórico auditado antes de eliminar el repositorio temporal no contenía esas dos funciones dentro del catálogo final observado; en su lugar estaban presentes `listar_transiciones_ot`, `cambiar_estado_ot` y el conjunto mostrado arriba.

Por tanto:

> ✅ Para describir **qué estuvo implementado realmente en el script auditado**, prevalece la tabla verificada contra código.
>
> 📘 La tabla diferente se conserva únicamente como evidencia de cómo evolucionó o se documentó el experimento.

---

# 13. Working Set y Human-in-the-Loop experimental

El servidor exploró un patrón de confirmación antes de ejecutar cambios:

```text
ws_editar_ot
    ↓
Working Set / preview
    ↓
┌─────────────────┐
↓                 ↓
confirmar       cancelar
↓                 ↓
ws_confirmar    ws_cancelar
_cambios        _cambios
```

El Working Set era memoria temporal dentro del proceso Python, **no una capacidad nativa de IBM Maximo**.

El aprendizaje relevante fue el patrón:

```text
proponer → revisar → confirmar
```

que anticipa una forma de Human-in-the-Loop especialmente importante para operaciones EAM con impacto real.

---

# 14. Evolución a VS Code + Cline

El laboratorio migró posteriormente de Claude Desktop como centro de desarrollo hacia **VS Code + Cline**.

El objetivo fue reducir el ciclo manual:

```text
solicitar cambio
    ↓
IA analiza / modifica código
    ↓
usuario revisa diff
    ↓
ejecución / prueba
    ↓
refresco del MCP Server
```

La documentación histórica describe a Cline como “Agente de Acción”. Conceptualmente, para esta documentación preferimos una formulación más precisa:

> Cline aportaba capacidades agénticas/orquestadas —edición de archivos, terminal y uso de Tools— sobre el entorno de desarrollo. MCP por sí solo no convierte a un LLM en agente.

---

# 15. El “Tridente MCP”

La fase avanzada combinó tres servidores:

```text
VS Code + Cline
   ├─ Maximo MCP
   ├─ Filesystem MCP
   └─ GitHub MCP
```

## 15.1 Maximo MCP

Servidor Python propio con lógica EAM/Maximo.

## 15.2 Filesystem MCP

Servidor basado en Node/npx para acceder únicamente a directorios locales autorizados.

## 15.3 GitHub MCP

Servidor utilizado históricamente para investigar repositorios y código.

La configuración histórica reproducida en los documentos es equivalente a:

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

> ⚠️ Esta configuración es histórica. No se adopta como recomendación actual y nunca deben publicarse PATs o secretos en el repositorio.

---

# 16. Prueba destacada con GitHub MCP

La bitácora registra una prueba especialmente útil:

1. tener GitHub MCP activo;
2. pedir a la IA investigar otros MCP Servers relacionados con Maximo;
3. identificar funciones que no existían localmente;
4. solicitar que se incorporaran capacidades útiles;
5. actualizar el servidor desde 4 hasta 14 Tools.

🧪 **DOCUMENTADO COMO PRUEBA SUPERADA:** investigación de repositorios mediante GitHub MCP y posterior ampliación del script local.

El código final auditado confirma que el servidor terminó conteniendo 14 Tools, aunque no permite atribuir automáticamente cada función a un repositorio externo concreto.

---

# 17. Hot reload / refresh

La documentación histórica describe que el paso a Cline permitió refrescar/reiniciar el servidor MCP con mucha menos fricción que el ciclo completo de Claude Desktop.

Esto debe entenderse como **comportamiento documentado del entorno usado entonces**, no como una garantía sobre versiones actuales de Cline o MCP.

---

# 18. Qué quedó realmente probado

## 🧪 PROBADO / suficientemente sustentado

- Python funcionando tras corregir PATH.
- MCP Server local en Python/FastMCP.
- Tool `verificar_conexion` ejecutada desde Claude Desktop.
- Uso de modo simulación.
- Consultas EAM simuladas desde lenguaje natural.
- Evolución del servidor a 14 Tools.
- Configuración histórica multi-MCP con Maximo + Filesystem + GitHub.
- Uso histórico de GitHub MCP para investigar implementaciones externas.
- Trabajo posterior con VS Code + Cline.

## ✅ VERIFICADO DIRECTAMENTE DURANTE LA RECONSTRUCCIÓN

- estructura del código histórico `maximo_mcp.py`;
- uso de FastMCP;
- `MODO_SIMULACION`;
- mocks de OT, inventario, activos, workflow y Object Structures;
- lógica OSLC/REST prevista;
- exactamente 14 Tools en el artefacto auditado;
- Working Set en memoria;
- `verify=False` y timeout de 10 segundos.

## ⚠️ DOCUMENTADO, NO AUDITADO COMO ARTEFACTO ORIGINAL

- `claude_desktop_config.json` real;
- `cline_mcp_settings.json` real;
- archivos locales de logs;
- comportamiento exacto del refresh/hot reload en la versión usada.

## ❌ NO VALIDADO

- conexión viva con IBM Maximo;
- lectura real contra Maximo;
- escritura real contra Maximo;
- workflow real;
- seguridad productiva;
- reducción real del 30 % del trabajo administrativo;
- RAG.

---

# 19. Problemas encontrados y soluciones

## 19.1 Python/PIP no reconocidos

**Problema:** terminal de Windows no encontraba Python/PIP.

**Solución:** corrección manual del PATH de Windows.

## 19.2 Archivo de configuración Claude equivocado

**Problema:** se editó inicialmente una ubicación que Claude no estaba utilizando.

**Solución:** `Settings → Developer → Edit configuration`, identificando la ruta de la instalación Windows Store bajo `%LOCALAPPDATA%\Packages\...`.

## 19.3 No disponer de Maximo real

**Problema:** la infraestructura objetivo no estaba accesible.

**Solución:** diseño dual con mocks y `MODO_SIMULACION`.

## 19.4 Ciclo lento de cambios en Claude Desktop

**Problema:** reiniciar completamente Claude para recargar el servidor.

**Evolución:** traslado a VS Code + Cline para reducir fricción de desarrollo.

---

# 20. Aspectos que no deben copiarse a producción

La PoC fue útil para aprender, pero varias decisiones son deliberadamente simplificadas:

- `verify=False`;
- warnings SSL deshabilitados;
- credencial modelada como variable directa;
- Working Set solo en memoria;
- reglas de transición de estados codificadas localmente;
- respuestas principalmente como strings;
- Tool genérica `query_maximo` potencialmente demasiado amplia;
- ausencia de control de autorización productivo;
- ausencia de observabilidad/auditoría robusta;
- ausencia de integración real verificada.

---

# 21. Conceptos MCP corregidos y consolidados

Durante la reconstrucción se corrigieron algunas explicaciones históricas para alinearlas con un modelo mental más preciso.

## Host

La aplicación/entorno de IA que coordina conexiones MCP. **No es simplemente el PC físico.**

## Client

Componente/conexión que habla el protocolo con un MCP Server.

## Server

Proceso que expone capacidades MCP.

## Tool

Capacidad invocable por el modelo/aplicación.

## MCP no es solo Tools

MCP también contempla otras primitivas, como **Resources** y **Prompts**.

## MCP no crea autonomía por sí mismo

La lógica del Host/agente decide cuándo y cómo utilizar capacidades. MCP estandariza la interfaz de acceso.

---

# 22. Aprendizajes EAM / IBM Maximo

📘 **Simular primero fue una buena decisión.** Separó el aprendizaje de MCP de la disponibilidad de Maximo.

📘 **Las Tools pueden hablar lenguaje EAM.** `consultar_ot`, `crear_ot`, workflow o inventario expresan capacidades de negocio, no simplemente endpoints HTTP.

📘 **OSLC/REST y MCP no son alternativas excluyentes.** MCP puede ser la frontera consumida por la IA mientras OSLC/REST sigue siendo la integración subyacente.

📘 **Las escrituras necesitan control.** El experimento Working Set mostró tempranamente el valor de preview + confirmación humana.

📘 **Combinar servidores especializados es útil.** Maximo, filesystem y GitHub aportaron capacidades diferentes al mismo entorno.

---

# 23. Qué se conserva después de eliminar el repositorio temporal

El repositorio temporal de prueba que contenía una copia histórica de `maximo_mcp.py` fue eliminado intencionalmente y **no es una fuente válida**.

El Learning Lab conserva el conocimiento necesario para recordar:

- arquitectura;
- instalaciones;
- configuración reconstruida;
- flujo de prueba;
- catálogo auditado de 14 Tools;
- problemas y soluciones;
- límites técnicos;
- nivel de evidencia.

La documentación ya no debe depender de aquel repositorio.

---

# 24. Cómo reproducir conceptualmente la PoC hoy

Este procedimiento reproduce **la idea histórica**, no garantiza compatibilidad exacta con versiones actuales:

```text
1. Instalar Python
2. Instalar el SDK MCP/FastMCP vigente
3. Crear un MCP Server mínimo en Python
4. Añadir una Tool sencilla
5. Configurar un MCP Host compatible
6. Conectar mediante stdio
7. Confirmar que el Host descubre la Tool
8. Ejecutarla desde lenguaje natural
9. Añadir datos EAM simulados
10. Incorporar capacidades progresivamente
11. Separar claramente lectura de escritura
12. Añadir confirmación humana para acciones con impacto
```

Si se quisiera repetir exactamente el laboratorio histórico con Claude/Cline, antes habría que verificar la documentación vigente de esos productos y de los MCP Servers utilizados.

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

El valor para AI-EAM-MAXIMO está en los **patrones aprendidos**, no en copiar el script histórico.

---

# 26. Fuentes históricas usadas en la reconstrucción

- `MCP_HANDOFF_GEMINI_A_CHATGPT.md` — HandOff del trabajo anterior.
- `Bitácora de Proyecto: IA Generativa + MCP para IBM Maximo` — evolución, instalaciones, configuración, pruebas y ampliación 4→14 Tools.
- `Guía de Configuración Avanzada: Cline + MCP (Maximo, Filesystem y GitHub)` — configuración y operación del entorno avanzado.
- Código histórico `maximo_mcp.py` — auditado durante el traslado al Learning Lab antes de eliminar el repositorio temporal de prueba que lo contenía.

> 🔐 Ninguna ruta personal, token, PAT, API key o URL corporativa debe persistirse en este repositorio público.

---

# 27. Resultado final del laboratorio MCP

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
