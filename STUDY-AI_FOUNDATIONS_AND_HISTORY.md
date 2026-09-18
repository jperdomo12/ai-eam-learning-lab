# 📘 Fundamentos de IA e historia mínima para AI-Driven EAM

> **Tipo:** STUDY  
> **Estado:** 📘 CONSOLIDADO — referencia transversal; Learning Lab congelado  
> **Actualizado:** 2026-09-18  
>
> **Propósito:** consolidar los conceptos básicos de IA que sirven de base para entender LLM, RAG, MCP y agentes, conectándolos con EAM / IBM Maximo sin convertir esta nota en un tratado académico.

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-18 | Auditoría final del Learning Lab: el estudio queda **consolidado como referencia transversal** y se mantiene para consulta durante el estado congelado del repositorio. |
| 2026-09-18 | Se añade un **Resumen de contenido** inmediatamente después del Historial para facilitar la recuperación rápida de los 19 bloques del estudio. |
| 2026-09-18 | Se enriquecen los fundamentos con una ruta pedagógica completa de una frase por un LLM, ejemplos de tokenización, Token IDs, embeddings, posición, Attention y generación; se añade la distinción explícita entre IA Generativa y LLM con ejemplos generales y EAM. |
| 2026-09-18 | Se añade referencia al estudio transversal `STUDY-LLM_BEYOND_THE_MODEL.md`, que profundiza de forma práctica en Connectors/Apps, Tool Calling, MCP, RAG y acceso de los LLM a sistemas externos. |
| 2026-09-14 | Se amplía la explicación de Tools con la analogía `MCP Server ≈ package/service` y `Tool ≈ función/procedimiento público invocable`, incluyendo el contrato que permite al LLM descubrir y llamar cada Tool. |
| 2026-09-14 | Se mueve la nota a la raíz del repositorio y se amplía la historia de IA, el puente con IA simbólica/Turbo Prolog, el nacimiento progresivo de los LLM, el origen de MCP, entrenamiento/inferencia, cuantización, Fine-tuning vs. RAG y la definición de agente. |
| 2026-09-14 | Creación inicial a partir de notas personales de estudio revisadas y del aprendizaje práctico realizado en los LAB de MCP y RAG. Se actualiza específicamente la situación de IBM Maximo 9.2 respecto a MCP, OSLC y capacidades RAG/DocSearch documentadas por IBM. |

---


## 🧭 Resumen de contenido

| Punto | Contenido |
|---|---|
| **1. Mapa mental general** | Ubica IA, ML, Deep Learning, modelos generativos, LLM, RAG, MCP y agentes en una misma visión. |
| **2. Historia mínima** | Recorre los hitos esenciales desde Turing y Dartmouth hasta Transformer, LLM, MCP y Maximo 9.2. |
| **3. Qué es un LLM** | Explica qué es un LLM, cuándo emerge el concepto moderno y sigue una frase completa por el proceso de generación. |
| **4. Tokenización** | Muestra cómo el texto se divide en tokens y Token IDs antes de ser procesado por el modelo. |
| **5. Embeddings, posición, Transformer y Attention** | Explica cómo el modelo representa tokens numéricamente, conserva orden y relaciona elementos del contexto. |
| **6. Entrenamiento, inferencia y memoria** | Distingue aprendizaje de pesos, uso del modelo y memoria/contexto externo. |
| **7. Modelos, runtimes y productos** | Separa conceptos como GPT/Llama, Ollama y aplicaciones como ChatGPT, Gemini, Claude o Cline. |
| **8. Cuantización** | Explica cómo reducir precisión numérica permite ejecutar modelos con menos memoria y cómputo. |
| **9. IA Generativa vs. LLM** | Aclara similitudes y diferencias entre IA generativa, LLM y ML predictivo, con ejemplos EAM. |
| **10. Cómo ampliar un LLM** | Resume Prompting, RAG, Fine-tuning, Tools y MCP como mecanismos complementarios. |
| **11. MCP y Claude** | Explica el origen de MCP, su relación inicial con Claude y su carácter abierto. |
| **12. Agentes de IA** | Define un agente como sistema con objetivo, modelo, herramientas, estado y ciclo de decisión/acción. |
| **13. RAG y MCP** | Aclara que resuelven problemas diferentes y cómo pueden combinarse en una solución AI-Driven EAM. |
| **14. IBM Maximo: OSLC, MCP y RAG** | Sitúa estas tecnologías en Maximo 2026 y explica cómo pueden coexistir. |
| **15. Lo probado en el Learning Lab** | Resume las pruebas reales realizadas en MCP y RAG. |
| **16. Analogías útiles** | Ofrece imágenes mentales sencillas para recordar LLM, RAG, MCP y agentes sin confundirlos. |
| **17. Síntesis AI-Driven EAM** | Conecta todos los conceptos con la arquitectura y decisiones que interesan al proyecto profesional. |
| **18. Fuentes verificadas** | Recoge referencias primarias e institucionales utilizadas para validar los conceptos principales. |
| **19. Regla de cierre** | Fija el nivel de profundidad buscado: comprender y aplicar sin convertir el estudio en un tratado académico. |

---

## 1. Mapa mental general

Una forma útil de ordenar los conceptos es:

```text
INTELIGENCIA ARTIFICIAL
    ↓
Machine Learning
    ↓
Deep Learning
    ↓
Modelos generativos
    ↓
LLM / modelos multimodales
    ↓
+ Prompting
+ RAG
+ Tools / MCP
+ Agentes
```

No son capas completamente excluyentes, pero esta jerarquía ayuda a entender cómo se relacionan.

Para profundizar específicamente en **cómo el LLM accede a datos, herramientas y conocimiento externo**, usar:

[`STUDY-LLM_BEYOND_THE_MODEL.md`](STUDY-LLM_BEYOND_THE_MODEL.md)

También conviene recordar otra vista:

```text
MODELO
→ aporta capacidad de lenguaje, razonamiento y generación

RAG
→ aporta conocimiento documental recuperado en el momento de la consulta

MCP / Tools
→ aporta acceso a sistemas, datos y acciones

AGENTE
→ utiliza un modelo y herramientas dentro de un ciclo orientado a un objetivo
```

