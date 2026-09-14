from __future__ import annotations

import os
import sys

import numpy as np

from step04_semantic_retrieval import load_embedding_model
from step05_query_vector_index import load_index
from step06_build_grounded_context import build_context, build_prompt


DEFAULT_QUERY = "¿Qué debo verificar antes de ajustar el PT-201 y cómo debo calibrarlo?"
GENERATION_TOP_K = 4
DEFAULT_GENERATION_MODEL = "gpt-5.6-luna"
MAX_OUTPUT_TOKENS = 800


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


def generate_with_openai(prompt: str, model_name: str) -> str:
    try:
        from openai import OpenAI
    except ImportError:
        print("Falta instalar el SDK oficial de OpenAI para esta ruta opcional.")
        print("Ejecuta:")
        print("  python -m pip install -r rag/requirements_openai_optional.txt")
        raise SystemExit(1)

    if not os.getenv("OPENAI_API_KEY"):
        print("No se encontró la variable de entorno OPENAI_API_KEY.")
        print("No escribas la clave dentro del código ni la subas a GitHub.")
        print("Configúrala en tu entorno antes de volver a ejecutar este paso.")
        raise SystemExit(1)

    client = OpenAI()

    response = client.responses.create(
        model=model_name,
        input=prompt,
        max_output_tokens=MAX_OUTPUT_TOKENS,
    )

    return response.output_text.strip()


def main() -> None:
    query = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else DEFAULT_QUERY
    model_name = os.getenv("OPENAI_MODEL", DEFAULT_GENERATION_MODEL)

    print("RAG LAB — Paso 08A: generación fundamentada con OpenAI API (ruta opcional)")
    print(f"Pregunta: {query}")
    print(f"Top-k baseline temporal: {GENERATION_TOP_K}")
    print(f"Modelo generativo: {model_name}\n")

    print("Objetivo de aprendizaje:")
    print("- reutilizar el índice persistido y el retrieval ya verificado")
    print("- construir el mismo contexto fundamentado observado en el Paso 06")
    print("- enviar pregunta + instrucciones + evidencia a un LLM real")
    print("- comprobar respuesta, citas y abstención sin dar acceso al LLM a herramientas externas")
    print("- esta ruta API queda como alternativa opcional del LAB\n")

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
    print("PROMPT FUNDAMENTADO ENVIADO AL LLM")
    print("=" * 80)
    print(prompt)

    print("\n" + "=" * 80)
    print("RESPUESTA DEL LLM")
    print("=" * 80)

    try:
        answer = generate_with_openai(prompt, model_name)
    except Exception as exc:
        print(f"La llamada al LLM falló: {type(exc).__name__}: {exc}")
        print("El retrieval y el prompt ya se mostraron arriba; el fallo está en la etapa de generación/API.")
        raise SystemExit(1)

    print(answer)

    print("\n" + "=" * 80)
    print("OBSERVACIÓN")
    print("En este paso el LLM no hizo el retrieval y no recibió los vectores.")
    print("Recibió únicamente instrucciones + pregunta + texto original recuperado.")
    print("La ruta local del LAB permite probar el mismo contrato sin coste de API.")
    print("=" * 80)


if __name__ == "__main__":
    main()
