# LAB — Paso 08: evaluación de generación fundamentada

> **Tipo:** LAB  
> **Estado:** 🧪 EN CURSO — Paso 08B Caso C ejecutado; pendiente Caso D con el mismo prompt  
> **Fecha:** 2026-09-14

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-14 | 🧪 Se ejecuta el **Paso 08B — Caso C** variando únicamente el prompt. La respuesta mejora claramente respecto a la baseline: cubre inspección, seguridad y menciona el procedimiento de calibración. Sin embargo, sigue siendo **parcialmente incompleta**: resume el procedimiento en lugar de desarrollar sus pasos respaldados y omite los criterios de aceptación de `[FUENTE 3]`. Además, las referencias aparecen como `FUENTE 1`/`FUENTE 4` en lugar del formato solicitado `[FUENTE n]`. Se confirma que el prompt influye en `completeness`, pero una única mejora de instrucciones no garantiza cobertura exhaustiva ni cumplimiento de formato. Antes de otro cambio se repetirá el Caso D con el mismo prompt 08B para comprobar que `abstention` se conserva. |
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

## 3. Caso C — información repartida

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

El contexto enviado al LLM contenía evidencia suficiente para:

```text
- inspección previa
- seguridad previa
- procedimiento de calibración
- criterio de aceptación
```

Resultado del LLM:

- utilizó correctamente inspección y seguridad;
- no inventó valores ni condiciones externas;
- omitió por completo el procedimiento de calibración;
- omitió los criterios de aceptación.

Evaluación:

```text
groundedness         → BUENA
completeness         → INSUFICIENTE
citation correctness → razonable para lo que sí respondió
abstention           → no aplica a este caso
```

Aprendizaje:

> **Retrieval completo ≠ generación completa.**

La evidencia puede llegar correctamente al LLM y aun así no ser utilizada de forma suficiente en la respuesta.

---

## 4. Caso D — respuesta inexistente

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
citation correctness → no usó referencias explícitas, pero tampoco afirmó datos técnicos
abstention           → CORRECTA
```

Aprendizaje:

> **Top-k existente no obliga a inventar una respuesta.**

La instrucción de declarar evidencia insuficiente fue obedecida por `llama3:latest` en este caso.

---

## 5. Comparación C vs. D de la baseline

```text
CASO C
contexto suficiente
→ respuesta fundamentada
→ pero incompleta

CASO D
contexto insuficiente para la pregunta
→ respuesta se abstiene correctamente
```

Esto separa dos capacidades distintas:

```text
COMPLETENESS
¿el LLM usa toda la evidencia necesaria disponible?

ABSTENTION
¿el LLM evita inventar cuando la evidencia no existe?
```

La baseline local muestra:

```text
completeness → necesita mejora
abstention   → funciona en el caso probado
```

---

## 6. Paso 08B — prompt orientado a completeness

Antes de cambiar modelo, `Top-k`, embeddings o retrieval se varió una sola variable:

```text
PROMPT
```

Se mantuvo exactamente:

```text
mismo índice
mismo modelo de embeddings
mismo retrieval
mismo Top-k = 4
mismo Ollama
mismo llama3:latest
misma pregunta
```

Único cambio:

```text
instrucciones del prompt
```

El prompt 08B exige de forma explícita:

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

### 6.1 Resultado del Caso C con prompt 08B

El `Top-4` fue exactamente el mismo de la baseline, por lo que el retrieval quedó controlado.

La respuesta mejoró en cobertura:

```text
inspección previa       → cubierta
seguridad previa        → cubierta
procedimiento           → mencionado / resumido
criterio de aceptación  → omitido
```

El LLM ya no ignoró totalmente la segunda parte de la pregunta. Reconoció que debía explicar cómo calibrar y remitió al contenido de la fuente de procedimiento.

Sin embargo, la respuesta quedó todavía por debajo de la evidencia disponible:

- no reprodujo los pasos concretos `0 → 5 → 10 bar`;
- no incluyó los umbrales de ajuste `ZERO` / `SPAN`;
- no incluyó la tolerancia `±0,05 bar` como criterio de aceptación;
- no explicó la acción de evaluación adicional si la tolerancia se supera;
- el formato de citas observado fue `FUENTE 1` / `FUENTE 4`, no exactamente `[FUENTE 1]` / `[FUENTE 4]`.

Evaluación comparada:

```text
                    Paso 08 baseline   Paso 08B
Groundedness        buena              buena
Completeness        insuficiente       mejora, pero aún parcial
Citation compliance parcial            parcial
Abstention          correcta en D      pendiente probar D
```

Aprendizaje:

> **El prompt sí cambia el comportamiento generativo, pero “pedir completeness” no garantiza automáticamente completeness exhaustiva.**

La mejora observada indica que el problema no estaba exclusivamente en retrieval. También confirma que `generation quality` debe evaluarse como una capa propia.

---

## 7. Próximo control

Antes de volver a modificar instrucciones o cambiar modelo, se debe ejecutar el **Caso D con el mismo prompt 08B**.

Objetivo:

```text
mejorar completeness
sin perder abstention
```

Solo después de observar ese resultado se decidirá la siguiente variable controlada.

---

## 8. Lo que todavía NO se concluye

Estas ejecuciones no demuestran que:

- Llama 3 sea el modelo generativo definitivo;
- el prompt 08B sea universalmente mejor;
- una nueva iteración de prompt sea necesariamente la mejor siguiente acción;
- `Top-k=4` sea apropiado fuera de este corpus;
- la abstención sea robusta en cualquier pregunta sin respuesta;
- exista un threshold de similarity capaz de decidir answerability.

El objetivo sigue siendo aprender mediante experimentos controlados y reproducibles antes de introducir optimizaciones adicionales.