---

## 2. Historia mínima que conviene recordar

La IA no nació con ChatGPT ni con Transformer. Es el resultado de varias etapas que se fueron acumulando.

### 1950 — Alan Turing y la pregunta por la inteligencia de las máquinas

**Alan Turing (1912–1954)** fue un matemático y lógico **británico**. En 1950 publicó *Computing Machinery and Intelligence* y propuso abordar la cuestión de la inteligencia de las máquinas mediante una prueba conversacional que después sería conocida como **Test de Turing**.

La importancia del hito no es que Turing construyera un LLM, sino que ayudó a convertir la pregunta filosófica:

```text
¿puede pensar una máquina?
```

en una cuestión que podía discutirse mediante comportamiento observable.

### 1956 — Dartmouth y el nacimiento formal del campo de IA

**John McCarthy (1927–2011)**, científico informático **estadounidense**, es reconocido por acuñar el término **Artificial Intelligence**.

El **Dartmouth Summer Research Project on Artificial Intelligence** se celebró durante el verano de 1956 en **Dartmouth College, Hanover, New Hampshire, Estados Unidos**. La propuesta había sido preparada por John McCarthy, Marvin Minsky, Nathaniel Rochester y Claude Shannon.

Ese encuentro no inventó de cero todas las ideas de IA, pero sí ayudó a consolidarlas bajo un campo de investigación con nombre propio.

### 1960s–1990s — IA simbólica, lógica y sistemas expertos

Durante décadas tuvo gran importancia la **IA simbólica**: representar conocimiento mediante símbolos, hechos y reglas explícitas y aplicar mecanismos de inferencia.

Modelo mental:

```text
HECHOS
+
REGLAS
+
MOTOR DE INFERENCIA
→
CONCLUSIONES
```

Lenguajes como **Lisp** y **Prolog** estuvieron fuertemente asociados con esta etapa. Prolog surgió a comienzos de los años 1970 en **Marsella, Francia**, alrededor del trabajo de Alain Colmerauer y Philippe Roussel. En los años 1980, productos como **Turbo Prolog** llevaron este estilo de programación lógica a PCs y entornos de formación.

La IA simbólica no desapareció. Sigue siendo útil donde se necesitan reglas explícitas, restricciones, lógica, trazabilidad o conocimiento estructurado.

### Conexión con la experiencia universitaria en Turbo Prolog

Un ejercicio típico permite ver la diferencia entre **programar reglas** y **aprender patrones**.

Supongamos estos hechos:

```text
A > B
B > C
```

y añadimos una regla de transitividad:

```text
si X > Y
y Y > Z
entonces X > Z
```

El sistema puede inferir:

```text
A > C   → verdadero
```

pero no debe inferir automáticamente:

```text
C > A   → falso, salvo que existan otros hechos o reglas que lo permitan
```

En Prolog la idea sería aproximadamente:

```prolog
mayor(a,b).
mayor(b,c).

mayor(X,Z) :- mayor(X,Y), mayor(Y,Z).
```

La conexión conceptual es importante:

```text
IA simbólica / Prolog
→ el conocimiento se escribe explícitamente como hechos y reglas

Machine Learning / LLM
→ los patrones se aprenden estadísticamente a partir de datos
```

Por eso resulta útil pensar en el salto desde **software que expresa reglas** hacia modelos cuyo comportamiento emerge de **pesos aprendidos**.

### 1997 — IBM Deep Blue

IBM Deep Blue derrotó al campeón mundial de ajedrez Garry Kasparov en una revancha celebrada en **Nueva York, Estados Unidos**, en mayo de 1997.

Fue un hito de cómputo especializado, búsqueda y evaluación masiva de posiciones. No era un LLM ni aprendía lenguaje como los modelos actuales. Es importante porque mostró que una máquina podía superar a un humano extraordinario en una tarea cognitiva muy delimitada.

### 2003 — un antecedente directo de los modelos de lenguaje neuronales

Yoshua Bengio y colaboradores publicaron *A Neural Probabilistic Language Model*. El trabajo mostró cómo una red neuronal podía aprender **representaciones distribuidas de palabras** y estimar probabilidades de secuencias de lenguaje, superando algunas limitaciones de los modelos estadísticos de n-gramas.

**Yoshua Bengio**, nacido en París y desarrollado académicamente en Canadá, es una de las figuras centrales del Deep Learning moderno.

Este trabajo es un antecedente mucho más directo de los LLM que Deep Blue.

### 2012 — auge moderno del Deep Learning: AlexNet

El año **2012** es un hito práctico porque Alex Krizhevsky, Ilya Sutskever y Geoffrey Hinton, desde la **University of Toronto, Canadá**, presentaron **AlexNet**, una red neuronal convolucional profunda entrenada con GPUs que obtuvo una mejora muy grande en clasificación de imágenes ImageNet.

El paper *ImageNet Classification with Deep Convolutional Neural Networks* fue presentado en **NIPS 2012**, cuya conferencia se celebró en **Lake Tahoe, Nevada, Estados Unidos**.

¿Por qué 2012 importa tanto?

```text
grandes datasets
+
redes profundas
+
backpropagation
+
GPUs con enorme capacidad paralela
→
resultados que superaron claramente enfoques anteriores
```

No fue el nacimiento de las redes neuronales ni del Deep Learning, que tienen historia anterior. Fue un punto de inflexión que convenció a gran parte de la industria y academia de que escalar redes profundas con datos y cómputo podía producir avances extraordinarios.

Geoffrey Hinton, **británico-canadiense**, junto con Yoshua Bengio y Yann LeCun, **francés-estadounidense**, sería reconocido en 2018 con el A.M. Turing Award por contribuciones fundamentales al Deep Learning.

### 2013–2014 — la IA generativa ya existía antes de Transformer

Antes de 2017 ya existían familias importantes de modelos generativos, entre ellas:

```text
Variational Autoencoders (VAE)
Generative Adversarial Networks (GAN)
modelos de lenguaje recurrentes
```

Por tanto, **no es correcto decir que toda la IA generativa nació con *Attention Is All You Need***.

Lo correcto es:

