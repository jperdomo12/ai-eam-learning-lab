from __future__ import annotations

import os
import subprocess
import sys

import numpy as np

from step04_semantic_retrieval import load_embedding_model
from step05_query_vector_index import load_index
from step06_build_grounded_context import build_context, build_prompt


DEFAULT_QUERY = "¿Qué debo verificar antes de ajustar el PT-201 y cómo debo calibrarlo?"
GENERATION_TOP_K = 4
DEFAULT_GENERATION_MODEL = "llama3:latest"


def retrieve_top_k(query: str, top_k: int = GENERATION_TOP_K) -> list[dict]:
    embeddings, metadata, manifest = load_index()
    model = load_embedding_model(manifest["model"])

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )[0]

    scores = embeddings @ query_embedding
    ranked = [
        {**record, "similarity": float(score)}
        for record, score in zip(metadata, scores)
    ]
    ranked.sort(key=lambda item: item["similarity"], reverse=True)
    return ranked[:top_k]


def generate_with_ollama(prompt: str, model_name: str) -> str:
    try:
        completed = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "Ollama no está instalado o el comando 'ollama' no está disponible en PATH."
        ) from exc

    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            f"Ollama terminó con código {completed.returncode}: {detail}"
        )

    answer = completed.stdout.strip()
    if not answer:
        raise RuntimeError("Ollama no devolvió texto utilizable.")

    return answer


def main() -> None:
    query = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else DEFAULT_QUERY
    model_name = os.getenv("OLLAMA_MODEL", DEFAULT_GENERATION_MODEL)

    print("RAG LAB — Paso 08: generación fundamentada con LLM local")
    print(f"Pregunta: {query}")
    print(f"Top-k baseline temporal: {GENERATION_TOP_K}")
    print("Runtime generativo: Ollama")
    print(f"Modelo generativo local: {model_name}\n")

    print("Objetivo de aprendizaje:")
    print("- reutilizar el índice persistido y el retrieval ya verificado")
    print("- construir el mismo contexto fundamentado observado en el Paso 06")
    print("- sustituir únicamente la capa de generación por un LLM local")
    print("- reutilizar el modelo local ya disponible antes de instalar otro")
    print("- no usar API keys ni generar coste por consulta")
    print("- comprobar respuesta, citas y abstención")
    print("- demostrar que retrieval y backend generativo son capas desacoplables\n")

    results = retrieve_top_k(query)
    context = build_context(results)
    prompt = build_prompt(query, context)

    print("Top-k enviado al LLM:")
    for position, result in enumerate(results, start=1):
        print(
            f"#{position} | similarity={result['similarity']:.4f} | "
            f"{result['document']} | chunk {result['chunk']} | {result['heading']}"
        )

    print("\n" + "=" * 80)
    print("PROMPT FUNDAMENTADO ENVIADO AL LLM LOCAL")
    print("=" * 80)
    print(prompt)

    print("\n" + "=" * 80)
    print("RESPUESTA DEL LLM LOCAL")
    print("=" * 80)

    try:
        answer = generate_with_ollama(prompt, model_name)
    except Exception as exc:
        print(f"La generación local falló: {type(exc).__name__}: {exc}")
        print("El retrieval y el prompt ya se mostraron arriba; el fallo está en la etapa local de generación.")
        print(f"Si el modelo no está descargado, ejecuta: ollama pull {model_name}")
        raise SystemExit(1)

    print(answer)

    print("\n" + "=" * 80)
    print("OBSERVACIÓN")
    print("El LLM local no hizo el retrieval y no recibió los vectores.")
    print("Recibió únicamente instrucciones + pregunta + texto original recuperado.")
    print("No se utilizó una API generativa de pago.")
    print("El siguiente análisis evaluará la respuesta y después repetirá el Caso D para probar abstención.")
    print("=" * 80)


if __name__ == "__main__":
    main()
