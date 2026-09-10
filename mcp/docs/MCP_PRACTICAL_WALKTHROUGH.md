# 🔌 MCP + IBM Maximo — Recorrido práctico paso a paso

> 🎯 **Objetivo:** dejar documentado, de forma reproducible y comprensible meses después, qué se hizo en el laboratorio MCP, cómo se configuró, qué se probó y qué quedó pendiente.
> 📍 **Estado:** ✅ DOCUMENTADO — reconstrucción basada en la evidencia histórica disponible y en el código real localizado.
> 🗓️ **Actualizado:** 2026-09-10

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Creación del recorrido práctico paso a paso del laboratorio MCP + IBM Maximo. |

---

# 1. Objetivo del laboratorio

El laboratorio nació para comprobar, de forma práctica, si una aplicación de IA podía usar capacidades externas relacionadas con IBM Maximo mediante **MCP (Model Context Protocol)**.

La idea era permitir interacciones como:

```text
Usuario
  ↓ lenguaje natural
Aplicación de IA
  ↓ MCP
Servidor MCP local
  ↓ tool
Código Python
  ↓
Datos simulados / futura API Maximo
```

El objetivo principal no era construir todavía una integración productiva, sino **entender MCP haciendo una PoC real**.

---

# 2. Evolución tecnológica

## 2.1 Primera exploración: Gemini / Google Cloud

Inicialmente se estudió una solución con Gemini y Google Cloud / Vertex AI.

La documentación histórica refleja que para una PoC local este camino se percibió como más complejo de lo necesario, porque implicaba infraestructura cloud, endpoints y configuración adicional.

## 2.2 Cambio a Claude Desktop

Se decidió utilizar **Claude Desktop**, ya que permitía trabajar con servidores MCP locales directamente desde el equipo.

La arquitectura pasó a ser:

```text
Claude Desktop
      ↓ MCP
maximo_mcp.py
      ↓
funciones Python
```

## 2.3 Evolución a VS Code + Cline

Más adelante se trasladó el trabajo a **Visual Studio Code + Cline** para acelerar el ciclo de desarrollo.

Cline permitía:

- abrir y editar archivos;
- mostrar diffs de cambios;
- ejecutar comandos de terminal;
- trabajar con varios servidores MCP;
- refrescar/reiniciar servidores desde el entorno de desarrollo.

## 2.4 Configuración de varios servidores MCP

El laboratorio terminó trabajando con tres servidores:

```text
VS Code + Cline
   ├─ Maximo MCP
   ├─ Filesystem MCP
   └─ GitHub MCP
```

Durante el trabajo se llamó informalmente a esta configuración **“Tridente MCP”**.

---

# 3. Software y componentes instalados

Los componentes utilizados históricamente fueron:

| Componente | Función |
|---|---|
| Visual Studio Code | Editor / IDE |
| Extensión Python de Microsoft | Soporte Python en VS Code |
| Python 3.10+ | Runtime del servidor MCP |
| Claude Desktop | Cliente/host utilizado inicialmente |
| Cline | Entorno/agente posterior dentro de VS Code |
| MCP Python SDK / FastMCP | Framework del servidor MCP |
| `requests` | Llamadas HTTP hacia Maximo |
| `urllib3` | Gestión de SSL/warnings en el laboratorio |
| Node.js / `npx` | Ejecución de servidores MCP adicionales |
| Filesystem MCP | Acceso a archivos locales |
| GitHub MCP | Acceso a repositorios GitHub |

Dependencias Python instaladas:

```bash
pip install mcp requests urllib3
```

Validación básica de Python:

```bash
python --version
```

Durante el laboratorio fue necesario corregir el `PATH` de Windows para que Python y `pip` pudieran ejecutarse desde terminal.

---

# 4. Configuración inicial de Claude Desktop

Claude Desktop necesitaba saber cómo arrancar el servidor MCP local.

El archivo de configuración utilizado conceptualmente fue:

```text
claude_desktop_config.json
```

Ejemplo sanitizado:

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

La documentación histórica registra dos ubicaciones posibles según el tipo de instalación de Claude Desktop. La ruta efectiva se terminó identificando desde **Settings > Developer > Edit configuration**.