> **Transformer fue uno de los hitos decisivos que hicieron posible la generación moderna basada en grandes modelos de lenguaje y posteriormente gran parte de la IA multimodal actual.**

### 2017 — *Attention Is All You Need* y Transformer

Ocho investigadores de Google —Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser e Illia Polosukhin— publicaron *Attention Is All You Need*.

El paper propuso la arquitectura **Transformer**, basada en mecanismos de atención y sin depender de recurrencia o convoluciones para procesar secuencias.

El trabajo fue presentado en **NIPS 2017**, celebrado del 4 al 9 de diciembre en **Long Beach, California, Estados Unidos**.

El cambio conceptual fue enorme:

```text
ANTES
procesamiento secuencial/recurrente dominante

TRANSFORMER
attention + paralelización
→ mejor escalabilidad
→ entrenamiento más eficiente
→ mejor manejo de relaciones a larga distancia
```

No toda la IA moderna procede únicamente de este paper. Pero **los LLM modernos basados en Transformer sí dependen directamente de esta arquitectura o de evoluciones de ella**.

### 2018–2020 — aparece la era de los LLM modernos

No existe una fecha única de “nacimiento del LLM”. Es una evolución:

```text
modelos estadísticos de lenguaje
→ modelos neuronales de lenguaje
→ embeddings y redes recurrentes
→ Transformer
→ pretraining a gran escala
→ modelos cada vez mayores
```

Un punto especialmente importante fue **GPT-1 de OpenAI en 2018**, que combinó Transformer con preentrenamiento generativo y adaptación posterior a tareas.

Después llegaron modelos como:

```text
2018 → BERT (Google)
2019 → GPT-2 (OpenAI)
2020 → GPT-3 (OpenAI, 175 mil millones de parámetros)
```

GPT-3 mostró de forma muy visible que escalar un modelo de lenguaje podía producir capacidades de **zero-shot, one-shot y few-shot**, es decir, resolver nuevas tareas mediante instrucciones o pocos ejemplos sin entrenar un modelo diferente para cada tarea.

Una forma útil de recordarlo es:

```text
2003 → lenguaje neuronal moderno empieza a consolidarse
2017 → Transformer
2018 → GPT demuestra pretraining Transformer generalista
2020 → GPT-3 hace evidente la era de los LLM a gran escala
2022 → ChatGPT populariza masivamente el uso conversacional
```

### 2022 — popularización masiva de la IA generativa conversacional

ChatGPT lleva los LLM al uso cotidiano de millones de personas. A partir de ese momento se acelera la adopción empresarial de asistentes, copilots, modelos multimodales y aplicaciones generativas.

### 2024 — Anthropic introduce MCP

Anthropic presentó **Model Context Protocol (MCP)** el **25 de noviembre de 2024** como un estándar abierto para conectar aplicaciones de IA con sistemas donde viven los datos y las herramientas.

El lanzamiento incluyó tres elementos importantes:

```text
1. especificación y SDKs de MCP
2. soporte de servidores MCP locales en Claude Desktop
3. repositorio open source de servidores MCP de referencia
```

Por tanto, **sí: Claude fue uno de los primeros vehículos prácticos de MCP**, especialmente Claude Desktop, pero MCP no fue diseñado para ser exclusivo de Claude.

La arquitectura buscaba ser general:

```text
Aplicación / Host de IA
      ↓
MCP Client
      ↓ protocolo común
MCP Server
      ↓
Datos / Tools / Sistemas
```

Anthropic creó MCP, pero posteriormente el protocolo fue adoptado por muchas otras herramientas y proveedores.

### 2025–2026 — de asistente a agente

La evolución práctica pasa de:

```text
preguntar → responder
```

a:

```text
entender objetivo
→ decidir pasos
→ consultar sistemas
→ usar herramientas
→ observar resultados
→ decidir siguiente acción
→ completar el objetivo
```

En EAM esto abre escenarios como consultar Maximo, recuperar documentación técnica, generar análisis y ejecutar acciones controladas con permisos y gobierno adecuados.

### 2026 — IBM Maximo incorpora MCP como interfaz para agentes

La documentación vigente de **Maximo Application Suite 9.2** incluye un **Maximo MCP Server** oficial. IBM también publicó un Feature Channel el 30 de abril de 2026 y MAS 9.2 fue anunciado el 25 de junio de 2026.

La evidencia revisada confirma la existencia del Maximo MCP Server en MAS 9.2; no se fija aquí el primer build exacto en que apareció la capacidad si IBM no lo documenta de forma inequívoca.

---

## 3. Qué es un LLM y cuándo “nace”

Un **Large Language Model (LLM)** es un modelo neuronal entrenado sobre grandes cantidades de texto para aprender patrones estadísticos del lenguaje y generar o transformar lenguaje.

Simplificando:

```text
texto
→ tokenización
→ representaciones numéricas
→ red neuronal / Transformer
→ probabilidad del siguiente token
→ generación iterativa
→ respuesta
```

### ¿Qué significa “Large”?

No existe un número universal que convierta un modelo en “Large”. El término refleja una combinación de escala:

```text
muchos parámetros
+
grandes conjuntos de entrenamiento
+
mucho cómputo
```

### ¿Cuándo nace el LLM?

No hay un único día.

Los **language models** existen desde décadas antes. Los modelos neuronales de lenguaje se desarrollaron antes de Transformer. El término y la idea moderna de **LLM** se consolidan progresivamente cuando modelos Transformer preentrenados empiezan a escalar fuertemente entre 2018 y 2020.

Para estudiar basta con recordar:

```text
2003 → neural language model de Bengio et al.
2017 → Transformer
2018 → GPT-1
2020 → GPT-3 y escalado masivo
2022 → ChatGPT populariza el paradigma conversacional
```

Un LLM **no funciona como una base de datos exacta de frases** ni como un disco duro que recupera registros literales. Su conocimiento queda distribuido en millones o miles de millones de **pesos** aprendidos durante el entrenamiento.

### 3.1 Ruta de una frase por un LLM

Para visualizar el proceso sin entrar todavía en las matemáticas internas, usemos una frase sencilla:

> **La flor era grande y de color morado.**

El recorrido conceptual es:

