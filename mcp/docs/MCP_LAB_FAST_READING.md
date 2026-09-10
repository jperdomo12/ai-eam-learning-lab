# ⚡ MCP LAB — Fast Reading

> 🎯 **Objetivo:** recuperar en pocos minutos qué buscó el laboratorio MCP, qué se construyó, cómo se configuró, cómo se probó y qué quedó realmente demostrado.
>
> 📍 **Estado:** ✅ resumen vigente del laboratorio MCP cerrado para su alcance actual.
>
> 📘 **Documento completo:** [`MCP_LAB_DOCUMENTATION.md`](MCP_LAB_DOCUMENTATION.md)

## 🕘 Historial

| Fecha | Cambio |
|---|---|
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

## 5. Software y configuración usada

Componentes principales:

| Componente | Para qué se usó |
|---|---|
| Python + FastMCP | implementar el MCP Server Maximo |
| Claude Desktop | primer Host práctico de la PoC |
| VS Code + Cline | iterar sobre código/configuración con menos fricción |
| Node.js / `npx` | ejecutar MCP Servers adicionales |
| Filesystem MCP | leer/escribir únicamente en carpetas autorizadas |
| GitHub MCP | investigar repositorios y código |
| `requests` / `urllib3` | preparar llamadas HTTP/OSLC hacia Maximo |

Ubicación local histórica del laboratorio:

```text
C:\Users\jpperdomo\JP\Profesional\IA\MCP-Claude
```

Código principal:

```text
C:\Users\jpperdomo\JP\Profesional\IA\MCP-Claude\maximo_mcp.py
```

En el Learning Lab la copia preservada está en:

```text
mcp/src/maximo_mcp.py
```

La configuración real de Claude se obtenía desde:

```text
Claude Desktop
→ Configuración
→ Desarrollador
→ Editar configuración
```

La copia pública y sanitizada está en:

```text
mcp/config/claude_desktop_config.example.json
```

---

## 6. Cómo se comunicaban los componentes

`claude_desktop_config.json` **no era el canal de intercambio**. Era solamente el archivo que indicaba a Claude qué servidores MCP debía iniciar y con qué comandos.

La ejecución local utilizó **stdio**:

```text
Claude / MCP Client
     ↓ mensaje JSON-RPC por stdin
maximo_mcp.py
     ↑ resultado JSON-RPC por stdout
Claude / MCP Client
```

Por tanto:

```text
archivo .json       = configuración guardada en disco
mensaje JSON-RPC    = información intercambiada durante MCP
stdio               = transporte local utilizado
```

---

## 7. Cómo se probó desde Claude Desktop

La primera Tool deliberadamente simple fue:

```text
verificar_conexion
```

La secuencia fue aproximadamente:

```text
1. Crear maximo_mcp.py.
2. Exponer verificar_conexion con @mcp.tool().
3. Registrar el servidor en claude_desktop_config.json.
4. Cerrar Claude Desktop completamente.
5. Abrirlo nuevamente.
6. Ir a Settings → Developer.
7. Comprobar/activar el servidor MCP.
8. Pedir desde el chat que ejecutara la prueba.
9. Recibir la respuesta del MCP Server.
```

Este hito confirmó **Claude Desktop ↔ MCP Server local**, no una conexión a IBM Maximo real.

Después se probaron operaciones EAM simuladas, por ejemplo consulta de OTs, inventario y cambios de estado.

### Fricción detectada

Para que Claude Desktop recogiera ciertos cambios de configuración/servidor, el flujo documentado implicaba salir completamente, volver a entrar y comprobar otra vez el servidor en Developer. Esto hacía lenta la iteración frecuente.

---

## 8. Cómo se probó desde VS Code + Cline

Cline se incorporó para concentrar el ciclo de desarrollo dentro del IDE:

```text
pedir cambio
   ↓
Cline revisa/modifica código
   ↓
usuario revisa diff
   ↓
refrescar/reiniciar MCP Server
   ↓
probar desde el mismo entorno
```

La mejora principal fue **reducir la fricción de iterar** sobre el servidor MCP. No fue únicamente una cuestión de copiar/pegar código.

Cline también permitió trabajar con varios MCP Servers configurados simultáneamente.

---

## 9. Ejemplos de pruebas y resultados

### Maximo MCP — consulta de inventario

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

### Maximo MCP — cambio de estado

Se probaron cambios simulados de estado respetando una tabla local de transiciones válidas. El script devolvía estado anterior, estado nuevo, memo y timestamp.

### Working Set

Se podía preparar un cambio de campos, obtener un preview y después confirmar o cancelar.

### Filesystem MCP

Se documentaron pruebas para:

- listar archivos de una carpeta autorizada;
- escribir un archivo dentro de una carpeta autorizada.

La configuración limitaba explícitamente las carpetas a las que el servidor podía acceder.

### GitHub MCP

Se utilizó para investigar repositorios relacionados con MCP + Maximo y comparar capacidades. Esa investigación contribuyó a ampliar el servidor local hasta el catálogo final de 14 Tools.

---

## 10. “Tridente MCP”

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

## 11. Lo más importante que aprendimos

1. **Host ≠ PC.** El Host es la aplicación/entorno de IA.
2. Un MCP Server expone capacidades; nuestra PoC se centró en **Tools**.
3. MCP también contempla otras primitivas como **Resources** y **Prompts**.
4. MCP no convierte por sí solo a un LLM en agente autónomo.
5. En local, **stdio** permite conectar Host/Client y Server sin desplegar un servicio HTTP.
6. Los mensajes de ejecución viajan como **JSON/JSON-RPC**, pero eso no significa intercambiar archivos `.json`.
7. **MCP y OSLC/REST son complementarios**: MCP puede ser la frontera orientada a IA y OSLC/REST la integración real con Maximo.
8. **Simular primero** fue una buena decisión: permitió aprender MCP sin depender de la infraestructura Maximo.
9. Para escrituras EAM, el patrón **proponer → revisar → confirmar** es más seguro que ejecutar cambios silenciosamente.
10. Combinar servidores especializados —Maximo, filesystem y GitHub— resultó más claro que mezclar todas las capacidades en un único componente.

---

## 12. Qué no debemos confundir con una solución productiva

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

## 13. Relación con RAG y AI-EAM-MAXIMO

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

## 14. Dónde continuar si vuelves meses después

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