> 🔐 En este repositorio no se documentan rutas personales reales ni secretos.

---

# 5. Creación del servidor MCP local

El artefacto principal fue:

```text
maximo_mcp.py
```

El código real histórico fue localizado posteriormente en:

```text
jperdomo12/Maximo-IA-Project/maximo_mcp.py
```

Elementos principales confirmados en el código:

```python
from mcp.server.fastmcp import FastMCP

MODO_SIMULACION = True
mcp = FastMCP("Maximo Enterprise")
```

Las capacidades eran expuestas con:

```python
@mcp.tool()
```

Y el servidor arrancaba con:

```python
if __name__ == "__main__":
    mcp.run()
```

---

# 6. Modo simulación vs modo real

Una decisión importante del laboratorio fue trabajar con una lógica dual.

## 6.1 Modo simulación

```python
MODO_SIMULACION = True
```

En este modo:

- no se necesitaba IBM Maximo;
- se devolvían datos ficticios;
- se podían probar descubrimiento e invocación de tools;
- se reducía el riesgo durante el aprendizaje.

El código incluía datos mock de:

- órdenes de trabajo;
- inventario;
- activos;
- workflow;
- Object Structures.

## 6.2 Modo real previsto

```python
MODO_SIMULACION = False
```

En este modo el script intentaba usar HTTP/OSLC contra Maximo mediante `requests`.

Se confirmaron en el código:

- `MAXIMO_URL` como placeholder;
- `API_KEY` como placeholder;
- `verify=False`;
- timeout de 10 segundos;
- construcción de URLs OSLC/Object Structures.

> ⚠️ Esto fue una conveniencia de laboratorio. `verify=False` y la desactivación de warnings SSL no deben tratarse como patrón de producción.

---

# 7. Primera prueba MCP

La primera prueba relevante fue deliberadamente sencilla: conseguir que Claude descubriera e invocara una tool del servidor local.

La tool utilizada como prueba fue:

```text
verificar_conexion
```

Flujo validado históricamente:

```text
Usuario
  ↓
Claude Desktop
  ↓ descubre tool MCP
verificar_conexion
  ↓
maximo_mcp.py
  ↓
respuesta devuelta a Claude
```

Este fue el hito principal que demostró que la comunicación MCP funcionaba de extremo a extremo.

---

# 8. Pruebas funcionales posteriores

Después de validar el mecanismo básico, se probaron consultas en lenguaje natural relacionadas con Maximo.

Ejemplos documentados:

```text
"Consulta la información de la orden de trabajo OT-2025"
```

```text
"¿Cuántos rodamientos tenemos en el almacén CENTRAL?"
```

En modo simulación el servidor devolvía datos mock y Claude los presentaba al usuario.

La convención utilizada era distinguir:

```text
🧪 [SIMULACIÓN]
```

frente a:

```text
✅ [REAL]
```

Aunque el modo real quedó diseñado en código, **no se validó contra una instancia viva de Maximo**.

---

# 9. Expansión del servidor MCP

El servidor evolucionó desde unas pocas tools iniciales hasta **14 tools**.

El código real confirma este catálogo:

| # | Tool | Objetivo |
|---:|---|---|
| 1 | `consultar_ot` | Consultar una orden de trabajo |
| 2 | `consultar_inventario` | Consultar inventario |
| 3 | `listar_transiciones_ot` | Ver transiciones de estado permitidas |
| 4 | `cambiar_estado_ot` | Cambiar estado de una OT |
| 5 | `query_maximo` | Consulta genérica a Object Structures |
| 6 | `consultar_activo` | Consultar un activo |
| 7 | `listar_object_structures` | Listar Object Structures |
| 8 | `crear_ot` | Crear una OT |
| 9 | `ws_editar_ot` | Preparar cambios en una OT |
| 10 | `ws_confirmar_cambios` | Confirmar cambios preparados |
| 11 | `ws_cancelar_cambios` | Cancelar cambios preparados |
| 12 | `obtener_workflow_assignments` | Consultar asignaciones de workflow |
| 13 | `enviar_workflow_response` | Responder workflow |
| 14 | `verificar_conexion` | Verificar servidor/conexión y catálogo |