```text
TEXTO
"La flor era grande y de color morado."
        ↓
TOKENIZACIÓN
el texto se divide en tokens
        ↓
TOKEN IDs
cada token se representa mediante un identificador numérico
        ↓
EMBEDDINGS
cada token pasa a una representación vectorial aprendida
        ↓
INFORMACIÓN DE POSICIÓN
el modelo conserva información sobre el orden de los tokens
        ↓
ATTENTION
calcula qué partes del contexto se relacionan entre sí
        ↓
CAPAS TRANSFORMER
refinan progresivamente las representaciones contextuales
        ↓
PROBABILIDADES
el modelo calcula qué token podría venir después
        ↓
GENERACIÓN ITERATIVA
elige/genera un token y repite el proceso
```

Ejemplo de relaciones que **Attention** podría reforzar:

```text
flor   ↔ grande
color  ↔ morado
```

Si el texto fuese:

```text
La flor era grande y de color...
```

el modelo no busca una frase exacta en una base de datos. Calcula probabilidades para posibles continuaciones:

```text
morado  → posible / alta según el contexto
rojo    → posible
azul    → posible
...
```

El valor real de cada probabilidad depende del modelo, del contexto y de sus pesos entrenados.

### Ejemplo EAM equivalente

```text
La bomba P-102 presenta alta temperatura en el rodamiento.
```

Conceptualmente el modelo puede construir relaciones contextuales como:

```text
P-102        ↔ bomba
temperatura  ↔ alta
temperatura  ↔ rodamiento
```

Esto no significa que el modelo haya consultado Maximo. Solo muestra cómo puede relacionar elementos que ya están dentro de su contexto.

---

## 4. Tokenización

Los LLM no procesan directamente palabras completas como lo hacemos las personas.

Primero convierten el texto en **tokens**, que pueden ser:

- palabras completas;
- partes de palabras;
- signos;
- números;
- espacios o combinaciones frecuentes de caracteres, según el tokenizer.

Por ejemplo, con nuestra frase:

```text
La flor era grande y de color morado.
```

una división **ilustrativa** podría parecerse a:

```text
["La", " flor", " era", " grande", " y", " de", " color", " morado", "."]
```

Pero esta división **no pretende representar un tokenizer real concreto**. Dependiendo del modelo, una palabra como `morado` podría ser un token completo o dividirse en varias partes.

Después cada token se representa mediante un identificador numérico:

```text
token
→ Token ID
→ número que identifica ese token dentro del vocabulario del modelo
```

Ejemplo puramente conceptual:

```text
"La"      → 123
" flor"   → 8451
" morado" → 21987
```

Los números anteriores son solo ilustrativos. Los Token IDs reales dependen del tokenizer y vocabulario de cada modelo.

El modelo no trabaja con la palabra escrita directamente; trabaja con estas representaciones numéricas y sus transformaciones posteriores.

Otro ejemplo técnico del Lab:

```text
Ajustar ZERO si el error supera 0,02 bar
```

también se convierte en tokens y Token IDs antes de entrar en las capas del modelo.

Consecuencia práctica:

```text
context window
→ se mide en tokens
→ no en páginas ni en palabras exactas
```

Más chunks en un RAG implican normalmente más tokens dentro del contexto del LLM.

---

## 5. Embeddings, posición, Transformer y Attention

### 5.1 Embeddings dentro del LLM

Un **Token ID** identifica un token, pero ese número por sí solo no expresa su significado.

El modelo transforma cada token en un **embedding**: un vector numérico aprendido que permite trabajar matemáticamente con características y relaciones del lenguaje.

Modelo mental:

```text
token
→ Token ID
→ embedding (vector)
→ procesamiento contextual
```

Con nuestra frase:

```text
"La flor era grande y de color morado."
```

el modelo no manipula literalmente las palabras. Manipula vectores asociados a esos tokens y los va ajustando contextualmente a través de sus capas.

> **Importante:** los embeddings internos de un LLM y los embeddings que usamos en RAG comparten la idea de representar información como vectores, pero no son necesariamente el mismo modelo, vector ni propósito.

En RAG:

```text
embedding
→ ayuda a encontrar contenido semánticamente parecido
```

Dentro del LLM:

```text
embedding
→ es parte de la representación numérica que el modelo procesa
```

### 5.2 Posición

El orden importa:

```text
El técnico revisó la bomba.
≠
La bomba revisó al técnico.
```

Aunque aparezcan palabras parecidas, su posición cambia el significado.

Por ello Transformer incorpora información que permite distinguir dónde aparece cada token dentro de la secuencia.

Modelo mental:

```text
embedding del token
+
información de posición
→ representación que entra al Transformer
```

No hace falta memorizar ahora las distintas técnicas de codificación posicional; basta con entender que **el modelo necesita conocer contenido y orden**.

### 5.3 Transformer

La arquitectura Transformer sustituyó gran parte del procesamiento secuencial tradicional por mecanismos de atención que permiten modelar relaciones entre elementos de una secuencia de forma mucho más paralelizable.

Una forma simplificada de verlo es:

```text
tokens representados numéricamente
        ↓
múltiples capas Transformer
        ↓
cada capa refina relaciones y contexto
        ↓
representaciones cada vez más contextuales
```

Transformer no es una única operación de Attention. Está formado por múltiples componentes y capas; para este nivel de estudio basta con recordar que **Attention es uno de sus mecanismos centrales**.

### 5.4 Attention

**Attention** permite que el modelo calcule qué elementos del contexto son relevantes entre sí durante el procesamiento.

Ejemplo con nuestra frase:

```text
"La flor era grande y de color morado."
```

durante el procesamiento, determinados tokens pueden prestar mayor atención a otros tokens relevantes:

```text
flor  ↔ grande
color ↔ morado
```

Otro ejemplo:

```text
"si el error supera 0,02 bar, ajustar ZERO"
```

puede reforzar relaciones como:

```text
error   ↔ 0,02 bar
ajustar ↔ ZERO
```

No significa que exista una regla fija escrita manualmente. Son relaciones calculadas numéricamente por el modelo según el contexto.

En una pregunta RAG puede relacionar:

