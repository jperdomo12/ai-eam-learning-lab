# LAB — Paso 08: evaluación de generación fundamentada

> **Tipo:** LAB  
> **Estado:** 🧪 EN CURSO — Paso 08B C y D ejecutados; siguiente control: reproducibilidad de generación  
> **Fecha:** 2026-09-14

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-14 | 🧪 Se ejecuta el **Paso 08B — Caso D** con el mismo prompt orientado a completeness. La abstención se conserva: el modelo declara que el contexto no contiene el par de apriete y no inventa ningún valor. La respuesta sigue sin respetar exactamente el formato solicitado `[FUENTE n]`, usando una referencia textual global a las fuentes. |
| 2026-09-14 | ⚙️ Se identifica una limitación metodológica importante de las comparaciones 08/08B: la generación se ejecutó mediante `ollama run` sin fijar explícitamente parámetros de muestreo. Por tanto, aunque retrieval/modelo/pregunta se mantuvieron, una sola ejecución por prompt no permite atribuir toda diferencia únicamente al prompt. Se prepara el **Paso 08C** con API local de Ollama, `temperature=0`, `seed=42` y dos repeticiones por prompt para crear una comparación reproducible. |
| 2026-09-14 | 🧪 Se ejecuta el **Paso 08B — Caso C** variando las instrucciones del prompt. La respuesta mejora claramente respecto a la baseline: cubre inspección, seguridad y menciona el procedimiento de calibración. Sin embargo, sigue siendo **parcialmente incompleta**: resume el procedimiento en lugar de desarrollar sus pasos respaldados y omite los criterios de aceptación de `[FUENTE 3]`. Además, las referencias aparecen como `FUENTE 1`/`FUENTE 4` en lugar del formato solicitado `[FUENTE n]`. |
| 2026-09-14 | Se documenta la baseline end-to-end del Paso 08 con Ollama + `llama3:latest`: Caso C fundamentado pero incompleto y Caso D con abstención correcta. Se prepara el Paso 08B para variar las instrucciones del prompt y estudiar `completeness` sin cambiar retrieval, `Top-k` ni modelo. |

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

El contexto contenía evidencia suficiente para inspección, seguridad, procedimiento y criterio de aceptación.

Resultado observado:

```text
inspección previa       → cubierta
seguridad previa        → cubierta
procedimiento           → omitido
criterio de aceptación  → omitido
```

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

Ningún chunk contiene el dato solicitado.

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
citation correctness → no usó referencias explícitas
abstention           → CORRECTA
```

Aprendizaje:

> **Top-k existente no obliga a inventar una respuesta.**

---

## 5. Paso 08B — prompt orientado a completeness

El prompt 08B añade instrucciones explícitas para:

```text
1. identificar todas las partes de la pregunta;
2. revisar todas las fuentes;
3. responder cada parte respaldada;
4. declarar qué parte carece de evidencia;
5. comprobar antes de finalizar que no se omitió evidencia aplicable.
```

Script:

```text
rag/src/step08b_generate_grounded_answer_prompt_completeness.py
```

### 5.1 Caso C con prompt 08B

Con el mismo `Top-4`, la respuesta mejoró:

```text
inspección previa       → cubierta
seguridad previa        → cubierta
procedimiento           → mencionado / resumido
criterio de aceptación  → omitido
```

Limitaciones observadas:

- no desarrolló los pasos `0 → 5 → 10 bar`;
- no incluyó de forma completa los ajustes `ZERO` / `SPAN`;
- no incluyó la tolerancia `±0,05 bar` ni la evaluación adicional;
- las citas no respetaron exactamente `[FUENTE n]`.

Evaluación comparada, solo como observación inicial:

```text
                    Paso 08 baseline   Paso 08B
Groundedness        buena              buena
Completeness        insuficiente       mejora, pero parcial
Citation compliance parcial            parcial
```

### 5.2 Caso D con prompt 08B

La misma pregunta sin respuesta documental produjo una abstención correcta:

```text
No hay información en el contexto recuperado que indique el par de apriete
...
no se puede determinar ... basado en el contexto recuperado.
```

Evaluación:

```text
groundedness         → BUENA
abstention           → CORRECTA
citation compliance  → PARCIAL; menciona "Fuentes 1, 2, 3 y 4" pero no `[FUENTE n]`
```

Conclusión provisional:

```text
prompt 08B
→ mejora aparente de completeness en C
→ mantiene abstention en D
→ no corrige todavía citation compliance
```

---

## 6. Limitación metodológica descubierta: stochasticity

Las ejecuciones 08 y 08B se hicieron con:

```text
ollama run llama3:latest <prompt>
```

sin fijar explícitamente parámetros como `temperature` y `seed`.

Eso significa que, aunque se mantuvieron fijos retrieval, `Top-k`, modelo y pregunta, la generación podía contener variación de muestreo entre ejecuciones.

Por tanto, no debemos afirmar todavía que **toda** la diferencia observada entre Paso 08 y 08B fue causada exclusivamente por el prompt.

Aprendizaje metodológico:

> **Un experimento controlado de generación debe controlar también la stochasticity del LLM.**

La documentación oficial de Ollama expone `temperature` como parámetro de generación y `seed` como mecanismo para obtener salidas reproducibles con el mismo prompt/modelo.

---

## 7. Paso 08C — comparación reproducible de prompts

Se crea:

```text
rag/src/step08c_compare_prompts_deterministic.py
```

El nuevo control utiliza la API local de Ollama:

```text
http://localhost:11434/api/generate
```

sin autenticación y sin coste externo.

Parámetros fijados:

```text
temperature = 0
seed        = 42
repeticiones por prompt = 2
```

Se recupera el contexto una sola vez y se comparan bajo exactamente las mismas condiciones:

```text
PROMPT A → baseline Paso 08
PROMPT B → completeness Paso 08B
```

Cada prompt se ejecuta dos veces para observar si la salida es estable.

Este Paso 08C **no reescribe retroactivamente** los resultados anteriores. Los Pasos 08 y 08B permanecen como evidencia histórica que llevó a descubrir la necesidad de controlar reproducibilidad.

---

## 8. Próximo paso

Ejecutar primero el Caso C con Paso 08C:

```text
python rag/src/step08c_compare_prompts_deterministic.py
```

Objetivos:

```text
1. comprobar si cada prompt produce dos salidas idénticas;
2. comparar baseline vs 08B en condiciones reproducibles;
3. reevaluar completeness y citation compliance;
4. solo después repetir Caso D.
```

---

## 9. Lo que todavía NO se concluye

Las ejecuciones actuales no demuestran que:

- Llama 3 sea el modelo generativo definitivo;
- el prompt 08B sea universalmente mejor;
- la diferencia observada en una sola ejecución se deba exclusivamente al prompt;
- `Top-k=4` sea apropiado fuera de este corpus;
- la abstención sea robusta en cualquier pregunta sin respuesta;
- exista un threshold de similarity capaz de decidir answerability.

El objetivo sigue siendo aprender mediante experimentos controlados y reproducibles antes de introducir optimizaciones adicionales.