---

# 10. Experimento de Working Set

Una parte especialmente interesante fue la introducción de un pequeño patrón de confirmación antes de persistir cambios.

Flujo:

```text
ws_editar_ot
   ↓
preparar / previsualizar cambio
   ↓
┌────────────────────┐
│                    │
↓                    ↓
confirmar          cancelar
↓                    ↓
ws_confirmar       ws_cancelar
_cambios           _cambios
```

El Working Set era **memoria temporal dentro del propio proceso Python**, no una funcionalidad nativa de Maximo.

Fue un experimento útil para aprender el patrón:

```text
proponer → revisar → confirmar
```

pero no debe confundirse con una implementación productiva o persistente.

---

# 11. Investigación con GitHub MCP

La documentación histórica registra que, una vez configurado GitHub MCP, se pidió a la IA investigar otros servidores MCP relacionados con Maximo.

Consulta aproximada utilizada:

```text
"Busca en GitHub otros servidores MCP de Maximo para ver si alguien ha programado funciones que nosotros no tenemos"
```

La investigación localizó implementaciones de terceros y posteriormente se amplió el `maximo_mcp.py` histórico.

Este episodio fue importante porque mostró que un entorno de IA podía combinar:

```text
MCP GitHub → investigar código
MCP Filesystem → trabajar con archivos
MCP Maximo → exponer lógica EAM
```

---

# 12. Configuración en VS Code + Cline

Cline utilizó un archivo de configuración específico para sus servidores MCP.

Ruta histórica documentada:

```text
%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
```

La configuración conceptual final era:

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

> ⚠️ Esta configuración se conserva como **referencia histórica**, no como recomendación actual. Los productos y servidores MCP han evolucionado y deben verificarse antes de reproducirla hoy.

---

# 13. Ciclo de operación histórico

Con Claude Desktop, después de modificar `maximo_mcp.py`, el procedimiento documentado era:

1. cerrar Claude Desktop completamente;
2. volver a abrirlo;
3. ir a `Settings > Developer`;
4. comprobar que el servidor MCP aparecía activo;
5. ejecutar una consulta de prueba.

Con Cline, el ciclo se hizo más corto y la documentación describe la posibilidad de refrescar el servidor MCP desde VS Code sin cerrar toda la aplicación.

---

# 14. Qué se probó realmente

## ✅ Verificado / sustentado por código y documentación

- servidor MCP local en Python/FastMCP;
- uso de `@mcp.tool()`;
- ejecución histórica de una tool desde Claude Desktop;
- modo simulación;
- catálogo real de 14 tools;
- lógica OSLC/REST prevista en código;
- evolución hacia VS Code + Cline;
- configuración histórica con Maximo MCP + Filesystem MCP + GitHub MCP;
- patrón experimental de Working Set.

## ⚠️ Documentado pero no reproducido hoy

- configuración exacta actual de Claude Desktop;
- configuración actual de Cline;
- disponibilidad actual de los mismos servidores MCP de Filesystem/GitHub;
- comportamiento actual del refresco/hot reload.

## ❌ No validado

- conexión viva con IBM Maximo;
- lectura real contra Maximo;
- escritura real contra Maximo;
- workflow real contra Maximo;
- seguridad productiva;
- RAG.

---

# 15. Problemas encontrados

## Python no estaba disponible desde terminal

Causa: `PATH` de Windows.

Resolución: corregir instalación/configuración hasta que:

```bash
python --version
```

funcionara correctamente.

## Ruta incorrecta del archivo de Claude

Se trabajó inicialmente con una ruta que no correspondía a la instalación real.

Resolución: utilizar la opción propia de Claude Desktop para localizar/editar la configuración efectiva.

## Dependencia de Maximo real

Problema: no había una instancia Maximo disponible para las pruebas.

Resolución: introducir `MODO_SIMULACION` y datos mock.

---

# 16. Decisiones que funcionaron bien

### Simular antes de integrar

Permitió aprender MCP independientemente de VPN, certificados o disponibilidad de Maximo.