```text
Pregunta: ¿Cómo calibro el PT-201?
                ↕
Contexto: ZERO / SPAN / 0-5-10 bar / tolerancia
```

### Attention no es Retrieval

Esta distinción es crítica:

```text
RAG retrieval
→ decide qué información EXTERNA entra en el contexto

Attention
→ relaciona tokens que YA están dentro del contexto del modelo
```

Por tanto:

```text
retrieval ≠ attention
```

### 5.5 De Attention a generación

Después de atravesar las capas Transformer, el modelo obtiene una representación contextual del texto y calcula probabilidades para el siguiente token.

Ejemplo:

```text
"La flor era grande y de color"
                ↓
Transformer + contexto
                ↓
probabilidades del siguiente token
                ↓
"morado" / "rojo" / "azul" / ...
```

Una vez generado un token, éste se incorpora al contexto y el proceso continúa:

```text
generar token
→ añadirlo al contexto
→ calcular siguiente token
→ repetir
```

Así se construye una respuesta token a token.

---

## 6. Entrenamiento, inferencia y memoria

### ¿Qué es entrenamiento?

El **entrenamiento** es el proceso mediante el cual se construye/adapta el comportamiento del modelo ajustando sus pesos numéricos a partir de grandes cantidades de ejemplos.

Conceptualmente:

```text
datos
→ modelo hace predicción
→ se calcula error
→ backpropagation
→ se ajustan pesos
→ repetir millones/billones de veces
```

En los grandes modelos suele distinguirse:

```text
PRETRAINING
→ aprendizaje general a gran escala

POST-TRAINING / FINE-TUNING
→ adaptación posterior del comportamiento, capacidades o dominio
```

El entrenamiento es costoso y modifica los **pesos** del modelo.

### ¿Qué es inferencia?

La **inferencia** es utilizar un modelo ya entrenado para obtener una salida.

Cuando escribimos una pregunta en ChatGPT, ejecutamos Llama 3 con Ollama o Cline usa DeepSeek, estamos haciendo principalmente **inferencia**:

```text
prompt
→ pesos ya entrenados
→ cálculo
→ generación de tokens
→ respuesta
```

La inferencia no vuelve a entrenar el modelo por cada pregunta.

### ¿Qué entendemos por “memoria”?

Conviene separar varias cosas:

```text
PESOS
→ conocimiento/patrones aprendidos durante entrenamiento

CONTEXTO
→ información temporal que recibe el modelo durante la consulta

MEMORIA EXTERNA
→ bases de datos, RAG, historiales, sistemas empresariales, etc.
```

Los pesos no son una colección exacta de documentos recuperables. Por eso un LLM puede generalizar e inferir, pero también producir una afirmación plausible que no esté respaldada por una fuente concreta.

---

## 7. Modelos, runtimes y productos

Es importante no confundir estas capas.

### Modelo (LLM)

Ejemplos:

```text
GPT
Gemini
Claude
Llama
Mistral
Qwen
DeepSeek
Gemma
```

### Runtime / plataforma que ejecuta un modelo

Ejemplo del Learning Lab:

```text
Llama 3
→ Modelo (LLM)

Ollama
→ runtime local que ejecuta ese modelo
```

### Producto / aplicación

Ejemplos:

```text
ChatGPT
Gemini
Claude Desktop
Cline
```

Un producto puede usar uno o varios modelos y añadir memoria, búsqueda, herramientas, interfaces, seguridad, orquestación y otros servicios.

### Modelos pequeños y grandes

Existen modelos suficientemente pequeños y/o cuantizados para ejecutarse en:

```text
portátil
edge
algunos smartphones
```

mientras modelos de mayor capacidad suelen ejecutarse en infraestructura cloud con GPUs o aceleradores especializados.

---

## 8. Cuantización

La **cuantización** reduce la precisión numérica utilizada para representar los pesos de un modelo.

Un modelo puede haberse entrenado utilizando números de mayor precisión —por ejemplo FP32, BF16 o FP16— y luego distribuirse en una versión que representa gran parte de sus pesos con menos bits.

Idea simplificada:

```text
16 bits por peso
→ más memoria
→ mayor precisión numérica

8 / 4 bits por peso
→ mucha menos memoria
→ menor tráfico de memoria
→ inferencia local más viable
→ posible pérdida de calidad
```

Ejemplo aproximado para entender la magnitud:

```text
8.000 millones de parámetros × 16 bits
≈ 16 GB solo para pesos

8.000 millones de parámetros × 4 bits
≈ 4 GB solo para pesos
```

En la práctica existen metadatos y overhead, pero explica por qué un modelo que sería difícil de ejecutar en un portátil puede volverse manejable después de cuantizarlo.

En el **RAG LAB** usamos:

```text
Modelo (LLM): llama3:latest
Parámetros:   8B
Cuantización: Q4_0
Tamaño local observado: ~4,7 GB
Runtime:      Ollama
```

`Q4_0` es un formato de cuantización de aproximadamente 4 bits utilizado en el ecosistema local de modelos. Su objetivo principal es reducir memoria y almacenamiento a cambio de cierta pérdida potencial de precisión/calidad frente a una representación de más bits.

La cuantización **no convierte un modelo en RAG ni modifica sus documentos**. Solo cambia cómo se representan numéricamente sus pesos para ejecutarlo de forma más eficiente.

---

## 9. Qué es IA Generativa y cómo se relaciona con un LLM

La **IA generativa** es una categoría amplia de sistemas capaces de producir contenido nuevo a partir de patrones aprendidos.

Puede generar:

```text
texto
código
imagen
audio
video
```

Un **LLM** es un tipo de modelo especializado principalmente en lenguaje: comprenderlo, transformarlo y generarlo.

La relación sencilla es:

```text
INTELIGENCIA ARTIFICIAL
        ↓
Machine Learning
        ↓
Deep Learning
        ↓
IA GENERATIVA
        ↓
   ┌────┴─────────────┐
   ↓                  ↓
  LLM             otros modelos
lenguaje          generativos
                  imagen/audio/video...
```

Por tanto:

> **Un LLM moderno normalmente forma parte de la IA generativa, pero no toda IA generativa es un LLM.**

### Similitudes

Ambos conceptos se relacionan porque:

