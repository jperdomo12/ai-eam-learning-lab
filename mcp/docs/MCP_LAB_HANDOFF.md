# 🧭 MCP_LAB_HANDOFF

> 📍 **Estado:** 🟨 **ÚLTIMA REVALIDACIÓN PENDIENTE — Claude Desktop cerrado correctamente; falta refresco final en VS Code + Cline antes de congelar MCP LAB**
> 🗓️ **Actualizado:** 2026-09-11

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-11 | Se ejecuta con éxito la prueba mixta **Maximo MCP + Filesystem MCP**: Claude consulta OTs abiertas simuladas y crea `ots_abiertas.csv` en `C:\Users\jpperdomo\Downloads`. La prueba confirma composición de capacidades entre dos MCP Servers. |
| 2026-09-11 | Se consolida el aprendizaje de selección de Tools: no es obligatorio indicar “usa MCP” en una petición normal; el Host puede elegir Tools a partir de intención, nombre, descripción/docstring y esquema de parámetros. Para una prueba controlada sí puede mencionarse explícitamente el MCP/Tool que se quiere observar. |
| 2026-09-11 | Se cierra el issue #1 sin reinstalar GitHub MCP. Se documenta qué ocurrió, por qué la configuración histórica dejó de ser una referencia vigente y cómo recuperarlo en el futuro con el servidor oficial actual de GitHub. |
| 2026-09-11 | Se confirma que el patrón del vídeo de referencia sigue siendo válido para aprender MCP local; lo obsoleto es el paquete histórico `@modelcontextprotocol/server-github`, no el modelo `Host → MCP local → stdio`. |
| 2026-09-11 | Se verifica que Docker no está instalado y que el equipo es `AMD64`. Si algún día se retoma GitHub MCP local, puede usarse el binario oficial Windows x86_64 de `github/github-mcp-server`, sin necesidad de instalar Docker solo para este laboratorio. |
| 2026-09-10 | Se corrige una observación de la sesión: en `Configuración → Conectores` sí aparece **Integración de GitHub** de tipo Web. No debe confundirse automáticamente con el GitHub MCP local histórico. |
| 2026-09-10 | Se reabre el laboratorio práctico para refrescar y revalidar la configuración histórica. Maximo MCP y Filesystem MCP continúan operativos; la recuperación de GitHub MCP en Claude Desktop queda registrada en el issue #1. |
| 2026-09-10 | Se cierra la consolidación documental con `MCP_LAB_DOCUMENTATION.md` v1.1 y `MCP_LAB_FAST_READING.md` como entrada rápida. |
| 2026-09-10 | Se adopta `MCP_LAB_DOCUMENTATION.md` como documento principal; el código `maximo_mcp.py` y la configuración sanitizada de Claude quedan preservados dentro del propio Learning Lab. |
| 2026-09-10 | Consolidación del trabajo previo realizado con Gemini / Claude Desktop / VS Code + Cline. |
| 2026-09-10 | Creación del HandOff inicial. |

## Dónde estamos

La **baseline documental MCP está consolidada** y la revalidación práctica en **Claude Desktop** queda satisfactoriamente cerrada para el objetivo de aprendizaje.

Estado actual:

