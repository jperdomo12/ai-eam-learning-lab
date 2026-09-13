from __future__ import annotations

import sys
from pathlib import Path

from step02_read_and_chunk import DEFAULT_SOURCE_DIR, create_chunks, discover_text_documents


DEFAULT_QUERY = "¿Cómo ajusto el transmisor de presión?"
DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
TOP_K = 3


def load_embedding_model(model_name: str):
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("Falta la dependencia 'sentence-transformers'.")
        print("Instálala con:")
        print("  python -m pip install -r rag/requirements.txt")
        raise SystemExit(1)

    print(f"Cargando modelo de embeddings: {model_name}")
    print("Nota: la primera ejecución puede descargar el modelo y tardar más.\n")
    return SentenceTransformer(model_name)


def build_chunk_records(folder: Path) -> list[dict]:
    records: list[dict] = []

    for document in discover_text_documents(folder):
        for chunk_index, chunk in enumerate(create_chunks(document), start=1):
            searchable_text = f"{chunk['heading']}\n{chunk['content']}"
            records.append(
                {
                    "document": document.name,
                    "chunk": chunk_index,
                    "heading": chunk["heading"],
                    "content": chunk["content"],
                    "searchable_text": searchable_text,
                }
            )

    return records


def semantic_retrieve(model, records: list[dict], query: str, top_k: int = TOP_K) -> tuple[list[dict], int]:
    texts = [record["searchable_text"] for record in records]

    # Normalizamos los embeddings para poder usar producto punto como cosine similarity.
    chunk_embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )[0]

    scores = chunk_embeddings @ query_embedding

    ranked: list[dict] = []
    for record, score in zip(records, scores):
        ranked.append({**record, "similarity": float(score)})

    ranked.sort(key=lambda item: item["similarity"], reverse=True)
    return ranked[:top_k], len(query_embedding)


def main() -> None:
    folder = DEFAULT_SOURCE_DIR
    query = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else DEFAULT_QUERY

    print("RAG LAB — Paso 04: retrieval semántico con embeddings")
    print(f"Carpeta fuente: {folder}")
    print(f"Pregunta/búsqueda: {query}\n")
    print("Objetivo de aprendizaje:")
    print("- convertir cada chunk y la pregunta en vectores")
    print("- comparar los vectores por similitud semántica")
    print("- recuperar los chunks cuyo significado esté más cerca de la pregunta")
    print("- todavía NO usamos vector store: embeddings y chunks viven solo en memoria RAM\n")

    model = load_embedding_model(DEFAULT_MODEL)
    records = build_chunk_records(folder)

    if not records:
        print("No se encontraron chunks para comparar.")
        return

    results, dimensions = semantic_retrieve(model, records, query)

    print(f"Chunks evaluados: {len(records)}")
    print(f"Dimensiones del embedding: {dimensions}")
    print(f"Top-{len(results)} chunks por similitud semántica:\n")

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
    print("Compara este ranking con el Paso 03 léxico usando la misma pregunta.")
    print("Aquí no contamos palabras iguales: comparamos representaciones vectoriales del significado.")
    print("Los embeddings de este paso NO se guardan todavía; el siguiente paso estudiará persistencia/indexación.")
    print("=" * 80)


if __name__ == "__main__":
    main()
