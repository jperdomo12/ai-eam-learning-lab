from __future__ import annotations

import sys

from step04_semantic_retrieval import load_embedding_model
from step05_query_vector_index import DEFAULT_QUERY, TOP_K, load_index


def retrieve_top_k(query: str) -> list[dict]:
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
    return ranked[:TOP_K]


def build_context(results: list[dict]) -> str:
    blocks: list[str] = []

    for position, result in enumerate(results, start=1):
        blocks.append(
            "\n".join(
                [
                    f"[FUENTE {position}]",
                    f"Documento: {result['document']}",
                    f"Sección: {result['heading']}",
                    f"Chunk: {result['chunk']}",
                    "Contenido:",
                    result["content"],
                ]
            )
        )

    return "\n\n".join(blocks)


def build_prompt(query: str, context: str) -> str:
    return f"""INSTRUCCIONES
Responde únicamente con base en el CONTEXTO RECUPERADO.
No inventes pasos, valores ni condiciones que no estén respaldados por las fuentes.
Si el contexto no contiene evidencia suficiente, indícalo explícitamente.
Al responder, cita las fuentes como [FUENTE 1], [FUENTE 2], etc.

PREGUNTA
{query}

CONTEXTO RECUPERADO
{context}
""".strip()


def main() -> None:
    query = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else DEFAULT_QUERY

    print("RAG LAB — Paso 06: construir contexto fundamentado para el LLM")
    print(f"Pregunta: {query}\n")
    print("Objetivo de aprendizaje:")
    print("- recuperar Top-k desde el índice persistido")
    print("- volver del vector al TEXTO ORIGINAL de cada chunk")
    print("- construir un contexto explícito con fuentes")
    print("- mostrar el prompt que recibiría un LLM")
    print("- todavía NO llamamos a ningún LLM\n")

    results = retrieve_top_k(query)
    context = build_context(results)
    prompt = build_prompt(query, context)

    print("Top-k recuperado:")
    for position, result in enumerate(results, start=1):
        print(
            f"#{position} | similarity={result['similarity']:.4f} | "
            f"{result['document']} | chunk {result['chunk']} | {result['heading']}"
        )

    print("\n" + "=" * 80)
    print("CONTEXTO RECUPERADO")
    print("=" * 80)
    print(context)

    print("\n" + "=" * 80)
    print("PROMPT FUNDAMENTADO — esto sería enviado al LLM")
    print("=" * 80)
    print(prompt)

    print("\n" + "=" * 80)
    print("OBSERVACIÓN")
    print("Los embeddings solo sirvieron para localizar los chunks.")
    print("El LLM recibiría el TEXTO ORIGINAL recuperado, no los vectores.")
    print("La siguiente etapa podrá añadir generación sin cambiar el mecanismo de retrieval.")
    print("=" * 80)


if __name__ == "__main__":
    main()