- ✅ **Maximo MCP** continúa configurado y operativo en Claude Desktop.
- ✅ **Filesystem MCP** continúa configurado y operativo en Claude Desktop.
- ✅ **Composición Maximo + Filesystem** validada de extremo a extremo dentro del alcance simulado: consulta de OTs abiertas → creación de CSV en carpeta local autorizada.
- 🟨 **GitHub MCP histórico**: aprendizaje y funcionamiento histórico preservados, pero la implementación usada entonces ya no se considera una referencia vigente para reinstalar.
- ✅ El incidente GitHub y su resolución conceptual quedaron documentados en el issue [#1](https://github.com/jperdomo12/ai-eam-learning-lab/issues/1), cerrado sin continuar la instalación.
- ✅ La **Integración de GitHub Web** visible en Claude Desktop es un mecanismo distinto y no se toma como sustituto automático del GitHub MCP local histórico.
- ⏳ **Último paso antes de congelar MCP LAB:** refrescar la configuración histórica en **VS Code + Cline**, verificar qué MCP siguen operativos y repetir una prueba mínima desde ese entorno.

El traslado a `ai-eam-learning-lab` no inicia un proyecto nuevo: consolida y continúa el trabajo realizado previamente con Gemini, Claude Desktop y Cline bajo un modelo ChatGPT ↔ GitHub más organizado y persistente.

La documentación cruda previa queda como material de referencia de transición; el conocimiento vigente ya está absorbido en la documentación del Learning Lab.

## Prueba final validada en Claude Desktop — composición de MCP Servers

### Objetivo

Comprobar que el Host puede resolver una sola instrucción usando **dos MCP Servers especializados**:

```text
Maximo MCP      → obtener información EAM
Filesystem MCP  → persistir un archivo local
```

### Ejecución

La petición solicitó, en esencia:

```text
Consulta las OTs abiertas, genera un archivo CSV con wonum,
descripción, estado y activo, y guárdalo en Downloads.
```

Resultado confirmado:

```text
Claude Desktop
   ├─ Maximo MCP      → obtiene OTs abiertas desde los mocks de maximo_mcp.py
   └─ Filesystem MCP  → crea ots_abiertas.csv
                          ↓
                  C:\Users\jpperdomo\Downloads
```

`Downloads` estaba autorizada explícitamente en la configuración de Filesystem MCP. La prueba funcionó correctamente.

### Qué demuestra

- el Host puede **componer Tools de servidores diferentes** dentro de una misma tarea;
- Filesystem MCP respeta un conjunto explícito de carpetas autorizadas;
- la petición de usuario **no necesita mencionar MCP de forma obligatoria** cuando el Host puede inferir las capacidades requeridas;
- el resultado EAM sigue siendo **simulado**, porque `maximo_mcp.py` continúa en `MODO_SIMULACION = True`.

## Selección de Tools — aprendizaje consolidado

Sí, las buenas descripciones ayudan a que la IA decida cuándo usar una Tool.

Con FastMCP, la información visible para el cliente/modelo deriva normalmente de:

```text
nombre de la función  → nombre de la Tool
docstring             → descripción de la Tool
type hints/parámetros → esquema de entrada
```

Ejemplo real del laboratorio:

```python
@mcp.tool()
def consultar_ot(num_ot: str) -> str:
    """Consulta los detalles completos de una Orden de Trabajo (OT) en Maximo."""
```

Y una descripción más orientativa:

```python
@mcp.tool()
def listar_transiciones_ot(num_ot: str) -> str:
    """
    Muestra el estado actual de una OT y los cambios de estado permitidos.
    Úsala antes de cambiar_estado_ot para saber qué opciones hay disponibles.
    Ejemplo: "¿A qué estados puedo mover la OT-1002?"
    """
```

La segunda ofrece más señales para diferenciar cuándo corresponde **consultar** de cuándo corresponde **listar transiciones**.

Regla práctica:

> **Tool names claros + descripciones/docstrings precisos + parámetros bien definidos mejoran la probabilidad de selección correcta.**

No es una garantía determinista: el modelo sigue evaluando intención, contexto, Tools disponibles, permisos y políticas.

Por ello:

- **uso normal:** no hace falta escribir “usa MCP” si la intención es suficiente;
- **laboratorio/prueba controlada:** conviene mencionar el MCP o la Tool si queremos comprobar explícitamente esa ruta.

## Cierre del issue #1 — GitHub MCP en Claude Desktop actual

### Qué pasó

Históricamente el laboratorio utilizó:

```text
npx -y @modelcontextprotocol/server-github
```

con un `GITHUB_PERSONAL_ACCESS_TOKEN` configurado en `claude_desktop_config.json`. Esta configuración funcionó durante meses y formó parte real del aprendizaje del “Tridente MCP”.

Durante la revalidación de septiembre de 2026:

- el PAT histórico fue revocado y sustituido por uno nuevo durante las pruebas;
- Claude Desktop actual mostró un comportamiento diferente al histórico al reescribir su configuración;
- se identificó y aisló correctamente el proceso del antiguo GitHub MCP;
- se eliminó su configuración sin afectar Maximo ni Filesystem;
- el servidor histórico dejó de reaparecer tras reiniciar Claude;
- se comprobó además que existen varias copias históricas de `claude_desktop_config.json` en el disco, por lo que no debe inferirse que todas sean archivos activos;
- no se considera necesario seguir investigando el origen exacto de cada copia ni reinstalar GitHub MCP para cumplir el objetivo de aprendizaje.

### Por qué ya no se reinstala igual

El problema no invalida MCP ni el enfoque del laboratorio. Lo que quedó desactualizado es la implementación concreta utilizada para GitHub:

```text
@modelcontextprotocol/server-github
```

Ese paquete está deprecated/archivado y GitHub mantiene actualmente su servidor oficial en:

```text
https://github.com/github/github-mcp-server
```

Por tanto:

```text
PATRÓN QUE SIGUE VÁLIDO
Host de IA → MCP Server local → stdio → Tools

IMPLEMENTACIÓN HISTÓRICA QUE NO SE RECOMIENDA REINSTALAR
npx @modelcontextprotocol/server-github + PAT
```

El vídeo de referencia usado para aprender MCP sigue siendo útil para el **patrón conceptual y práctico de MCP local**. No debe interpretarse como garantía de que todos los paquetes concretos mostrados entonces continúen vigentes años después.

### Cómo recuperar GitHub MCP si alguna vez vuelve a ser necesario

No se hará ahora, pero la ruta queda definida para no repetir la investigación:

1. usar el servidor oficial actual `github/github-mcp-server`;
2. mantenerlo como MCP local por `stdio`, si se desea reproducir la filosofía del “Tridente”;
3. en este equipo Windows, ya se confirmó arquitectura `AMD64`, por lo que puede utilizarse el release oficial `Windows_x86_64`;
4. alternativa: Docker, aunque actualmente **Docker no está instalado** y no se justifica instalarlo solo para este laboratorio;
5. registrar el ejecutable/servidor en Claude Desktop mediante la configuración MCP local vigente;
6. usar autenticación GitHub con mínimo privilegio y nunca persistir PAT reales en el repositorio;
7. validar al menos lectura de repositorio, lectura de archivo y acceso a Issues antes de considerar recuperado el tercer componente.

La **Integración de GitHub Web** de Claude puede ser útil para otros casos, pero no se documenta como equivalente al GitHub MCP local histórico sin una prueba funcional específica.

### Decisión

> **No invertir más tiempo en reinstalar GitHub MCP dentro de esta revalidación.**

El objetivo de aprendizaje ya se cumplió históricamente. El incidente actual aporta además un aprendizaje válido sobre evolución de herramientas: el patrón MCP puede permanecer vigente aunque una implementación concreta quede deprecated.

## Documentos vigentes

Para recuperar el laboratorio:

```text
mcp/docs/MCP_LAB_FAST_READING.md      ← recuperación rápida
mcp/docs/MCP_LAB_DOCUMENTATION.md     ← fuente completa y canónica
mcp/docs/MCP_LAB_HANDOFF.md           ← estado y continuidad
```

`MCP_LAB_FAST_READING.md` ya incorpora la prueba mixta ejecutada y el aprendizaje sobre selección de Tools. `MCP_LAB_DOCUMENTATION.md` mantiene la baseline consolidada; al terminar la última revalidación de VS Code + Cline se realizará el cierre documental final para congelar el frente MCP antes de abrir RAG.

## Artefactos preservados

```text
mcp/src/maximo_mcp.py
mcp/src/history/connection_test.py
mcp/src/history/maximo_mcp_gemini_v1.py
mcp/config/claude_desktop_config.example.json
```

El código final confirma servidor Python/FastMCP, `MODO_SIMULACION = True`, datos mock, rama OSLC/REST preparada, 14 Tools y Working Set temporal.

La configuración Claude sanitizada conserva como **evidencia histórica** la combinación Maximo MCP + Filesystem MCP + GitHub MCP. No debe interpretarse como receta actual para reinstalar el antiguo paquete GitHub.

## Qué quedó probado históricamente y en la revalidación actual

- ejecución de un MCP Server local con Python/FastMCP;
- invocación de Tools desde Claude Desktop;
- modo simulación para capacidades EAM;
- consultas y cambios de estado simulados;
- Filesystem MCP para listar/escribir archivos;
- composición validada **Maximo MCP + Filesystem MCP → CSV**;
- uso histórico de GitHub MCP para investigar código;
- evolución histórica a VS Code + Cline;
- entorno multi-MCP “Tridente”;
- catálogo final de 14 Tools recuperado en código;
- experimentación con Working Set / confirmación humana;
- importancia práctica de nombre, descripción/docstring y esquema de argumentos para el descubrimiento/selección de Tools.

## Qué NO quedó validado

- conexión con una instancia viva de IBM Maximo;
- lectura/escritura real contra Maximo;
- workflow real contra Maximo;
- seguridad productiva;
- compatibilidad actual de toda la configuración histórica;
- funcionamiento actual del GitHub MCP oficial en esta máquina, porque se decidió conscientemente no instalarlo;
- equivalencia funcional entre la **Integración de GitHub Web** actual y el GitHub MCP local histórico;
- **estado actual de la configuración MCP en VS Code + Cline**, que será la última comprobación antes de congelar el LAB.

## Relación con AI-EAM-MAXIMO

El Learning Lab conserva aprendizaje y evidencia. Cualquier patrón que deba trasladarse al producto `jperdomo12/ai-driven-eam-copilot` se tratará allí como **🟨 CANDIDATO A INCORPORAR** y seguirá su gobernanza formal.

## Próximo paso

➡️ **Refrescar la configuración MCP de VS Code + Cline y realizar una prueba mínima desde ese entorno.**

Objetivo de esa última sesión:

```text
1. Abrir VS Code + Cline.
2. Localizar/revisar la configuración MCP efectiva.
3. Verificar qué servidores aparecen y cuáles arrancan actualmente.
4. Probar al menos Maximo MCP.
5. Si Filesystem está disponible, realizar una prueba corta adicional.
6. No bloquear el cierre por GitHub MCP histórico.
7. Documentar el resultado final.
8. Congelar/cerrar MCP LAB.
9. Pasar al laboratorio RAG.
```

No reabrir decisiones ya cerradas sobre GitHub MCP salvo que aparezca una nueva necesidad real.