# LAB — Paso 08: evaluación de generación fundamentada

> **Tipo:** LAB  
> **Estado:** ✅ VERIFICADO — Paso 08 cerrado  
> **Fecha:** 2026-09-14

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-14 | ✅ Se completa el **Paso 08C** con generación reproducible mediante API local de Ollama (`temperature=0`, `seed=42`, dos repeticiones por prompt). Ambos prompts producen salidas idénticas entre repeticiones. Bajo las mismas condiciones, el **Prompt A baseline** sigue siendo parcialmente incompleto, mientras el **Prompt B orientado a completeness** cubre inspección, seguridad, procedimiento completo de calibración, criterios de aceptación y acción ante tolerancia excedida. Se confirma que, en este experimento, la mejora procede del prompt y no del retrieval. |
| 2026-09-14 | ✅ Se cierra el **Paso 08** para el nivel de aprendizaje buscado. `Groundedness` y `abstention` quedan satisfactoriamente demostrados; `completeness` mejora de forma clara con el prompt 08B bajo condiciones reproducibles. El formato exacto de citas `[FUENTE n]` no se fuerza más: el modelo referencia correctamente las fuentes, aunque use formas como `(FUENTE 2)`. No se continuarán optimizaciones de prompt, modelo, sampling ni evaluación automática en esta etapa. |
| 2026-09-14 | 🧪 Se ejecuta el **Paso 08B — Caso D** con el mismo prompt orientado a completeness. La abstención se conserva: el modelo declara que el contexto no contiene el par de apriete y no inventa ningún valor. La respuesta sigue sin respetar exactamente el formato solicitado `[FUENTE n]`, usando una referencia textual global a las fuentes. |
| 2026-09-14 | ⚙️ Se identifica una limitación metodológica importante de las comparaciones 08/08B: la generación se ejecutó mediante `ollama run` sin fijar explícitamente parámetros de muestreo. Por tanto, aunque retrieval/modelo/pregunta se mantuvieron, una sola ejecución por prompt no permite atribuir toda diferencia únicamente al prompt. Se prepara el **Paso 08C** con API local de Ollama, `temperature=0`, `seed=42` y dos repeticiones por prompt para crear una comparación reproducible. |
| 2026-09-14 | 🧪 Se ejecuta el **Paso 08B — Caso C** variando las instrucciones del prompt. La respuesta mejora claramente respecto a la baseline: cubre inspección, seguridad y menciona el procedimiento de calibración. Sin embargo, sigue siendo **parcialmente incompleta**: resume el procedimiento en lugar de desarrollar sus pasos respaldados y omite los criterios de aceptación de `[FUENTE 3]`. Además, las referencias aparecen como `FUENTE 1`/`FUENTE 4` en lugar del formato solicitado `[FUENTE n]`. |
| 2026-09-14 | Se documenta la baseline end-to-end del Paso 08 con Ollama + `llama3:latest`: Caso C fundamentado pero incompleto y Caso D con abstención correcta. Se prepara el Paso 08B para variar únicamente las instrucciones del prompt y estudiar `completeness` sin cambiar retrieval, `Top-k` ni modelo. |

---

## 1. Objetivo

Evaluar la etapa de **generation** después de haber verificado retrieval, contexto y prompt base.

Pipeline mantenido:

```text
pregunta
→ embedding de consulta
→ índice persistido
→ retrieval semántico
→ Top-k = 4
→ texto original + procedencia
→ prompt
→ LLM local
→ respuesta
```

La finalidad es distinguir claramente problemas de retrieval de problemas de generación.

---

## 2. Baseline local utilizada

```text
Runtime:       Ollama 0.34.0
Modelo:        llama3:latest
Arquitectura:  Llama 3
Parámetros:    8.0B
Contexto:      8192
Cuantización:  Q4_0
Top-k:         4
API key:       no requerida
Coste API:     0
```

Se reutilizó una instalación local preexistente en lugar de instalar otro runtime o descargar otro modelo.