- aprenden patrones a partir de datos;
- pueden generar contenido nuevo;
- durante inferencia producen una salida a partir de una entrada/contexto;
- los sistemas modernos pueden combinar varias modalidades.

### Diferencias

```text
IA GENERATIVA
→ categoría amplia
→ texto, imagen, audio, video, código...

LLM
→ tipo de modelo
→ centrado históricamente en lenguaje
→ puede formar parte de sistemas multimodales modernos
```

Ejemplos:

```text
ChatGPT generando una explicación
→ IA Generativa
→ usa un modelo de lenguaje

modelo generando una imagen
→ IA Generativa
→ no necesariamente es un LLM

modelo generando música
→ IA Generativa
→ no necesariamente es un LLM
```

La frontera es menos rígida hoy porque algunos modelos modernos son **multimodales**: pueden trabajar con texto, imágenes, audio u otras modalidades dentro del mismo sistema.

### IA predictiva vs. IA generativa

También conviene distinguir:

```text
IA / ML PREDICTIVO
→ clasifica / estima / detecta / predice

IA GENERATIVA
→ crea una salida nueva
```

Ejemplo EAM:

```text
Predecir probabilidad de fallo de la bomba P-102
→ Machine Learning predictivo
→ no necesariamente IA Generativa

Explicar en lenguaje natural por qué P-102 podría estar fallando
→ LLM / IA Generativa

Redactar una recomendación de mantenimiento basada en evidencia
→ LLM / IA Generativa
```

En lenguaje, un LLM genera una respuesta token a token condicionada por:

```text
pesos aprendidos
+
prompt actual
+
contexto disponible
```

### IA generativa ≠ exclusivamente Transformer

Modelos generativos existían antes de 2017. Transformer es especialmente importante porque se convirtió en la arquitectura fundamental de los **LLM modernos** y posteriormente de muchas arquitecturas multimodales.

Por tanto:

```text
IA generativa
→ concepto más amplio y anterior

Transformer
→ arquitectura clave para la era moderna de LLM y mucha GenAI actual
```

---

## 10. Cómo ampliamos o especializamos un LLM

### 10.1 Prompting

Le damos instrucciones, ejemplos y contexto dentro de la propia petición.

No modifica los pesos del modelo.

### 10.2 RAG

Recuperamos conocimiento externo relevante y lo incorporamos al contexto antes de generar la respuesta.

```text
documentos
→ chunks
→ embeddings
→ índice
→ retrieval
→ contexto
→ LLM
```

RAG **no reentrena** el modelo.

### 10.3 Fine-tuning

Fine-tuning es entrenamiento adicional sobre un modelo ya preentrenado. **Sí modifica los pesos**.

Puede ser útil para:

```text
enseñar formatos de salida
especializar comportamiento
adaptar tono/estilo
mejorar una tarea muy concreta
adaptar el modelo a ejemplos de un dominio
```

### RAG versus Fine-tuning en una empresa

Una empresa mediana o grande **sí puede decidir adaptar un modelo con sus propios datos**. Pero conviene distinguir dos objetivos diferentes:

```text
QUIERO QUE EL MODELO SE COMPORTE MEJOR EN MI DOMINIO
→ Fine-tuning / domain adaptation puede ayudar

QUIERO QUE RESPONDA CON DATOS EXACTOS, ACTUALES Y CITABLES DE MIS DOCUMENTOS
→ RAG suele seguir siendo necesario
```

Una confusión frecuente es imaginar:

```text
cargo todos mis manuales mediante fine-tuning
→ los documentos quedan "guardados" exactamente dentro del modelo
→ ya no necesito RAG
```

Eso **no es una buena equivalencia**.

El fine-tuning cambia los pesos para que el modelo aprenda comportamientos/patrones. No crea una base documental exacta y fácilmente auditable. Además:

- cambiar un documento puede exigir nuevo entrenamiento;
- recuperar un valor exacto aprendido en pesos no está garantizado;
- resulta difícil demostrar de qué documento/revisión procede una afirmación;
- permisos y revocación documental son más difíciles de gobernar;
- el conocimiento puede quedar desactualizado.

RAG, en cambio, permite:

- actualizar documentos sin reentrenar el LLM;
- recuperar la revisión vigente;
- mostrar la fuente;
- aplicar filtros y permisos;
- mantener conocimiento empresarial fuera de los pesos del modelo.

### ¿Podrían coexistir?

Sí, y en una arquitectura empresarial madura es perfectamente razonable:

```text
MODELO BASE
   ↓
Fine-tuning / adaptación
→ aprende mejor el lenguaje, formato o tarea del dominio

+

RAG
→ entrega documentación factual vigente y trazable
```

Un modelo afinado para mantenimiento industrial podría comprender mejor terminología, clasificaciones o tipos de respuesta y **aun así usar RAG** para consultar el manual exacto de una bomba, la revisión vigente de un procedimiento o una norma interna.

Por tanto, no conviene pensar:

```text
Fine-tuning O RAG
```

sino:

```text
Fine-tuning
→ especializa comportamiento/capacidad

RAG
→ aporta conocimiento documental externo, actual y trazable
```

Para AI-Driven EAM, RAG sigue teniendo mucho valor incluso si algún día se utiliza un modelo adaptado al dominio EAM.

### 10.4 Tools

El modelo puede invocar funciones externas para consultar o ejecutar acciones.

Ejemplos:

```text
consultar una OT
crear una OT
leer un archivo
buscar inventario
llamar una API
```

Para un perfil de arquitectura/software, una analogía muy útil es pensar en un **package o servicio con operaciones públicas**.

Por ejemplo, conceptualmente en PL/SQL podríamos tener:

```text
PACKAGE MAXIMO_OT
    FUNCTION consultar_ot(...)
    PROCEDURE cambiar_estado_ot(...)
    FUNCTION consultar_prioridad(...)
```

Una organización equivalente en MCP sería:

```text
MCP Server: Maximo
    Tool: consultar_ot(...)
    Tool: cambiar_estado_ot(...)
    Tool: query_maximo(...)
```

La analogía práctica es:

```text
MCP Server
≈ package / servicio que agrupa capacidades

Tool
≈ función o procedimiento público invocable
```

