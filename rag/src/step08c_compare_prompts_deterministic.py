from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

from step06_build_grounded_context import build_context, build_prompt
from step08_generate_grounded_answer import (
    DEFAULT_GENERATION_MODEL,
    DEFAULT_QUERY,
    GENERATION_TOP_K,
    retrieve_top_k,
)
from step08b_generate_grounded_answer_prompt_completeness import build_completeness_prompt


OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
GENERATION_TEMPERATURE = 0.0
GENERATION_SEED = 42
REPETITIONS = 2


def generate_with_ollama_api(prompt: str, model_name: str) -> str:
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": GENERATION_TEMPERATURE,
            "seed": GENERATION_SEED,
        },
    }

    request = urllib.request.Request(
        OLLAMA_GENERATE_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "No se pudo conectar con la API local de Ollama en "
            f"{OLLAMA_GENERATE_URL}. Verifica que Ollama esté ejecutándose."
        ) from exc

    answer = str(body.get("response", "")).strip()
    if not answer:
        raise RuntimeError("Ollama no devolvió texto utilizable.")

    return answer


def run_prompt(label: str, prompt: str, model_name: str) -> list[str]:
    print("\n" + "=" * 80)
    print(label)
    print("=" * 80)

    answers: list[str] = []
    for run_number in range(1, REPETITIONS + 1):
        print(f"\n--- Ejecución {run_number}/{REPETITIONS} ---")
        answer = generate_with_ollama_api(prompt, model_name)
        answers.append(answer)
        print(answer)

    print("\nReproducibilidad dentro de este prompt:")
    if len(set(answers)) == 1:
        print("- las ejecuciones fueron IDÉNTICAS")
    else:
        print("- las ejecuciones fueron DIFERENTES")

    return answers


def main() -> None:
    query = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else DEFAULT_QUERY
    model_name = os.getenv("OLLAMA_MODEL", DEFAULT_GENERATION_MODEL)

    print("RAG LAB — Paso 08C: comparación reproducible de prompts")
    print(f"Pregunta: {query}")
    print(f"Top-k: {GENERATION_TOP_K}")
    print(f"Runtime generativo: Ollama API local")
    print(f"Modelo generativo local: {model_name}")
    print(f"temperature: {GENERATION_TEMPERATURE}")
    print(f"seed: {GENERATION_SEED}")
    print(f"repeticiones por prompt: {REPETITIONS}\n")

    print("Objetivo de aprendizaje:")
    print("- hacer reproducible la etapa generativa antes de seguir comparando prompts")
    print("- mantener fijo retrieval, Top-k, modelo y parámetros de generación")
    print("- comparar prompt baseline vs prompt 08B bajo las mismas condiciones")
    print("- repetir cada prompt para observar si la salida se mantiene estable")
    print("- NO reinterpretar retroactivamente las ejecuciones 08/08B, que quedan como evidencia histórica\n")

    results = retrieve_top_k(query)
    context = build_context(results)
    baseline_prompt = build_prompt(query, context)
    completeness_prompt = build_completeness_prompt(query, context)

    print("Top-k compartido por ambos prompts:")
    for position, result in enumerate(results, start=1):
        print(
            f"#{position} | similarity={result['similarity']:.4f} | "
            f"{result['document']} | chunk {result['chunk']} | {result['heading']}"
        )

    try:
        baseline_answers = run_prompt(
            "PROMPT A — baseline del Paso 08",
            baseline_prompt,
            model_name,
        )
        completeness_answers = run_prompt(
            "PROMPT B — completeness del Paso 08B",
            completeness_prompt,
            model_name,
        )
    except Exception as exc:
        print(f"\nLa generación local falló: {type(exc).__name__}: {exc}")
        raise SystemExit(1)

    print("\n" + "=" * 80)
    print("RESUMEN DEL CONTROL")
    print("=" * 80)
    print(f"Prompt A reproducible: {len(set(baseline_answers)) == 1}")
    print(f"Prompt B reproducible: {len(set(completeness_answers)) == 1}")
    print("La comparación cualitativa entre A y B debe hacerse usando estas salidas")
    print("porque comparten exactamente retrieval, modelo y parámetros de generación.")
    print("=" * 80)


if __name__ == "__main__":
    main()
