from __future__ import annotations

import json
import sys

import numpy as np

from step04_semantic_retrieval import load_embedding_model
from step05_build_vector_index import EMBEDDINGS_PATH, MANIFEST_PATH, METADATA_PATH


DEFAULT_QUERY = "¿Qué pasos debo seguir para ajustar correctamente un transmisor de presión?"
TOP_K = 3


def load_index() -> tuple[np.ndarray, list[dict], dict]:
    missing = [
        path
        for path in (EMBEDDINGS_PATH, METADATA_PATH, MANIFEST_PATH)
        if not path.exists()
    ]
    if missing:
        print("Falta construir el índice vectorial.")
        print("Ejecuta primero:")
        print("  python rag/src/step05_build_vector_index.py")
        raise SystemExit(1)

    embeddings = np.load(EMBEDDINGS_PATH)
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    if len(embeddings) != len(metadata):
        raise ValueError("Índice inconsistente: embeddings y metadata tienen distinto número de registros.")

    return embeddings, metadata, manifest


def main() -> None:
    query = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else DEFAULT_QUERY

    print("RAG LAB — Paso 05B: consultar índice vectorial persistente")
    print(f"Pregunta/búsqueda: {query}\n")
    print("Objetivo de aprendizaje:")
    print("- cargar embeddings de documentos ya persistidos")
    print("- NO volver a leer ni re-embeddizar todos los documentos")
    print("- generar solo el embedding de la pregunta")
    print("- comparar contra el índice persistido y recuperar Top-k\n")

    embeddings, metadata, manifest = load_index()

    print("Índice cargado:")
    print(f"- modelo: {manifest['model']}")
    print(f"- chunks: {manifest['chunks']}")
    print(f"- dimensiones: {manifest['dimensions']}")
    print(f"- embeddings persistidos: {EMBEDDINGS_PATH}\n")

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
    results = ranked[:TOP_K]

    print(f"Top-{len(results)} chunks desde el índice persistido:\n")
    for position, result in enumerate(results, start=1):
        print("=" * 80)
        print(
            f"#{position} | similarity={result['similarity']:.4f} | "
            f"{result['document']} | chunk {result['chunk']}"
        )
        print(f"Sección: {result['heading']}")
        print("-" * 80)
        print(result["content"])
        print()

    print("=" * 80)
    print("OBSERVACIÓN")
    print("En este paso los vectores de los documentos ya estaban guardados en disco.")
    print("Durante la consulta solo generamos el embedding de la pregunta y lo comparamos con el índice.")
    print("Esto separa claramente INDEXACIÓN y CONSULTA, aunque todavía no usemos una vector database.")
    print("=" * 80)


if __name__ == "__main__":
    main()