No es una equivalencia literal. Un package de base de datos vive dentro de un motor concreto; un MCP Server es un proceso/servicio que expone capacidades mediante el protocolo MCP. Pero para entender la **unidad funcional** resulta una comparación muy útil.

Además, una Tool MCP no es solo una función con código. Debe exponer un **contrato que el modelo pueda descubrir e interpretar**, normalmente compuesto por:

```text
nombre de la Tool
+
descripción de lo que hace
+
parámetros / esquema de entrada
+
resultado
```

Ejemplo conceptual:

```text
Tool: consultar_ot
Descripción: consulta los detalles de una Orden de Trabajo en Maximo
Entrada: num_ot
Salida: descripción, estado, activo, sitio, prioridad...
```

El LLM puede utilizar esas señales para decidir qué Tool llamar según la intención del usuario.

Por eso una forma útil de recordarlo es:

> **El MCP Server publica capacidades; cada Tool es una operación pública con un contrato suficientemente claro para que un agente/LLM pueda descubrirla e invocarla.**

### 10.5 MCP

MCP estandariza la forma en que aplicaciones/agentes de IA descubren y utilizan herramientas, datos y capacidades ofrecidas por servidores MCP.

---

## 11. MCP: qué es y qué relación tuvo inicialmente con Claude

**Model Context Protocol** es un estándar abierto iniciado por Anthropic para reducir la proliferación de integraciones ad-hoc entre aplicaciones de IA y herramientas/sistemas externos.

Modelo mental:

```text
Host / aplicación de IA
        ↓
MCP Client
        ↓
protocolo MCP
        ↓
MCP Server
        ↓
Tools / Resources / sistemas reales
```

En su lanzamiento de noviembre de 2024, Anthropic publicó:

- la especificación MCP;
- SDKs;
- servidores MCP open source de referencia;
- soporte de servidores MCP locales en **Claude Desktop**.

Por eso Claude Desktop fue una de las primeras formas visibles de utilizar MCP. Nuestro propio MCP LAB siguió precisamente esa secuencia:

```text
Claude Desktop
→ primer Host MCP real utilizado

VS Code + Cline
→ entorno posterior de desarrollo y pruebas
```

Pero MCP no pertenece conceptualmente a Claude como modelo. Un Host puede utilizar otros modelos y seguir hablando MCP.

---

## 12. Qué es un agente de IA

Un **agente de IA** no es simplemente “un LLM que responde mejor”. Es un **sistema** que utiliza un modelo para avanzar hacia un objetivo mediante un ciclo de decisiones y acciones.

Un modelo mental suficientemente preciso es:

```text
OBJETIVO
   ↓
OBSERVAR CONTEXTO / ESTADO
   ↓
LLM decide el siguiente paso
   ↓
USAR TOOL / CONSULTAR / ACTUAR
   ↓
OBSERVAR RESULTADO
   ↓
¿objetivo completado?
   ├─ NO → decidir siguiente paso
   └─ SÍ → entregar resultado
```

Un agente suele combinar:

```text
Modelo (LLM)
+
instrucciones / objetivo
+
herramientas
+
contexto / estado
+
bucle de ejecución
+
controles / permisos / Human-in-the-Loop
```

### Chat tradicional vs. agente

```text
CHAT
Usuario → pregunta → LLM → respuesta

AGENTE
Usuario → objetivo
           ↓
      LLM planifica/decide
           ↓
      usa herramientas
           ↓
      observa resultados
           ↓
      decide otra acción si hace falta
           ↓
      resultado final
```

La autonomía no significa “sin control humano”. En aplicaciones empresariales, especialmente EAM, puede ser deseable exigir aprobación humana para acciones críticas.

---

## 13. RAG y MCP: no resuelven el mismo problema

Modelo mental para AI-Driven EAM:

```text
LLM
→ razonamiento y generación

RAG
→ conocimiento documental

MCP
→ acceso a sistemas, datos y acciones

Maximo
→ contexto EAM transaccional y operacional
```

Ejemplo:

```text
"La bomba B-201 presenta alta temperatura.
¿Tiene OTs abiertas y qué indica el manual?"

MCP / Maximo
→ OTs y estado actual

RAG
→ manual / procedimiento

LLM / agente
→ integra ambas evidencias
```

---

## 14. IBM Maximo: OSLC, MCP y RAG en 2026

### 14.1 OSLC sigue siendo relevante

La llegada de MCP **no elimina ni sustituye OSLC**.

Maximo continúa utilizando APIs, Object Structures y otros mecanismos de integración. La propia documentación del Maximo MCP Server muestra respuestas con `nl2oslc` y URLs OSLC.

Una imagen mental razonable es:

```text
Agente / LLM
      ↓
Maximo MCP Server
      ↓
Tools
      ↓
Maximo Manage
      ↓
OSLC / Object Structures / Automation Scripts / Workflows
```

MCP añade una **interfaz estandarizada orientada a agentes y tools**. OSLC y las capacidades de integración de Maximo siguen existiendo debajo o junto a esa capa.

### 14.2 Servidor MCP oficial de Maximo

La documentación vigente de **Maximo Application Suite 9.2** incluye un **Maximo MCP Server** oficial.

IBM documenta que:

- corre como pod en Red Hat OpenShift;
- permite a agentes acceder a datos y funcionalidades de Maximo Manage mediante tool calls estandarizadas;
- sincroniza su lista de tools con Maximo Manage;
- admite tools personalizadas construidas con Automation Scripts, Object Structures o Workflows;
- permite conectar agentes externos mediante una ruta pública con autenticación;
- el Maximo Assistant agentic utiliza el servidor MCP para encadenar múltiples tool calls.

Esto representa un cambio importante respecto al paradigma tradicional donde un integrador debía trabajar directamente con endpoints y payloads de APIs.

No significa que OSLC haya quedado obsoleto. Significa que el agente puede trabajar con una **capacidad de negocio expuesta como Tool**, mientras Maximo continúa resolviendo internamente la implementación y acceso subyacente.

### 14.3 ¿Tiene Maximo RAG?

La respuesta necesita matiz.