El modelo de embeddings sigue siendo independiente:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Por tanto:

```text
MiniLM → retrieval
Llama 3 → generation
```

---

## 3. Paso 08 baseline — Caso C

Pregunta:

```text
¿Qué debo verificar antes de ajustar el PT-201 y cómo debo calibrarlo?
```

Top-4 recuperado:

```text
#1 | 0.6864 | Inspección previa
#2 | 0.6438 | Procedimiento de calibración
#3 | 0.4909 | Criterio de aceptación
#4 | 0.4400 | Antes de calibrar un transmisor de presión
```

El contexto contenía evidencia suficiente para:

```text
- inspección previa
- seguridad previa
- procedimiento de calibración
- criterio de aceptación
```

La primera generación fue conservadora y fundamentada, pero incompleta: utilizó inspección y seguridad y omitió procedimiento y criterios.

Evaluación:

```text
groundedness         → BUENA
completeness         → INSUFICIENTE
citation correctness → razonable para lo que sí respondió
abstention           → no aplica
```

Aprendizaje:

> **Retrieval completo ≠ generación completa.**

---

## 4. Paso 08 baseline — Caso D

Pregunta:

```text
¿Cuál es el par de apriete de los bornes eléctricos del PT-201?
```

Top-4 recuperado:

```text
#1 | 0.5414 | Inspección previa
#2 | 0.4098 | Procedimiento de calibración
#3 | 0.3795 | Lectura inestable
#4 | 0.3564 | Antes de calibrar un transmisor de presión
```

Ningún chunk contiene un valor de par de apriete para bornes eléctricos.

Respuesta observada:

```text
No se encuentra información en el contexto recuperado sobre el par de
apriete de los bornes eléctricos del PT-201. Las fuentes proporcionadas no
contienen información sobre este tema.
```

Evaluación:

```text
groundedness         → BUENA
completeness         → CORRECTA para una pregunta sin evidencia
citation correctness → sin referencias explícitas exactas
abstention           → CORRECTA
```

Aprendizaje:

> **Top-k existente no obliga a inventar una respuesta.**

---

## 5. Paso 08B — prompt orientado a completeness

Se varió una sola variable conceptual:

```text
PROMPT
```

Se mantuvo:

```text
mismo índice
mismo modelo de embeddings
mismo retrieval
mismo Top-k = 4
mismo Ollama
mismo llama3:latest
mismas preguntas
```

El prompt 08B exige:

```text
1. identificar todas las partes de la pregunta;
2. revisar todas las fuentes recuperadas;
3. responder cada parte respaldada por evidencia;
4. declarar qué parte carece de evidencia;
5. verificar antes de finalizar que no se omitió evidencia aplicable.
```

Script:

```text
rag/src/step08b_generate_grounded_answer_prompt_completeness.py
```

### 5.1 Caso C con prompt 08B

En la primera ejecución no determinista, la respuesta mejoró pero siguió parcialmente incompleta: cubrió inspección y seguridad, mencionó calibración, pero resumió el procedimiento y omitió criterios de aceptación.

### 5.2 Caso D con prompt 08B

La abstención se mantuvo correctamente. El modelo declaró ausencia de evidencia y no inventó un valor de torque.

Conclusión provisional:

> **El prompt influye en la calidad generativa, pero una ejecución aislada no basta para medir rigurosamente el efecto.**

---

## 6. Paso 08C — comparación reproducible de prompts

Para controlar la variabilidad de generación se utiliza la API local de Ollama con:

```text
temperature = 0.0
seed        = 42
repeticiones por prompt = 2
```

Script:

```text
rag/src/step08c_compare_prompts_deterministic.py
```

Se compara:

```text
PROMPT A → baseline del Paso 08
PROMPT B → completeness del Paso 08B
```

manteniendo exactamente el mismo:

```text
índice
embedding model
retrieval
Top-k = 4
llama3:latest
pregunta
parámetros de generación
```