### Empezar por una tool mínima

`verificar_conexion` permitió comprobar primero el protocolo antes de añadir lógica EAM.

### Encapsular capacidades EAM

Tools como `consultar_ot`, `crear_ot` o `obtener_workflow_assignments` expresaban intención funcional, no únicamente llamadas HTTP genéricas.

### Introducir confirmación antes de cambios

El patrón Working Set exploró tempranamente la idea de human-in-the-loop.

### Separar servidores por capacidad

Maximo, filesystem y GitHub demostraron que MCP permite combinar diferentes dominios de capacidades bajo un mismo entorno de IA.

---

# 17. Limitaciones y riesgos detectados en el código histórico

El código fue útil para aprender, pero contiene simplificaciones propias de una PoC:

- `verify=False` para HTTPS;
- warnings SSL deshabilitados;
- API key modelada como variable de configuración;
- transiciones de estado codificadas de forma fija;
- Working Set únicamente en memoria;
- respuestas principalmente como strings formateados;
- consulta genérica `query_maximo` con alcance amplio;
- falta de validación contra configuración real de Maximo;
- escrituras no validadas en un entorno real.

Estos puntos deben tratarse como **deuda/limitación histórica**, no como patrones recomendados para producción.

---

# 18. Qué aprendimos conceptualmente

📘 **Host**: aplicación de IA que gestiona la experiencia y las conexiones MCP.

📘 **Client**: componente que mantiene la conexión con un servidor MCP.

📘 **Server**: proceso que expone capacidades a través del protocolo.

📘 **Tools**: operaciones invocables por el modelo/host.

📘 MCP no sustituye necesariamente APIs existentes. Puede actuar como una capa estándar sobre OSLC, REST u otros servicios.

📘 MCP por sí solo no convierte un LLM en agente autónomo. La lógica del host/agente determina cuándo y cómo usar las capacidades.

📘 MCP es más amplio que Tools: el protocolo también contempla otros tipos de capacidades como Resources y Prompts.

---

# 19. Relación con IBM Maximo

El patrón estudiado fue:

```text
Aplicación IA
    ↓
MCP
    ↓
Tool orientada a EAM
    ↓
OSLC / REST / servicio Maximo
    ↓
IBM Maximo Manage
```

La principal enseñanza es que MCP puede ofrecer una **frontera semántica para IA** sin eliminar las APIs de Maximo que ejecutan la operación real.

---

# 20. Relación con AI-EAM-MAXIMO

Este laboratorio es un antecedente de aprendizaje.

```text
Learning Lab MCP
     ↓
aprendizaje validado
     ↓
🟨 CANDIDATO A INCORPORAR
     ↓ revisión explícita
AI-EAM-MAXIMO
```

Nada de este laboratorio se considera automáticamente arquitectura o código aprobado del producto.

---

# 21. Cómo volver a entender este trabajo dentro de 3 meses

Leer en este orden:

1. `mcp/README.md` — visión general del laboratorio MCP.
2. `mcp/docs/MCP_PRACTICAL_WALKTHROUGH.md` — este documento; recorrido paso a paso.
3. `mcp/docs/history/MCP_HISTORICAL_LAB.md` — reconstrucción y auditoría histórica detallada.
4. `mcp/docs/MCP_LAB_HANDOFF.md` — estado final y continuidad.
5. `jperdomo12/Maximo-IA-Project/maximo_mcp.py` — código fuente histórico real.

Con esos cinco elementos debe ser posible reconstruir qué se hizo sin depender del historial del chat.

---

# 22. Estado final

✅ **Laboratorio MCP cerrado para el alcance actual.**

Quedó documentado:

- por qué se inició;
- qué software se utilizó;
- qué se instaló;
- cómo se configuró;
- cómo se creó el servidor MCP;
- cómo se probó;
- cómo evolucionó;
- qué 14 tools existieron;
- qué funcionó;
- qué no fue validado;
- qué aprendimos;
- qué riesgos tenía la PoC;
- cómo se relaciona con IBM Maximo y AI-EAM-MAXIMO.

➡️ Próximo laboratorio: **RAG**.
