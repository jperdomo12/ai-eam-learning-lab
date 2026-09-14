from __future__ import annotations

import os
import sys

from step06_build_grounded_context import build_context
from step08_generate_grounded_answer import (
    DEFAULT_GENERATION_MODEL,
    DEFAULT_QUERY,
    GENERATION_TOP_K,
    generate_with_ollama,
    retrieve_top_k,
)


def build_completeness_prompt(query: str, context: str) -> str:
    return f"""INSTRUCCIONES
Responde únicamente con base en el CONTEXTO RECUPERADO.
No inventes pasos, valores ni condiciones que no estén respaldados por las fuentes.

Antes de redactar la respuesta:
1. identifica todas las partes explícitas de la PREGUNTA;
2. revisa todas las FUENTES recuperadas, no solo la primera que parezca relevante;
3. responde cada parte de la pregunta para la que exista evidencia;
4. si alguna parte no tiene evidencia suficiente, indícalo explícitamente;
5. antes de finalizar, verifica que no hayas omitido ninguna parte respaldada por el contexto.

Al responder, cita las afirmaciones usando [FUENTE 1], [FUENTE 2], etc.
No uses conocimiento externo al CONTEXTO RECUPERADO.

PREGUNTA
{query}

CONTEXTO RECUPERADO
{context}
""".strip()


def main() -> None:
    query = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else DEFAULT_QUERY
    model_name = os.getenv("OLLAMA_MODEL", DEFAULT_GENERATION_MODEL)

    print("RAG LAB — Paso 08B: experimento controlado de completeness del prompt")
    print(f"Pregunta: {query}")
    print(f"Top-k: {GENERATION_TOP_K}")
    print("Runtime generativo: Ollama")
    print(f"Modelo generativo local: {model_name}\n")

    print("Variable controlada:")
    print("- mismo índice persistido")
    print("- mismo modelo de embeddings")
    print("- mismo retrieval")
    print(f"- mismo Top-k = {GENERATION_TOP_K}")
    print("- mismo LLM local y runtime")
    print("- misma pregunta")
    print("- ÚNICO cambio: instrucciones del prompt para exigir cobertura de todas las partes respaldadas\n")

    results = retrieve_top_k(query)
    context = build_context(results)
    prompt = build_completeness_prompt(query, context)

    print("Top-k enviado al LLM:")
    for position, result in enumerate(results, start=1):
        print(
            f"#{position} | similarity={result['similarity']:.4f} | "
            f"{result['document']} | chunk {result['chunk']} | {result['heading']}"
        )

    print("\n" + "=" * 80)
    print("PROMPT 08B ENVIADO AL LLM LOCAL")
    print("=" * 80)
    print(prompt)

    print("\n" + "=" * 80)
    print("RESPUESTA DEL LLM LOCAL")
    print("=" * 80)

    try:
        answer = generate_with_ollama(prompt, model_name)
    except Exception as exc:
        print(f"La generación local falló: {type(exc).__name__}: {exc}")
        raise SystemExit(1)

    print(answer)

    print("\n" + "=" * 80)
    print("OBSERVACIÓN")
    print("Este experimento conserva retrieval, Top-k y modelo generativo.")
    print("Solo cambia el prompt para estudiar si mejora completeness sin dañar abstention.")
    print("Debe compararse contra la baseline del Paso 08, no sustituirla retroactivamente.")
    print("=" * 80)


if __name__ == "__main__":
    main()