IBM sí documenta capacidades relacionadas con RAG dentro de Maximo Assistant, por ejemplo búsqueda híbrida para reglas/prompts y una tool de búsqueda sobre documentación IBM.

Por tanto, no sería correcto afirmar que **Maximo no utiliza RAG en absoluto**.

Sin embargo, en la documentación IBM revisada hasta 2026-09-14 **no se ha identificado una capacidad general de RAG para indexar documentación técnica propia del cliente —manuales, procedimientos o archivos asociados mediante Doclinks— y responder sobre ella como hicimos en nuestro RAG Learning Lab**.

Distinción:

```text
RAG documentado por IBM
→ capacidades internas del Assistant
→ búsqueda en IBM Documentation

Necesidad AI-EAM que seguimos explorando
→ manuales y procedimientos propios
→ documentación asociada a activos
→ Doclinks / repositorios documentales
→ RAG técnico del cliente
```

Esto deja una arquitectura especialmente interesante:

```text
Maximo MCP
→ datos y acciones transaccionales

RAG propio
→ conocimiento técnico documental del cliente

Modelo (LLM) / agente
→ combina ambas fuentes
```

---

## 15. Lo probado realmente en este Learning Lab

### MCP LAB — ✅ cerrado

Primera etapa:

```text
Claude Desktop
→ Modelo (LLM): Claude
→ Maximo MCP simulado + Filesystem MCP
```

Etapa posterior:

```text
VS Code + Cline
→ Modelo (LLM): DeepSeek V4 Flash
→ Maximo MCP simulado + Filesystem MCP
```

Cline fue el agente/entorno. **DeepSeek V4 Flash fue el Modelo (LLM)** seleccionado durante la revalidación final, principalmente por estar disponible como opción `Free` en ese momento.

### RAG LAB básico — ✅ cerrado

Se verificó:

```text
documentos locales
→ chunking
→ embeddings MiniLM
→ índice persistente
→ retrieval semántico
→ Top-k
→ contexto recuperado
→ Modelo (LLM): Llama 3 local mediante Ollama
→ respuesta fundamentada
```

También se verificó:

```text
retrieval correcto ≠ generación necesariamente completa
Top-k encontrado ≠ respuesta encontrada
similarity ≠ confianza
sin evidencia → el LLM debe abstenerse
```

---

## 16. Analogías útiles, con sus límites

### LLM = cerebro entrenado

Útil para recordar que el modelo aprendió patrones, pero no significa que piense o recuerde como un cerebro humano.

### RAG = bibliotecario

```text
pregunta
→ busca las páginas relevantes
→ se las entrega al modelo
→ el modelo redacta
```

Muy útil para distinguir recuperación de generación.

### MCP = USB / interfaz común

Sirve para recordar que muchos sistemas pueden exponer capacidades mediante un protocolo común, pero **el MCP Server sigue necesitando una implementación real contra el sistema que está detrás**.

### Agente = trabajador con cerebro + manos + objetivo

```text
cerebro → LLM
manos   → Tools / MCP
fuentes → RAG / sistemas
objetivo→ instrucciones
control → permisos / Human-in-the-Loop
```

---

## 17. Síntesis para AI-Driven EAM

La arquitectura conceptual que estamos construyendo puede resumirse así:

```text
                 MODELO (LLM)
               razona / genera
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
        RAG                    MCP
 conocimiento documental   datos y acciones
          ↓                     ↓
manuales/procedimientos    IBM Maximo / sistemas
          └──────────┬──────────┘
                     ↓
                  AGENTE
           coordina hacia un objetivo
```

Para un profesional AI-Driven EAM, el objetivo no es entrenar modelos fundacionales desde cero. Es comprender suficientemente bien estas piezas para poder decidir:

- qué modelo utilizar;
- qué conocimiento debe venir por RAG;
- qué capacidades deben exponerse mediante Tools/MCP;
- qué acciones pueden automatizarse;
- qué controles necesita el agente;
- cómo integrar todo ello con EAM / IBM Maximo de forma mantenible y segura.

---

## 18. Fuentes de referencia verificadas

Esta nota es de estudio, no una bibliografía académica exhaustiva. Para los hitos principales se revisaron fuentes primarias o institucionales:

- Alan Turing — contexto biográfico: https://www.britannica.com/biography/Alan-Turing
- Dartmouth y nacimiento formal de AI: https://ai.dartmouth.edu/our-story
- Propuesta de Dartmouth (1955/1956): https://onlinelibrary.wiley.com/doi/full/10.1609/aimag.v27i4.1904
- IBM Deep Blue: https://www.ibm.com/history/deep-blue
- Bengio et al. (2003), *A Neural Probabilistic Language Model*: https://www.jmlr.org/papers/v3/bengio03a.html
- Krizhevsky, Sutskever & Hinton (2012), AlexNet: https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html
- Google Research (2017), *Attention Is All You Need*: https://research.google/pubs/attention-is-all-you-need/
- NIPS 2017, Long Beach: https://nips.cc/Conferences/2017
- OpenAI (2018), generative pretraining / GPT: https://openai.com/index/language-unsupervised/
- OpenAI (2020), GPT-3: https://openai.com/index/language-models-are-few-shot-learners/
- Anthropic (2024), lanzamiento de MCP: https://www.anthropic.com/news/model-context-protocol
- Microsoft Learn, RAG vs Fine-tuning: https://learn.microsoft.com/en-us/azure/developer/ai/augment-llm-rag-fine-tuning
- IBM, Maximo MCP Server overview: https://www.ibm.com/docs/en/masv-and-l/cd?topic=developing-maximo-mcp-server-overview
- IBM, conexión de agentes externos a Maximo MCP: https://www.ibm.com/docs/en/masv-and-l/cd?topic=developing-connecting-external-agents
- IBM, anuncio MAS 9.2: https://www.ibm.com/new/announcements/introducing-maximo-application-suite-9-2

---

## 19. Regla de cierre

> **Entender IA para AI-Driven EAM no significa memorizar toda su matemática. Significa comprender cómo se relacionan modelo, contexto, conocimiento, herramientas, agentes y sistemas empresariales; saber qué problema resuelve cada pieza y poder validar con práctica cuándo usarla.**