### 6.1 Reproducibilidad

Resultado:

```text
Prompt A → ejecución 1 == ejecución 2
Prompt B → ejecución 1 == ejecución 2
```

Por tanto, para este control:

```text
Prompt A reproducible → True
Prompt B reproducible → True
```

### 6.2 Prompt A — resultado reproducible

El prompt baseline cubre:

```text
inspección previa      → sí
seguridad previa       → sí
procedimiento          → solo resumido
criterio de aceptación → omitido
```

La respuesta permanece fundamentada, pero no explota toda la evidencia disponible.

### 6.3 Prompt B — resultado reproducible

El prompt orientado a completeness cubre:

```text
inspección previa      → sí
seguridad previa       → sí
procedimiento completo → sí
ZERO / SPAN            → sí
0 / 5 / 10 bar         → sí
±0,05 bar              → sí
as-left                 → sí
criterio aceptación    → sí
evaluación adicional   → sí
```

No se observan valores técnicos ajenos al contexto.

Las referencias corresponden a las fuentes correctas, aunque el modelo usa formas como `(FUENTE 2)` en lugar de respetar literalmente `[FUENTE 2]`.

### 6.4 Conclusión del control

Bajo condiciones reproducibles:

```text
mismo retrieval
mismo contexto
mismo LLM
mismos parámetros
          ↓
solo cambia el prompt
          ↓
Prompt B produce una respuesta sustancialmente más completa
```

Por tanto, en este experimento puede afirmarse que **la formulación del prompt mejoró `completeness` sin cambiar el retrieval**.

---

## 7. Resultado final del Paso 08

Evaluación consolidada:

```text
Groundedness         → ✅ SATISFACTORIA
Completeness         → ✅ SATISFACTORIA con prompt orientado a cobertura
Abstention           → ✅ SATISFACTORIA en el Caso D probado
Citation correctness → 🟡 SEMÁNTICAMENTE CORRECTA; formato literal no siempre respetado
Reproducibilidad      → ✅ VERIFICADA en el control 08C
```

Aprendizajes principales:

```text
1. retrieval correcto no garantiza una respuesta completa;
2. generation debe evaluarse como una capa independiente;
3. un mejor prompt puede mejorar completeness sin tocar retrieval;
4. abstention puede funcionar aunque el retriever siempre entregue Top-k;
5. para comparar prompts conviene controlar también los parámetros de generación;
6. embeddings, retriever y LLM generativo pueden ser componentes desacoplados.
```

---

## 8. Decisión de cierre

Para el objetivo de aprendizaje actual, **no se requieren más experimentos de optimización en esta etapa**.

No se continuará ahora con:

- más variantes de prompt;
- comparación de otros LLM locales;
- ajuste fino de `temperature`, `seed` u otros parámetros;
- thresholds de answerability;
- jueces LLM;
- evaluación automática avanzada;
- reranking o retrieval híbrido por motivos de generación.

Estas técnicas quedan como conocimiento posterior si una necesidad concreta de AI-EAM-MAXIMO las justifica.

El siguiente bloque del Learning Lab debe regresar al objetivo EAM:

```text
RAG básico comprendido y probado
        ↓
Simulación Maximo / doclinks
        ↓
contexto EAM para localizar documentos
        ↓
RAG sobre el documento localizado
```

---

## 9. Lo que NO se concluye

Este LAB no demuestra que:

- Llama 3 sea el modelo generativo definitivo;
- el prompt 08B sea universalmente óptimo;
- `Top-k=4` sea apropiado fuera de este corpus;
- la abstención sea robusta para cualquier pregunta;
- el índice NumPy/JSON sea una solución de producción;
- exista un threshold universal de similarity;
- Ollama sea la arquitectura recomendada para AI-EAM-MAXIMO.

Todos esos elementos siguen siendo **baselines pedagógicas del LAB**, no decisiones productivas.
